---
title: Konvertering og metadata (Mermaid)
---

## Prosess for konvertering og metadata

To make input documents more AI friendly it is usefull to convert input documents fraom DOCX, PDF etc to markdown. It can also be useful when maintaining a source repository containing a large document base to include some metadata about provenance of the different documents in the repo. This prosess describe one way to convert requested source documents to Markdown with a script using Datalab converter or Datalab API, retain extracted images in a separate folder for each output Markdown file, and add schema-compliant metadata as frontmatter.

```mermaid
flowchart LR
    actor["Business Actor<br/>Kildedokumentets opphav / utgiver"]
    source["Business Object<br/>Kildedokumenter<br/>PDF, DOCX, HTML m.m."]
    schema["Business Object<br/>Metadata-skjema<br/>metadata-schema.md + .json"]
    scope["Business Process<br/>Finn kilder / last ned"]
    convert["Business Process<br/>Konverter kildedokumenter"]
    metadata["Business Process<br/>Registrer metadata og valider"]
    quality["Business Process<br/>Kvalitetssikre metadata og Markdown"]
    datalab(["Business Service<br/>Datalab API"])
    output["Business Object<br/>Konvertert filoutput<br/>Markdown, ekstraherte bilder og metadata"]

    actor -. "utgir / leverer" .-> source
    scope --> convert --> metadata --> quality
    source -. "kilde" .-> convert
    schema -. "følger skjema" .-> metadata
    datalab -. "betjener" .-> convert
    convert -. "genererer" .-> output
    metadata -. "beriker" .-> output
    quality -. "kontrollerer" .-> output

    classDef business fill:#ffff99,color:#333333,stroke:#666666;
    class actor,source,schema,scope,convert,metadata,quality,datalab,output business;
```
