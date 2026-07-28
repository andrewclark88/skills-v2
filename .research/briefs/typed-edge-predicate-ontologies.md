---
id: typed-edge-predicate-ontologies
kind: research-brief
summary: ARD's twelve typed-edge predicates draw ten ancestors from CiTO, IBIS/Toulmin, and SKOS plus two substrate-native predicates coined because the established ontologies have no clean home for a design→implementation edge.
updated: 2026-06-04
source_handles:
  - cito-spec
  - cito-paper
  - ibis-kunz-rittel
  - toulmin-argument
  - skos-reference
---

# Which ontologies ground ARD's typed-edge predicate vocabulary

*Settled synthesis (2026-06-04), folding a three-facet research campaign
(CiTO · IBIS/Toulmin · SKOS) into a single brief. Process artifacts (decomposition rationale,
dispatch, verification checklist) are mined only for durable corrections they surfaced; the
analytical content lives in the per-tradition sections below and the evaluation.*

## The shape of the answer

ARD's `typed_edge_predicates` (SPEC §10.5 / CATALOGS §9; vendored as
`plugins/agentic-research/scripts/catalogs.json`) declares a `source_ancestor` for each
predicate, naming CiTO, IBIS/Toulmin, and SKOS plus "substrate-native." The twelve predicates
partition into **ten with a named external ancestor** and **two substrate-native** — and,
crucially, "substrate-native" does *not* uniformly mean "no ancestor":

| Predicate | `source_ancestor` (verbatim, catalogs.json) | Tradition |
|---|---|---|
| `cites` | CiTO cito:cites | CiTO |
| `citesAsEvidence` | CiTO cito:citesAsEvidence | CiTO |
| `extends` | CiTO cito:extends | CiTO |
| `refutes` | CiTO cito:refutes | CiTO |
| `usesMethodIn` | CiTO cito:usesMethodIn | CiTO |
| `obtainsBackgroundFrom` | CiTO cito:obtainsBackgroundFrom | CiTO |
| `grounds` | Toulmin (data → claim) | Toulmin |
| `supports` | IBIS argument-to-position; CiTO cito:supports | IBIS + CiTO |
| `objects-to` | IBIS argument-to-position; CiTO cito:critiques/disputes | IBIS + CiTO |
| `related` | SKOS skos:related | SKOS |
| `implements` | Substrate-native (no clean ontology ancestor) | substrate-native |
| `contrasts` | Substrate-native (partial CiTO citesAsRelated) | substrate-native |

So: **10 inherited** (6 pure-CiTO, 1 Toulmin, 2 IBIS+CiTO dual, 1 SKOS) + **2 substrate-native**.
Of the two substrate-native, only `implements` has *no* ancestor; `contrasts` is substrate-native
but the catalog records a *partial* echo of CiTO `citesAsRelated`. Each tradition contributes a
*different kind* of relation, and they are complementary except at one seam (below).

## CiTO — citation typing (citation-stance predicates)

CiTO (Citation Typing Ontology) is an OWL 2 DL ontology whose stated purpose is to enable
"characterization of the nature or type of citations, both factually and rhetorically"
[cito-spec]{1}. Its founding motivation is that conventional citation lists are opaque: a bare
reference reveals nothing about *why* the cited work is cited [cito-paper]{4}. The ontology's
organising primitive is a **factual/rhetorical axis** (what a source *supplies* vs. how it is
*positioned*), realised as a sub-property hierarchy under a top-level `cites`, so any typed edge
also entails bare `cites` [cito-spec]{14}.

CiTO grounds six pure-CiTO predicates in ARD: `cites` (the untyped fallback, since all other
predicates are sub-properties and thus entail it) [cito-spec]{2}; `citesAsEvidence`
[fact-of-evidence] [cito-spec]{3}; `extends` [intellectual extension] [cito-spec]{4}; `refutes`
[rebuttal stance] [cito-spec]{5}; `usesMethodIn` [methodological reuse] [cito-spec]{7}; and
`obtainsBackgroundFrom` [context-setting] [cito-spec]{8}. Each inherits the factual/rhetorical
axis directly from CiTO's design [cito-spec]{1}. The ontology's full vocabulary is far larger —
CiTO version 2.8.1 (2018-02-16) defines 70+ named citation relationship properties
[cito-spec]{14}, against the 23 documented in the 2010 founding paper [cito-paper]{2} — so ARD's
selection is a principled subset, not the whole vocabulary.

**Disconfirming analysis (CiTO facet).** No disconfirming evidence was found that undermines
CiTO as a suitable *grounding* ontology for the inherited predicates. The one gap is real but
narrow: CiTO is **citation-centric** — every predicate assumes a citing/cited *document* pair
[cito-spec]{1}, so it has no predicate for a non-bibliographic edge such as a work-item
realizing a design. ARD also lacks inverse-predicate and confidence/temporal semantics; CiTO
itself supplies inverses (e.g. `isCitedAsEvidenceBy`) [cito-spec]{14} but is atemporal, so the
attestation layer must add the temporal/confidence dimension.

