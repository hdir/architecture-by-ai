# Metadatamodell for kildedokumenter

Dette er en kort metadata-modell for kildedokumenter i `background/*/markdown`. Bare Markdown-filer i disse katalogene omfattes. Modellen skal gjøre dokumentene søkbare, sammenlignbare og egnet som underlag for analyse og andre oppgaver.

Maskinlesbar valideringsvariant i JSON Schema Draft 2020-12: [metadata-schema.json](metadata-schema.json).

## Prinsipper

- Metadata beskriver dokumentet, ikke sannhetsverdien i påstandene i dokumentet.
- Bruk kontrollerte verdier der det er praktisk mulig, men behold `notes` for tvilstilfeller.
- Skill mellom agentene som har utarbeidet dokumentet (`creator`), bidratt til eller sendt det (`contributor`) og publisert eller utstedt det (`publisher`). Samme agent kan ha flere roller.
- Skill mellom dokumentets tilgangsnivå og om det faktisk er publisert på nett.
- `Agent` beskriver aktørens identitet. Roller knyttet til en bestemt aktivitet registreres på agentdeltakelsen i `provenance`, ikke på agentidentiteten.
- `provenance` beskriver kjente aktiviteter som har generert eller endret Markdown-dokumentet. Hver oppføring gjelder én aktivitet; målet er Markdown-dokumentet selv.
- Flere verdier er tillatt for `information_categories`, `topics`, `creator` og `contributor`.

## Metadatafelt

| Felt | Type | Påkrevd | Beskrivelse og bruk |
| --- | --- | --- | --- |
| `id` | string | Ja | Stabil lokal identifikator. Anbefalt format: `DF-0001` eller annen prosjektintern ID. |
| `title` | string | Ja | Dokumentets tittel slik den fremgår av kilden. |
| `alternative_title` | string | Nei | Kortnavn, undertittel, rapportserie eller originaltittel på annet språk. |
| `document_type` | enum | Ja | Dokumentets hovedtype, se vokabular nedenfor. |
| `information_categories` | enum[] | Ja | Hvilken type informasjon dokumentet inneholder. Minst én verdi, flere ved behov. |
| `summary` | string | Nei | Kort, nøytral beskrivelse av innhold og formål. |
| `topics` | string[] | Nei | Søkeord eller kontrollerte emneord, for eksempel `digital helse`, `samhandling`, `styring`. |
| `creator` | Agent[] | Ja | Person(er) eller organisasjon(er) som har utarbeidet innholdet. Tilsvarer dokumentets `dc:creator`, ikke i seg selv en aktivitet. |
| `contributor` | Agent[] | Nei | Andre bidragsytere, høringsparter, oppdragsgiver eller godkjennende instans. Tilsvarer dokumentets `dc:contributor`. |
| `publisher` | Agent | Nei | Organisasjon som publiserte eller utstedte dokumentet. Tilsvarer dokumentets `dc:publisher`. |
| `publication_date` | date | Nei | Første publiserings- eller utstedelsesdato, ISO 8601 (`YYYY-MM-DD`). Bruk første dag i måneden bare når kilden oppgir måned og år. |
| `modified_date` | date | Nei | Siste faglige eller redaksjonelle endring, dersom kjent. |
| `language` | enum | Ja | Språk, normalt `nb`, `nn`, `no`, `en` eller `mul` (flere språk). |
| `access_level` | enum | Ja | Tilgangsbegrensning, se vokabular. |
| `web_published` | boolean | Ja | `true` når dokumentet er publisert på et åpent nettsted. Dette kan være `false` selv om dokumentet er åpent tilgjengelig på annen måte. |
| `source` | Source | Nei | Kildested, URL, arkiv eller annen sporbar opprinnelse. |
| `original_document` | OriginalDocument | Nei | Proveniens for den nedlastede originalen eller den direkte webkilden som Markdown-filen er basert på. |
| `provenance` | Provenance[] | Nei | Kjente aktiviteter som genererte eller endret Markdown-dokumentet, med tilhørende agenter og kildeentiteter. |
| `normative_level` | enum | Ja | Dokumentets normerende status, eller `none` når det ikke har en slik status. |
| `status` | enum | Ja | Dokumentets livsløp: `current`, `superseded`, `draft`, `historical` eller `unknown`. |
| `version` | string | Nei | Versjonsnummer, revisjon eller utgave slik kilden oppgir det. |
| `related_documents` | string[] | Nei | ID-er til relaterte, overordnede, underordnede eller erstattede dokumenter. |
| `metadata_confidence` | enum | Ja | `high`, `medium` eller `low`, basert på hvor tydelig metadata kan dokumenteres i kilden. |
| `notes` | string | Nei | Forbehold, tolkinger, manglende opplysninger eller annen forvaltningsinformasjon. |

