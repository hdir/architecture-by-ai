"""
Convert all files in background/helsereform/input to Markdown using the Datalab REST API.
Output is saved to background/helsereform/markdown/
"""

import os
import argparse
import base64
import re
import time
import requests
from pathlib import Path
from urllib.parse import quote

API_KEY = os.environ.get("DATALAB_API_KEY", "g8Ago5sK2TC95qxrl-J3BVXbsw0c0PkZnKx-6kBZ-q8")
API_URL = "https://www.datalab.to/api/v1/marker"
HEADERS = {"X-Api-Key": API_KEY}

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".epub", ".html"}
MAX_CONCURRENT = 1        # Sequential to avoid rate limits
SUBMIT_DELAY = 7          # Seconds between submissions (free tier: 10/min)
POLL_INTERVAL = 3
MAX_POLLS = 120


def submit_file(file_path: Path) -> tuple[Path, str | None, str | None]:
    mime_types = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".epub": "application/epub+zip",
        ".html": "text/html",
    }
    mime = mime_types.get(file_path.suffix.lower(), "application/octet-stream")
    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, mime)}
        data = {
            "output_format": (None, "markdown"),
            "force_ocr": (None, "false"),
            "disable_image_extraction": (None, "false"),
        }
        try:
            response = requests.post(API_URL, headers=HEADERS, files=files, data=data, timeout=60)
            if not response.ok:
                return file_path, None, f"HTTP {response.status_code}: {response.text[:200]}"
            result = response.json()
            return file_path, result.get("request_check_url"), None
        except Exception as e:
            return file_path, None, str(e)


def decode_image(image_data) -> bytes:
    if isinstance(image_data, dict):
        image_data = (
            image_data.get("content")
            or image_data.get("data")
            or image_data.get("base64")
            or image_data.get("url")
        )
    if not isinstance(image_data, str):
        raise ValueError("Unsupported image payload")
    if image_data.startswith("data:"):
        image_data = image_data.split(",", 1)[1]
    if image_data.startswith(("http://", "https://")):
        response = requests.get(image_data, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.content
    return base64.b64decode(image_data)


def extract_images(status: dict) -> list[tuple[str, bytes]]:
    raw_images = status.get("images") or status.get("image_files") or {}
    if isinstance(raw_images, dict):
        image_items = raw_images.items()
    elif isinstance(raw_images, list):
        image_items = (
            (image.get("filename") or image.get("name"), image)
            for image in raw_images
            if isinstance(image, dict)
        )
    else:
        return []

    images = []
    for filename, image_data in image_items:
        if not filename:
            continue
        try:
            images.append((Path(filename).name, decode_image(image_data)))
        except (ValueError, base64.binascii.Error, requests.RequestException) as error:
            print(f"  WARNING unable to save image {filename}: {error}")
    return images


def add_image_references(markdown: str, images: list[tuple[str, bytes]], output_dir: Path, document_stem: str) -> str:
    if not images:
        return markdown

    image_dir = output_dir / document_stem
    image_dir.mkdir(parents=True, exist_ok=True)
    image_paths = {}
    for filename, image_data in images:
        image_path = image_dir / filename
        image_path.write_bytes(image_data)
        image_paths[filename] = quote(f"{document_stem}/{filename}", safe="/")

    referenced = set()

    def replace_reference(match):
        target = match.group(2)
        filename = Path(target.split("?", 1)[0]).name
        if filename not in image_paths:
            return match.group(0)
        referenced.add(filename)
        return f"{match.group(1)}{image_paths[filename]}{match.group(3)}"

    markdown = re.sub(r"(!\[[^\]]*\]\()([^)]*?)(\))", replace_reference, markdown)
    missing = [
        f"![{filename}]({image_paths[filename]})"
        for filename in image_paths
        if filename not in referenced
    ]
    if missing:
        markdown = markdown.rstrip() + "\n\n" + "\n".join(missing) + "\n"
    return markdown


def poll_result(file_path: Path, check_url: str) -> tuple[Path, str | None, list[tuple[str, bytes]], str | None]:
    for _ in range(MAX_POLLS):
        try:
            response = requests.get(check_url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            status = response.json()
            if status.get("status") == "complete":
                markdown = status.get("markdown") or ""
                if not markdown:
                    return file_path, None, [], f"API returned empty markdown. Full response: {status}"
                return file_path, markdown, extract_images(status), None
            elif status.get("status") == "failed":
                return file_path, None, [], status.get("error", "Unknown error")
        except Exception as e:
            return file_path, None, [], str(e)
        time.sleep(POLL_INTERVAL)
    return file_path, None, [], "Timed out waiting for result"


def convert_file(file_path: Path, output_dir: Path, overwrite: bool = False) -> bool:
    out_file = output_dir / (file_path.stem + ".md")
    if out_file.exists() and not overwrite:
        print(f"  skip  {file_path.name} (already converted)")
        return True

    print(f"  submit  {file_path.name}")
    time.sleep(SUBMIT_DELAY)
    file_path, check_url, error = submit_file(file_path)
    if error:
        print(f"  ERROR  {file_path.name}: {error}")
        return False

    file_path, markdown, images, error = poll_result(file_path, check_url)
    if error:
        print(f"  ERROR  {file_path.name}: {error}")
        return False

    markdown = add_image_references(markdown, images, output_dir, file_path.stem)
    out_file.write_text(markdown, encoding="utf-8")
    print(f"  done   {file_path.name} -> {out_file.name} ({len(images)} images)")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    input_dir = args.input_dir or script_dir / "input"
    output_dir = args.output_dir or script_dir / "markdown"
    output_dir.mkdir(exist_ok=True)

    files = args.files or [f for f in input_dir.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]
    files = [f if f.is_absolute() else input_dir / f for f in files]
    print(f"Found {len(files)} files to convert\n")

    success = 0
    failed = 0

    for f in files:
        if convert_file(f, output_dir, args.overwrite):
            success += 1
        else:
            failed += 1

    print(f"\nDone: {success} converted, {failed} failed")


if __name__ == "__main__":
    main()