## IBIS + Toulmin — argumentation (deliberative + evidential predicates)

**IBIS (Kunz & Rittel 1970)** grounds the bipolar argument axis — `supports` and `objects-to`
(each dual-ancestried with CiTO; see the seam below). IBIS defines a small closed ontology of
Issue / Position / Argument node types with a governed link grammar in which "Pros (arguments
for) or Cons (arguments against)" attach arguments to positions [ibis-kunz-rittel]{5}, with "no
third pole" — every argument is for or against. The link grammar constrains argumentation to
positions: "Arguments can only associate with ideas" [ibis-kunz-rittel]{6}.

**Toulmin's *Uses of Argument* (1958)** grounds `grounds` — the data→claim relationship in which
evidence is the basis a conclusion rests on, its relevance licensed by a warrant that "links
data and other grounds to a claim, legitimizing the claim by showing the grounds to be relevant"
[toulmin-argument]{1}. ARD encodes no separate `warrant` predicate; the warrant is discharged in
artifact prose — the `grounds` edge asserts the evidential link, the body justifies it. The
Toulmin model's six elements (Claim, Grounds, Warrant, Backing, Qualifier, Rebuttal) are well
established in rhetoric, communication, and computer science [toulmin-argument]{6}; the 1958,
1969, and 2003 editions are the same work [toulmin-argument]{11}.

**Disconfirming analysis (IBIS/Toulmin facet).** Could `grounds` be from IBIS rather than
Toulmin? IBIS defines no evidential "grounds" predicate — its arguments are Pro/Con, asserting
for or against a position without distinguishing evidential basis from inferential move
[ibis-kunz-rittel]{5}; Toulmin's grounds is the correct ancestor. Could `supports` / `objects-to`
derive entirely from CiTO rather than IBIS? CiTO does define `cito:supports` and
`cito:critiques`/`cito:disputes` [cito-spec]{6}, but CiTO's design intent is citation stance
between *documents*; IBIS supplies the deliberative-stance semantics. The catalog records dual
ancestry for both — neither alone is sufficient. **Limitation:** both attestations rest partly
on **secondary** sources (the Kunz-Rittel 1970 primary and the Toulmin 1958 monograph were not
web-fetchable; claims are cite-through via reputable secondaries).

## SKOS — knowledge organization (associative predicate)

SKOS (W3C Recommendation) is a common RDF/OWL data model for knowledge organization systems.
`skos:related` asserts an associative link between concepts — "two concepts are inherently
'related', but that one is not in any way more general than the other" [skos-reference]{2}.
SKOS grounds ARD's `related` predicate on three load-bearing dimensions:

- **Symmetry** — `skos:related` is an instance of `owl:SymmetricProperty` (S23): if `<A>
  skos:related <B>`, the triple `<B> skos:related <A>` is entailed [skos-reference]{4}. This is
  why `related` is ARD's *only* symmetric predicate — it inherits SKOS's associative-symmetric
  shape directly.
- **Non-transitivity** — explicitly *not* transitive [skos-reference]{7}; each associative link
  is a point-to-point assertion, no implied chains.
- **Disjoint from hierarchical relations** — formally declared disjoint with
  `skos:broaderTransitive` (S27) [skos-reference]{6}, enforcing the associative/hierarchical
  distinction.

**Disconfirming analysis (SKOS facet).** Could `skos:related` be asymmetric in practice? The
symmetry is a formal OWL entailment, not a guideline; any SKOS-conformant reasoner derives the
inverse triple [skos-reference]{4}. Not disconfirmed. SKOS over-specifies compared to ARD's
substrate-level use (the formal disjointness condition S27 needs OWL reasoning, which ARD does
not run), but that is a scope difference, not a contradiction.

## The one seam — dual ancestry of `supports` / `objects-to`

`catalogs.json` records **dual ancestry** for `supports` and `objects-to` (IBIS *and* CiTO
`cito:supports` / `cito:critiques`). The IBIS/Toulmin facet examined this directly; it is not a
contradiction but an *intersection*: IBIS supplies the **deliberative-stance** semantics (an
argument is for or against a *position* [ibis-kunz-rittel]{5}), while CiTO supplies the
**citation-stance** semantics (a citing document's rhetorical posture toward a *cited document*
[cito-spec]{6}). ARD relaxes IBIS's type constraint (arguments→positions only
[ibis-kunz-rittel]{6}) to any artifact pair while keeping the directional for/against semantics
— a substrate-design relaxation not grounded in any attestation. The seam is real and worth
recording: a reader tracing lineage finds two ancestors that agree on direction and polarity
but come from different worlds (scholarly citation vs. policy deliberation).

