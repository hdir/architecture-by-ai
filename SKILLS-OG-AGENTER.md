# Skills og spesialistagenter

Dette prosjektet bruker [Claude Code](https://claude.ai/code) med prosjektspesifikke skills og agenter for utredningsarbeid i norsk offentlig sektor.

## Skills

Skills gir Claude metoder og rammeverk som aktiveres automatisk basert på kontekst. De ligger i `.claude/skills/`.

### utredningsinstruksen

Aktiveres når du skal vurdere, evaluere eller foreslå tiltak. Inneholder de seks minimumskravene fra utredningsinstruksen (kongelig resolusjon 11. oktober 2024), forholdsmessighetsprinsippet, og nullalternativet.

**Når brukes den?** Ved analyse av tiltak, vurdering av alternativer, eller når du skriver beslutningsgrunnlag.

### klarsprak-offentlig

Aktiveres ved skriving eller gjennomgang av dokumenter for offentlig sektor. Basert på språkloven § 9 og Språkrådets retningslinjer, med fokus på aktiv form, viktigste-først, og unngå substantivsyke.

**Når brukes den?** Ved skriving av rapporter, anbefalinger eller kommunikasjon rettet mot beslutningstakere eller innbyggere.

### archimate-modellering

Aktiveres ved opprettelse av arkitekturdiagrammer. Mapper ArchiMate-konsepter til PlantUML (.puml) og Draw.io (.drawio) med fargekonvensjoner per lag (forretning=gul, applikasjon=blå, teknologi=grønn). PlantUML brukes for tekstbaserte/automatiserte diagrammer, Draw.io for komplekse/interaktive diagrammer.

**Når brukes den?** Når du skal lage arkitekturdiagrammer, visualisere systemlandskap eller modellere sammenhenger mellom lag.

## Agenter

Agenter er spesialiserte roller som kan kalles for spesifikke oppgaver. De ligger i `.claude/agents/`. Du kan referere til dem med `@agent-navn` i Claude Code.

### virksomhetsarkitekt

Helhetlig koordinator som vurderer problemstillinger på tvers av forretning, applikasjon og teknologi. Kan orkestrere de andre agentene for å bygge en komplett analyse. Ansvarlig for å generere navigerbar HTML-rapport i `rapporter/html/` som siste steg i en utredning.

**Bruk til:** Helhetsvurderinger, arkitekturanalyser, koordinert utredning, HTML-rapportgenerering.

### offentlig-utreder

Systematisk informasjonsinnsamler som bygger kunnskapsgrunnlag fra offentlige kilder (regjeringen.no, lovdata.no, EU-kilder, DFØ, SSB). Strukturerer funn etter utredningsinstruksens seks spørsmål.

**Bruk til:** Bakgrunnsarbeid, kildegjennomgang, bygge faktagrunnlag.

### samfunnsokonom

Vurderer tiltak etter DFØs veileder for samfunnsøkonomisk analyse. Identifiserer nytte og kostnader, fordelingsvirkninger og usikkerhet.

**Bruk til:** Kostnads-/nyttevurderinger, sammenligning av alternativer, vurdering av fordelingsvirkninger.

### helsepersonellombud

Talsmann for helsepersonells perspektiv. Vurderer hvordan løsninger påvirker klinisk arbeidshverdag, brukervennlighet og pasientsikkerhet.

**Bruk til:** Vurdere konsekvenser for helsepersonell, identifisere risiko for pasientsikkerhet, evaluere brukervennlighet.

### klarsprak-copywriter

Språklig kvalitetssikrer som omskriver tekst til klarspråk etter språkloven § 9. Returnerer forbedret tekst med begrunnelse for endringene. Kvalitetssikrer også HTML-rapporter for kontrast, konsistens og lenker.

**Bruk til:** Kvalitetssikring av rapporter og HTML, omskriving av tekst til klarspråk, tilpasning til målgruppe.

## Samspill mellom agentene

```
virksomhetsarkitekt (koordinator)
├── kaller offentlig-utreder → faktagrunnlag
├── kaller samfunnsokonom → kostnads-/nyttevurdering
├── kaller helsepersonellombud → klinisk perspektiv
└── sender resultat til klarsprak-copywriter → lesbar tekst
```

Virksomhetsarkitekten er den sentrale agenten som kan orkestrere de andre. Hver agent kan også kalles direkte for spesifikke oppgaver.

### Ferdigstillingsfase

Når en utredning er komplett, genererer virksomhetsarkitekten en navigerbar HTML-rapport i `rapporter/html/`. Klarspråk-copywriteren kvalitetssikrer HTML-rapporten for språk, kontrast og konsistens.

## Avgrensning mot CLAUDE.md

De tre lagene utfyller hverandre:

- **CLAUDE.md** styrer *hva* som skal gjøres i EHDS-prosjektet (mål, roller, rapportstruktur)
- **Skills** gir *metoder* (utredning, klarspråk, modellering)
- **Agenter** fyller *roller* som vurderer fra ulike perspektiver