### Agent

`Agent` beskriver en aktøridentitet og tilsvarer aktøren som refereres av FHIR `Provenance.agent.who`.

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `name` | string | Ja | Navn på person, organisasjon eller annen aktør. |
| `agent_type` | enum | Ja | `person`, `organization`, `group`, `device`, `software`, `patient`, `practitioner_role`, `care_team`, `related_person`, `public_body`, `company`, `unknown`. `public_body` og `company` er lokale presiseringer av `organization`. |
| `identifier` | string | Nei | Stabil lokal ID eller ekstern identifikator, helst URI når tilgjengelig. |
| `affiliation` | string | Nei | Beskrivende organisatorisk tilknytning. Dette er ikke det samme som FHIR `agent.onBehalfOf`, som registreres på en bestemt agentdeltakelse. |

### Source

`Source` er et objekt med:

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `url` | URI | Nei | URL til publisert dokument eller landingsside. |
| `retrieved_date` | date | Nei | Dato dokumentet eller URL-en ble hentet, ISO 8601. |
| `source_name` | string | Nei | Navn på nettsted, arkiv, journal eller samling. |
| `source_identifier` | string | Nei | Rapportnummer, journalnummer, DOI eller annen ekstern identifikator. |

### OriginalDocument

`OriginalDocument` beskriver dokumentet som ble konvertert eller lastet ned, ikke kilder som bare er referert i dokumentteksten.

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `id` | string | Nei | Stabil ID for originalentiteten, brukt av `provenance.entity.what` når den refererer til dette dokumentet. |
| `local_path` | path | Nei | Relativ sti til originalfilen under `background`, for eksempel `annet/input/rapport.pdf`. |
| `format` | enum | Ja når objektet finnes | Originalformat: `pdf`, `docx`, `html`, `csv`, `md` eller `other`. |
| `online_url` | URI | Nei | Canonical URL til originaldokumentet eller den offisielle landingssiden. |
| `online_status` | enum | Ja når objektet finnes | `verified`, `candidate`, `not_found`, `not_checked` eller `not_applicable`. |
| `retrieved_date` | date | Nei | Dato originalen eller URL-en ble hentet, ISO 8601. |

### Provenance

`Provenance` følger kjernemønsteret i FHIR R5 `Provenance`: én oppføring beskriver én aktivitet, agentene som deltok, og eventuelle entiteter aktiviteten brukte. `target` er implisitt Markdown-filen som metadataene står i. Bruk flere oppføringer dersom flere aktiviteter skal dokumenteres.

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `activity` | CodeableConcept | Ja | Aktiviteten som fant sted; tilsvarer FHIR `Provenance.activity`. |
| `occurred` | date-time eller Period | Nei | Når aktiviteten fant sted; tilsvarer FHIR `Provenance.occurred[x]`. |
| `recorded` | date-time | Nei | Når proveniensopplysningen ble registrert; tilsvarer FHIR `Provenance.recorded`. |
| `agent` | AgentParticipation[] | Ja | Minst én agent som deltok i aktiviteten; tilsvarer FHIR `Provenance.agent`. |
| `entity` | ProvenanceEntity[] | Nei | Entiteter aktiviteten brukte, for eksempel originaldokumentet; tilsvarer FHIR `Provenance.entity`. |

`CodeableConcept` er et objekt med:

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `coding` | Coding[] | Nei | Kodede verdier. Oppgi minst én kode når konseptet har en kjent kode. |
| `text` | string | Nei | Menneskelesbar tekst når en kodet verdi ikke finnes eller trenger forklaring. |

`Coding` er et objekt med:

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `system` | URI | Nei | Kodesystemets URI. |
| `code` | string | Nei | Kode i kodesystemet. |
| `display` | string | Nei | Menneskelesbar betegnelse for koden. |

`AgentParticipation` er et objekt med:

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `who` | Agent | Ja | Aktøren som deltok; tilsvarer FHIR `Provenance.agent.who`. |
| `type` | CodeableConcept | Nei | Hvordan agenten deltok, for eksempel `author` eller `assembler`; tilsvarer FHIR `Provenance.agent.type`. |
| `role` | CodeableConcept[] | Nei | Agentens funksjonelle rolle i akkurat denne aktiviteten; tilsvarer FHIR `Provenance.agent.role`. |
| `on_behalf_of` | Agent | Nei | Agenten som deltakeren handlet på vegne av i denne aktiviteten; tilsvarer FHIR `Provenance.agent.onBehalfOf`. |

