---
name: konvertering-og-metadata
description: "Use when converting one or more source documents to Markdown with this repository's Datalab API converter, including selecting input and output paths, extracting images into a per-document folder, and adding YAML metadata using .llm/data/metadata-schema.md and .llm/data/metadata-schema.json. Also use to validate conversion results, image links, and metadata."
---

# Dokumentkonvertering og metadata

Convert requested source documents to Markdown with the repository's existing Datalab converter, retain extracted images in a separate folder for each output Markdown file, and add schema-compliant metadata where the schema allows it.

## Boundaries and safety

- Use the Datalab API only when requested or clearly authorized. Source documents are uploaded to an external service. If a document is marked restricted or secret, or appears to contain sensitive personal or security information, confirm that cloud processing is authorized before upload.
- Never put an API key in this skill, source code, generated Markdown, logs, or command-line arguments. Read it from `DATALAB_API_KEY`. Do not print or echo the value. If it is missing, ask the user to set it in their terminal; do not request secrets through a chat question.
- Some repository scripts may have a fallback key. Do not rely on it: require a non-empty `DATALAB_API_KEY` in the process that runs the converter.
- Do not overwrite existing Markdown or images unless the user requested reconversion or explicitly approved replacement. Inspect existing outputs first and preserve unrelated files.
- Do not invent document facts, publication details, URLs, dates, parties, or normative status. Leave optional fields out when unknown. Use `unknown` only where the schema permits it and the source provides no reasonable basis for identification.

## Workflow

1. Identify the requested source file or collection, output directory, and whether existing results may be replaced. Resolve relative paths from the workspace root and verify each input exists.
2. Read `.llm/data/metadata-schema.md` and `.llm/data/metadata-schema.json`, then inspect the relevant `convert_to_markdown.py` before running it. Check the script's supported formats, argument syntax, default paths, overwrite behavior, image extraction behavior, and environment-variable handling. Prefer the converter closest to the requested input/output area when multiple scripts exist. Do not assume different scripts have the same CLI.
3. If the script does not support the requested inputs, output path, or image extraction requirement, explain the mismatch and use only a compatible existing converter. Do not silently switch to a different API or disable image extraction.
4. For a single file, pass the exact source and requested output directory using that script's documented arguments. For a collection, pass only the requested files or directory; exclude temporary files and unsupported formats. Preserve the converter's sequential/rate-limit behavior. Set `DATALAB_API_KEY` only for the converter process when practical, and clear the temporary environment value afterward.
5. Confirm the converter completed successfully for each requested document. Do not report skipped or failed files as converted. If a requested output already existed and was skipped, report that and do not claim it was regenerated.
6. For every successful conversion, verify that the Markdown file exists and is non-empty. Check that extracted images are in a separate, document-specific subdirectory beneath the output directory, and that Markdown image links resolve to those files. Report the number of extracted images and any extraction warnings.
7. Add YAML front matter to each eligible Markdown file as described below. Preserve the converted body and any existing valid metadata. Do not produce duplicate YAML keys or add metadata to files outside the schema's scope.
8. Validate the front matter against `.llm/data/metadata-schema.json`. Also check the cross-field, uniqueness, filesystem, and provenance-reference rules in `.llm/data/metadata-schema.md`, which JSON Schema cannot fully enforce. Recheck that the Markdown body and image references remain intact after front matter is added.
9. Report the output Markdown paths, per-document image-folder paths and counts, metadata uncertainty, skipped/failed files, and any validation issues. Never include the API key in the report.

## Converter invocation

Inspect the selected script's `argparse` configuration before building the command. Repository scripts may accept a positional list of files, positional input/output directories, or named options such as `--file` and `--output-dir`. On Windows, invoke Python with the `py` launcher rather than assuming `python.exe` is on `PATH`.

For PowerShell on Windows, use the `py` launcher:

```powershell
$ErrorActionPreference = 'Stop'
try {
  $env:DATALAB_API_KEY = '<set locally; do not commit or print>'
  py 'src\convert_to_markdown.py' `
    'C:\Git\Digital-Forstelinje\background\annet\input\Nasjonal e-helsestrategi versjon 1.0-2025.pdf' `
    'C:\Git\Digital-Forstelinje\background\annet\input\Vedlegg 1 Helsenorge veikart.pdf' `
    --output-dir 'C:\Git\Digital-Forstelinje\background\annet\markdown'
  if ($LASTEXITCODE -ne 0) { throw "Converter exited with code $LASTEXITCODE" }
} finally {
  Remove-Item Env:DATALAB_API_KEY -ErrorAction SilentlyContinue
}
```

The converter accepts one or more source paths as positional arguments and uses `--output-dir` for the destination. Replace the example files and destination with the user's requested paths. Do not add `--overwrite` unless the user asked to reconvert or approved replacing existing output.

Do not paste a real key into this skill or save it in a workspace settings file. If a run fails, report the converter's safe error details without exposing request headers or credentials.

## Metadata rules

Use [`.llm/data/metadata-schema.md`](../../data/metadata-schema.md) for metadata scope, field semantics, controlled vocabularies, examples, and validation rules. Use [`.llm/data/metadata-schema.json`](../../data/metadata-schema.json) to validate the structure and machine-checkable constraints. Read both before creating or changing front matter; do not duplicate their field definitions or rules in this skill.

The Markdown specification includes guidance and checks not expressible in JSON Schema. Follow it alongside JSON Schema validation. If the two schema files disagree, report the discrepancy rather than inventing a resolution.

## Front matter shape

Follow the schema's recommended structure and omit optional fields when unknown. The example below is copied from `background/annet/markdown/Nasjonal e-helsestrategi versjon 1.0-2025.md`. It uses the new `Agent` structure. It has no `provenance` record because the file does not identify a specific activity that generated the Markdown target. Do not copy its document-specific values or reuse its ID.

```yaml
---
id: ANNET-029
title: "Nasjonal e-helsestrategi"
document_type: strategy_or_plan
information_categories:
  - goal_or_outcome
  - recommendation
  - technical_or_architectural
  - organizational_or_governance
creator:
  - name: "Helsedirektoratet"
    agent_type: public_body
contributor:
  - name: "Aktører og interessenter i helse- og omsorgssektoren"
    agent_type: group
summary: "Sektorstrategi som setter felles retning, prioriteringer og mål for digitalisering av helse- og omsorgstjenesten fram mot 2030."
topics:
  - e-helse
  - digitalisering
  - helsedata
  - samhandling
language: nb
access_level: web_published
web_published: true
source:
  url: "https://www.helsedirektoratet.no/digitalisering-og-e-helse/nasjonal-e-helsestrategi"
  retrieved_date: 2026-09-30
  source_name: "Helsedirektoratet"
original_document:
  local_path: "annet/input/Nasjonal e-helsestrategi versjon 1.0-2025.pdf"
  format: pdf
  online_url: "https://www.helsedirektoratet.no/digitalisering-og-e-helse/nasjonal-e-helsestrategi"
  online_status: verified
normative_level: advisory
status: current
version: "1.0 (2025; angitt i filnavnet)"
metadata_confidence: medium
notes: "Helsedirektoratet er oppgitt som fagmyndighet og koordinator; aktører og interessenter er oppgitt som deltakere i strategiarbeidet. Konvertert dokumenttekst angir ikke eksplisitt publiseringsdato."
---
```