## Why ARD needed substrate-native predicates

The two substrate-native predicates — `implements` ("an implementation realizes a
design/decision") and `contrasts` ("an alternative without disagreement") — exist because each
named tradition is scoped to a world that does not cleanly contain these relations:

- **CiTO is citation-centric** — every predicate assumes a citing/cited *document* pair; it has
  no predicate for a non-bibliographic edge such as a work-item realizing a design
  [cito-spec]{1}. (CiTO's `citesAsRelated` is close enough that the catalog records it as a
  *partial* ancestor for `contrasts`, but not an exact one.)
- **IBIS and Toulmin are argumentation models** — for/against a position, evidence-for-a-claim;
  an *implementation-realizes-design* relation is neither an argument nor an evidential ground
  [ibis-kunz-rittel]{5} [toulmin-argument]{1}.
- **SKOS is associative and symmetric** — `implements` is directed and asymmetric, so
  `skos:related` cannot be its ancestor [skos-reference]{4}.

So the substrate-native predicates are not a research gap; they are a genuine extension ARD
coined because its substrate pairs *research* with *operational* work (`.work/` ↔ `.research/`),
and the established citation/argumentation/KOS ontologies have no clean home for a
design→implementation edge. That is the honest reason `source_ancestor` reads "Substrate-native
(no clean ontology ancestor)" for `implements` — and only a *partial* CiTO echo for `contrasts`.

## Disconfirming evidence

Searched for evidence that the named ancestors are *wrong* or *insufficient* for the predicates
they ground. None found at the predicate level: each inherited predicate's name and semantic
match its `source_ancestor`'s primary definition (CiTO property definitions [cito-spec]{1};
IBIS Pro/Con [ibis-kunz-rittel]{5}; Toulmin grounds→claim [toulmin-argument]{1};
`skos:related` symmetry/non-transitivity [skos-reference]{4}). The one thing the by-ontology
lens *would* have missed — the substrate-native predicates, and that `contrasts` (unlike
`implements`) retains a partial CiTO echo — is surfaced above rather than dropped. Two facets
rest partly on **secondary** sources (the Kunz-Rittel 1970 primary and the Toulmin 1958
monograph were not web-fetchable; claims are cite-through via reputable secondaries, disclosed
in those attestations as `reduced-substrate-attestation`).

## Contradictions

- **`supports` / `objects-to` dual ancestry** (IBIS vs. CiTO) — `tension`, not `contradicts`:
  resolved above as an intersection of deliberative- and citation-stance traditions; both
  ancestries are legitimately recorded in `catalogs.json`.
- No source-level contradictions were found *within* any tradition's sources. Apparent ones are
  edition/version evolution, not disagreement: CiTO documented 23 predicates in the 2010 paper
  [cito-paper]{2} and 70+ in the current spec [cito-spec]{14} (a superset over time); Toulmin's
  1958/1969/2003 editions are the same work [toulmin-argument]{11}.

## Verification outcomes that changed the synthesis

The campaign's verification pass (adversarial-read → evaluate → revision) corrected two
provenance defects in the first draft, both reflected in the brief above:

1. **`contrasts` ancestor.** The first draft asserted both substrate-native predicates read "no
   clean ontology ancestor." Ground truth: `implements` does, but `contrasts` reads
   "Substrate-native (partial CiTO citesAsRelated)." Corrected above (and surfaced as a
   partial-ancestor gap, not erased).
2. **"Both specialists independently flagged" the dual ancestry.** Only the IBIS/Toulmin facet
   examined the `supports`/`objects-to` dual ancestry directly; the CiTO facet documents
   `cito:supports`/`critiques` purely as CiTO predicates. The seam section above attributes the
   dual-ancestry finding to the IBIS/Toulmin facet only, with the CiTO facet contributing the
   citation-stance side that the synthesis then composes.

A residual minor wrinkle (acknowledged, not blocking): the `ibis-kunz-rittel` attestation's
quotes are not perfectly self-consistent on whether arguments attach to "ideas" or "issues";
this brief follows the formal IBIS Pro/Con-attach-to-Positions grammar
[ibis-kunz-rittel]{5} [ibis-kunz-rittel]{6}.

## Revisit if

- ARD adds predicates drawing on further IBIS/Toulmin elements (e.g. a Toulmin `qualifier` → a
  hedge predicate), or extends predicates to non-bibliographic contexts at scale (re-examine
  the CiTO scope gap and the `contrasts`/`citesAsRelated` partial echo).
- The Kunz-Rittel 1970 primary becomes fetchable — verify the original predicate names against it.
- A future ARD release changes a `source_ancestor` (this synthesis pins the v0.4.x ARD release's
  `catalogs.json` lineage; the catalog's own `catalog_baseline` field reads `0.3`).