`ProvenanceEntity` er et objekt med:

| Felt | Type | Påkrevd | Beskrivelse |
| --- | --- | --- | --- |
| `role` | enum | Ja | Hvordan entiteten ble brukt: `revision`, `quotation`, `source`, `instantiates` eller `removal`; tilsvarer FHIR `Provenance.entity.role`. |
| `what` | string | Ja | Stabil ID eller URI for entiteten; tilsvarer FHIR `Provenance.entity.what`. Bruk `original_document.id` når entiteten er originaldokumentet. |
| `agent` | AgentParticipation[] | Nei | Agenter som entiteten tilskrives; tilsvarer FHIR `Provenance.entity.agent`. |

Registrer bare en Provenance-oppføring når aktiviteten og minst én deltakende agent kan identifiseres. Ikke utled en aktivitet eller agent fra `creator`, `publisher` eller `publication_date` alene.

## Kontrollerte vokabularer

### `document_type`

`report`, `directive_or_assignment`, `strategy_or_plan`, `analysis_or_evaluation`, `legal_assessment`, `guidance`, `standard_or_requirement`, `consultation_response`, `submission_or_feedback`, `research_publication`, `presentation_or_note`, `summary`, `other`.

Velg dokumentets primære form. Et høringsinnspill som også inneholder analyse registreres som `submission_or_feedback`, mens analyseinnholdet registreres i `information_categories`.

### `information_categories`

`descriptive`, `empirical_evidence`, `stakeholder_view`, `problem_or_challenge`, `need_or_requirement`, `goal_or_outcome`, `proposal_or_measure`, `recommendation`, `decision_or_mandate`, `legal_or_regulatory`, `technical_or_architectural`, `organizational_or_governance`, `economic_or_financial`, `risk_or_security`, `privacy_or_data_protection`, `implementation_or_operations`, `evaluation_or_effects`, `research_or_method`, `definitions_or_terminology`, `other`.

### `access_level`

- `web_published`: publisert på åpent nettsted.
- `open`: ikke nødvendigvis webpublisert, men kan gis til alle uten særskilt tilgangsvurdering.
- `restricted`: tilgang begrenses av organisasjon, sak, avtale eller annen hjemmel.
- `secret`: sikkerhetsgradert eller på annen måte strengt hemmeligholdt.

`web_published` er en egen boolsk verdi fordi et dokument kan være webpublisert, men likevel ha vedlegg eller deler med begrenset tilgang. Registrer den strengeste kjente tilgangen i `access_level` og forklar avvik i `notes`.

### `normative_level`

`none`, `descriptive`, `advisory`, `guideline`, `recommended_standard`, `mandatory_standard`, `legal_or_regulatory`, `formal_decision`.

Verdiene uttrykker dokumentets status, ikke hvor overbevisende eller faglig godt innholdet vurderes. Bruk `advisory` for råd eller anbefalinger uten formell normeringsstatus, `guideline` for retningslinjer/veiledere, `recommended_standard` for anbefalt standard og `mandatory_standard` for bindende standard. Bruk `legal_or_regulatory` for lov, forskrift eller tilsvarende bindende regelverk.

## Valideringsregler

1. Alle påkrevde felt skal være utfylt. `id` skal være unik.
2. `title`, `document_type`, `information_categories`, `creator`, `language`, `access_level`, `web_published`, `normative_level`, `status` og `metadata_confidence` skal ikke være tomme.
3. Metadata skal bare registreres for `.md`-filer under `background/*/markdown`; filer i `input`, `output`, `old` og `html` skal ikke registreres som kildedokumenter.
4. Datoer skal være gyldige ISO 8601-datoer. `modified_date` skal ikke være tidligere enn `publication_date` når begge finnes.
5. `web_published: true` krever normalt `access_level: web_published`; avvik skal begrunnes i `notes`.
6. `source.url` skal være en absolutt `http`- eller `https`-URI når den finnes.
7. `original_document.local_path` skal, når den finnes, peke til en eksisterende fil under `background`.
8. `original_document.online_url` skal være en absolutt `http`- eller `https`-URI når den finnes. `online_status: verified` krever `online_url`.
9. En agent skal registreres med `agent_type: unknown` bare når kilden ikke gir rimelig grunnlag for identifikasjon. Ikke gjett person eller organisasjon.
10. Påstander om normativ status skal kunne spores til dokumentet eller en oppgitt kilde. Bruk `metadata_confidence: low` når statusen er tolket.
11. Hver `provenance`-oppføring skal ha `activity` og minst én `agent` med `who`.
12. `provenance[].recorded` og `provenance[].occurred` skal, når de er dato/tid, være gyldige ISO 8601-verdier. For `occurred` som periode skal slutten ikke være før starten.
13. Hver `provenance[].entity[].what` skal peke til en identifiserbar entitet. Når den viser til `original_document`, skal `original_document.id` være utfylt.

