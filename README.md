# AI som verktøy for virksomhetsarkitektur

Repository for å teste hvordan Helsedirektoratet kan benytte AI som verktøy i sitt arbeid med virksomhetsarkitektur for helsesektoren. Repository fungerer som dokumentasjon av ulike måter vi kan ta i bruk AI for å understøtte arkitekturarbeidet.

## Eksempel

- [Skills og spesialistagenter](SKILLS-OG-AGENTER.md) – Oversikt over prosjektspesifikke skills og agenter for utredningsarbeid med Claude Code
- [Konvertere til markdown og legg til metadata](konvertering-og-metadata-prosess.md)
  - [script](src/convert_to_markdown.py)
  - [metadata skjema](.claude/data/metadata-schema.md)
  - [metadata og konvertering skill](.claude/skills/konvertering-og-metadata/SKILL.md)

## Use cases

Use-cases for AI innen arkitektur.

- Dataanalyse - av mange datakilder i henhold til problemstilinger som er viktig for å avklare mål og kapabiliter
- Visualisering av arkitekturartefakter for å vise sammenhenger som er vanskelig å få oversikt over som tekst, diagrammer og modeller, presentasjoner, prosessflyt og systemkart
- Sammenstilling og strukturering av informasjon - syntese av mange dokumenter, strukturere innspill, sammenstille status og gap
- Rollespill og perspektivtesting - djevelens advokat, opptre som interessent og scenariotesting av varianter og risikovurdering

```mermaid
mindmap
   ((Use-cases AI))
      Dataanalyse
         (Innsikt i data)
         (Hvordan henger data sammen)
      Visualisering
         (oversikt og sammenhenger)
         (mål, verdi, prosesser og roller)
         (presentasjon)
         (systemkart)
      Strukturering av informasjon
         (Oversikt over data)
         (syntese av mange dokumenter)
         (sammenstille status)
         (sammenstille gap)
```