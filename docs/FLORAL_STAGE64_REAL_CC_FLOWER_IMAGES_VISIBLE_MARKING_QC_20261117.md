# Stage64 — Actual openly licensed flower photographs: source verification, image eligibility and no false guide negatives

Date 2026-11-17 JST. **Status: original iNaturalist API source and actual eight medium images retrieved; one unblinded exploratory image reviewer identified two source photos with visible petal spots/lines. Not a measured multisensory selection effect, guide function or new species-level prevalence result.**

## Why real original images were required

Existing original Stage60 taxon-name photo review queue: 80 original VOC305 × FCP4475 exact binomial taxa, 55 with ≥40 original **coarse whole-flower-colour classifiable** images. FCP is a validated original four-colour classification programme, **not** a within-petal visible nectar-guide classifier; a species having many old FCP photos does not imply a new sample contains open flowers or resolved markings.

Four species were fixed from source original Stage60 before inspecting photos: `Dianthus deltoides` (iNat 76647, FCP classifiable 82), `D. barbatus` (60015, 71), `Helichrysum stoechas` (82641, 81), `Antirrhinum majus` (48969, 66). First two are NHM marking **textual candidates**, not verified positive; latter two are unlabeled photo opportunity comparators, **not confirmed negatives**.

This work then queried **new** source iNaturalist original research-grade noncultivated observations (official v1 observations API, up to first 50 by id), choosing at most one photo per observation/user and strictly CC0/CC-BY/CC-BY-SA original photo licenses. No original photo pixels downloaded in initial metadata stage; no GPS/observer names saved. **These are NOT the original FCP 100 photos per species** and cannot be called FCP source-image remeasurement.

### Actual source metadata and independently validated photo pixels

- Original source metadata [GitHub Actions run 44019626997](https://github.com/zuizui0223/adaptive-gain/actions/runs/44019626997) **SUCCESS**, original artifact **14300990223**, SHA256 `aded5ca91862059804193a9ed15ea4fe45723a6aeac8c1ba5741e2b5f6aef7e7fcc8e444924332a58d9ef6bbb1`. Source record metadata: **17** original CC licence/photo-ID candidates across four species: 5 D. deltoides, 4 D. barbatus, 5 Helichrysum and 3 Antirrhinum. These are license- and observer-qualified photo IDs, not flower-positive. No failed original API calls remain.
- Official iNaturalistAPI confirms that an original `/square.jpg` photo URL can be transformed to the **same original photo ID** `/medium.jpg`; the 500px max variant maintains the original image's license and author. Source documentation: https://github.com/inaturalist/iNaturalistAPI/blob/main/lib/views/swagger_v1.yml.ejs.
- From **source ID only, before opening pixels**, a stable SHA-based identity selection chose two photos/taxon; CC-BY-SA excluded from contact-sheet adaptations, retained as valid source metadata. Read-only full pixels and CC-BY attribution were obtained in [CI 44019859643](https://github.com/zuizui0223/adaptive-gain/actions/runs/44019859643), **8 actual photo pixels across four source taxa, all 8 downloads successful**, artifact **14300222304**, ZIP SHA256 `e6c2c57ba8a04656320b581410f90f3830b867aacb8519d527d3bfbd66540d6a`. Contact sheet is accompanied by original photograph ID, attribution, license, original source observation URL and exact medium pixel SHA256. No unlicensed source photos rehosted.
- One assistant reviewer **unblinded to displayed names and captions** visually inspected the actual original CC image pixels. These are not double-scored independent botanical ratings, not an automatic UV/RGB classifier. Original source-vs-label SHA and photo-ID consistency checked independently by original [CI 44020202688](https://github.com/zuizui0223/adaptive-gain/actions/runs/44020202688) **SUCCESS**, five synthetic contract tests, final derived artifact **14301016030**, ZIP SHA256 `da7e14d733e38201d0de7987e317f2090a76e00fa8c21719f720b185d08f708c`.

### Original eight-photo independent quality observations

| Species | Source photo ID | Actual visual eligibility | Conservative observed label |
|---|---|---|---|
| D. deltoides | 763131994 | Open corolla, part detail visible | Pale spots and streaks on purple/pink petal interior **visible** |
| D. deltoides | 752917601 | Open corolla, part detail visible | White inner-petal spots/lines in magenta petals **visible** |
| D. barbatus | 761718545 | Vegetative foliage, no open flower | **unknown**, not unmarked flower |
| D. barbatus | 763028653 | Vegetative foliage, no open flower | **unknown** |
| H. stoechas | 763934945 | Dry inflorescence, no reviewable open corolla | **unknown** |
| H. stoechas | 762455029 | Yellow inflorescences visible, internal organ unresolved | **unknown** |
| A. majus | 760688061 | Flowers seen, petal detail too small to classify | **unknown** |
| A. majus | 762081546 | Vegetative leaves, no open flower | **unknown** |

**Actual source QA totals:** 8 independently authenticated photographed records; **2 photographs with visible intrapetal color marks** (both *same species* D. deltoides), **0 photograph-verified visually uniform petals**, **6 unknown/not-evaluable** (three vegetative, one dry inflorescence, two floral detail unresolved). These are SOURCE photo-level observations, not 2 independent evolved signal taxa or an estimated 25% frequency: source observers, license availability, species and selected photo frame are biased.

### What this does NOT show

- Visible white spots/lines are **not** confirmed reward guides, insect-attracting signals, UV nectar guides, nectar chemistry, receptor colour contrast or visual ecological adaptation. RGB alone cannot measure UV.
- A source photographed species may differ in locale, date, floral stage, cultivar/cultivation status and exact plant from the 2020 original VOC sample. The studied VOC emission of a species is not a chemical assay on these photographs.
- Multiple photos of one species do not make phylogenetically independent taxa. Images without open flowers cannot be classified as true species signal-negative; missingness is not a single-color phenotype.
- No weather at the exact photographed time, wind plume, Bombus realized visitation, pollen deposit, or plant fitness is linked. No SEM, selection gradient, new prior sensory-backup effect or stochastic cue-policy effect can be fitted from eight nonrandom sample photos.

## Scientifically identifiable next step

Use the iNaturalist **Flowers and Fruits = Flowers** official annotation filter (`term_id=12&term_value_id=13`) to *prospectively source* a potentially more reviewable photo sample. The tag indicates source plant observation annotated flowering; it does not certify that each particular photo shows an open, resolvable flower. Keep it distinct from previous unfiltered sample. Validate original source photo ID and license, exclude photos failing flower-specific anatomical review, and sample additional actual lineages with TRUE reviewable visible-negative controls (not fabricated negatives). At least two blinded reviewers should verify pixel-level organ/marking labels; only then estimate species-level floral visible patterns.

Read-only source code, image preview QA, eight source photo IDs/digests and metadata audit in `research/floral_routeability_stage64/` and three dedicated original-source workflows. **Do not merge; main remains untouched**.