## Anbefalt front matter

```yaml
id: DF-0001
title: "Eksempel på dokumenttittel"
document_type: guidance
information_categories:
  - recommendation
  - technical_or_architectural
summary: "Kort, nøytral beskrivelse av dokumentets innhold."
topics:
  - digital helse
creator:
  - name: "Direktoratet for e-helse"
    agent_type: public_body
publisher:
  name: "Direktoratet for e-helse"
  agent_type: public_body
publication_date: 2019-06-15
modified_date: 2023-06-15
language: nb
access_level: web_published
web_published: true
source:
  url: "https://example.org/dokument"
  retrieved_date: 2026-09-18
  source_name: "Eksempelnettsted"
  source_identifier: "PUB-123"
original_document:
  id: "ORIG-DF-0001"
  local_path: "annet/input/eksempel.pdf"
  format: pdf
  online_url: "https://example.org/dokument"
  online_status: verified
  retrieved_date: 2026-09-18
provenance:
  - activity:
      coding:
        - system: "https://example.org/codes/activity"
          code: conversion
          display: "PDF til Markdown-konvertering"
    occurred: "2026-09-18T10:30:00Z"
    recorded: "2026-09-18T10:35:00Z"
    agent:
      - who:
          name: "Markdown-konverterer"
          agent_type: software
          identifier: "https://example.org/tools/converter"
        type: assembler
        role:
          - coding:
              - system: "https://example.org/codes/agent-role"
                code: converter
    entity:
      - role: source
        what: "ORIG-DF-0001"
normative_level: advisory
status: current
version: "1.1"
related_documents: []
metadata_confidence: high
notes: ""
```

## Standardmapping

Creator, contributor og publisher er metadata om dokumentet og beholdes som
separate felt. De blir ikke automatisk til en FHIR Provenance-aktivitet. Når
en proveniensoppføring finnes, mappe den slik:

| Modellfelt | FHIR R5 Provenance |
| --- | --- |
| Markdown-filen med metadataene | `target` |
| `provenance[].activity` | `activity` |
| `provenance[].occurred` | `occurred[x]` |
| `provenance[].recorded` | `recorded` |
| `provenance[].agent[].who` | `agent.who` |
| `provenance[].agent[].type` | `agent.type` |
| `provenance[].agent[].role` | `agent.role` |
| `provenance[].agent[].on_behalf_of` | `agent.onBehalfOf` |
| `provenance[].entity[].role` | `entity.role` |
| `provenance[].entity[].what` | `entity.what` |
| `provenance[].entity[].agent` | `entity.agent` |
| `original_document` | Kildeentitet referert fra `entity.what`, vanligvis med `entity.role: source` |

FHIR `Provenance` krever minst én `target` og én agent med `who`. I denne
modellen er målet implisitt den aktuelle Markdown-filen, mens hver oppføring
krever minst én agentdeltakelse. Ved eksport må lokale ID-er og identiteter
oversettes til entydige FHIR-referanser. Dette er en praktisk delmodell, ikke
en full FHIR-ressurs.

### Dublin Core-mapping

| Modellfelt | Dublin Core |
| --- | --- |
| `title`, `alternative_title` | `dc:title`, `dc:alternative` |
| `creator` | `dc:creator` |
| `contributor` | `dc:contributor` |
| `publisher` | `dc:publisher` |
| `publication_date`, `modified_date` | `dc:date` / `dcterms:modified` |
| `summary`, `topics`, `language` | `dc:description`, `dc:subject`, `dc:language` |
| `source` | `dc:source`, `dc:identifier` |
| `document_type` | `dc:type` |
| `access_level` | `dc:rights` |
| `related_documents` | `dc:relation` |

Felt som `information_categories`, `normative_level`, `web_published`, `status` og `metadata_confidence` er prosjektspesifikke utvidelser. `provenance` følger FHIR R5-mønsteret, men er en avgrenset lokal modell og ikke en full FHIR-ressurs.
