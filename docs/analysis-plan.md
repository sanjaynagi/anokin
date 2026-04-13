# AnoKin Data Analysis Plan

## Context

AnoKin is a close-kin mark-recapture (CKMR) study of ~900 *Anopheles funestus* mosquitoes sampled from Lake Kanyaboli, Siaya County, Kenya. Samples were sequenced by SeqArt using DArTseq (a RADseq-like method). The genomic data (~1GB across 5 CSVs) uses an unusual multi-row header format specific to DArT genotyping platforms. Field metadata lives in ODK exports across several CSVs. The goal is to rigorously characterise the dataset, build a clean metadata sheet, and perform exploratory genomic analyses before proceeding to kinship/dispersal estimation.

---

## Step 1: Orient & Document (`docs/anokin-dataset.md`)

**Goal**: Create a persistent reference document describing the full dataset so future sessions can orient quickly.

**Contents**:
- Study overview (site, species, sampling design, dates)
- Description of each data file: path, format, dimensions, key columns
- DArTseq format explanation (multi-row headers, SilicoDArT vs SNP markers, mapping files)
- ODK data structure (household-level vs mosquito-level, barcode/ID linkage)
- Sample tracking: how SeqArt plate positions map to ODK barcodes
- Known quirks (tab-delimited .csv, hierarchical ODK field names, `*` placeholder headers)

**Key files to read**:
- `docs/seqart-method.md` — sequencing methodology
- `docs/anokin-sampling-protocol.md` — field protocol
- `data/seqart_sample_tracking_file.csv` — plate-to-barcode mapping
- Headers of all `Report_DMo25-3087_*.csv` files

**Deliverable**: `docs/anokin-dataset.md`

---

## Step 2: Deep-Dive into DArTseq Report Files

**Goal**: Fully characterise the genomic data format, dimensions, and quality.

**Tasks**:
1. Parse the multi-row header structure of each Report file:
   - `Report_DMo25-3087_SilicoDArT_1.csv` — presence/absence of restriction fragments (binary 1/0)
   - `Report_DMo25-3087_SNP_2.csv` — SNP genotypes (coded as 0/1/2 or similar)
   - `Report_DMo25-3087_SNP_3.csv` — additional SNP quality/count metrics
   - `Report_DMo25-3087_SNP_mapping_2.csv` — genomic positions of SNPs (chromosome, position, strand)
   - `Report_DMo25-3087_SNP_mapping_3.csv` — additional mapping metadata
2. Determine: number of samples, number of markers, genotype encoding, missingness rates (per sample and per marker)
3. Cross-reference sample IDs across files and with `seqart_sample_tracking_file.csv`
4. Document findings in `docs/anokin-dataset.md`

**Deliverable**: Updated `docs/anokin-dataset.md` with full format specification

---

## Step 3: Build Master Metadata Sheet

**Goal**: Merge ODK field data into a single, clean, sample-level metadata table.

**Input files**:
- `sampling/odk/ckmr_sampling.csv` — household-level data (GPS, building materials, date, collector)
- `sampling/odk/ckmr_morpho_id.csv` — morpho ID session-level (barcode, household-id, collector)
- `sampling/odk/ckmr_morpho_id-mosquito_data.csv` — individual mosquito data (species, sex, blood-fed status, sample_id)
- `sampling/odk/ckmr_uvlt.csv` — UV light trap collections
- `data/seqart_sample_tracking_file.csv` — plate position to barcode mapping

**Tasks**:
1. Parse each ODK file; understand the join keys (PARENT_KEY/KEY hierarchy, barcode, household-id)
2. Join mosquito-level data to household-level data (GPS, date, building type)
3. Join to SeqArt tracking file to link field barcodes → sequencing plate positions → genomic data columns
4. QC checks:
   - Missing GPS coordinates
   - Duplicate sample IDs / barcodes
   - Species mismatches (expect An. funestus; flag An. gambiae s.l.)
   - Date/collector inconsistencies
   - Samples in genomic data but not in ODK (and vice versa)
5. Output: `data/master_metadata.csv` — one row per mosquito, columns for all field + sequencing metadata

**Deliverable**: Notebook `notebooks/01_metadata.ipynb` + `data/master_metadata.csv`

---

## Step 4: Exploratory Genomic Analysis

**Goal**: QC the genomic data and look for biological signal (relatedness, spatial structure).

**Pixi environment setup** — create `pixi.toml` with:
- Python 3.11+
- pandas, numpy, scipy, matplotlib, seaborn, plotly
- scikit-learn (PCA, clustering)
- scikit-allel (if compatible) or custom parsing
- jupyter, openpyxl
- geopandas, shapely (spatial analyses)

**Notebook `notebooks/02_genomic_qc.ipynb`**:
1. Load and parse DArTseq data into usable matrices (samples × markers)
2. Per-sample QC: call rate / missingness, heterozygosity
3. Per-marker QC: call rate, minor allele frequency (MAF), HWE tests
4. Filter markers and samples by quality thresholds
5. Summary statistics and visualisations

**Notebook `notebooks/03_exploratory_analysis.ipynb`**:
1. PCA / MDS on filtered SNP data — look for population structure, outliers, batch effects
2. Pairwise genetic distance/relatedness matrix (e.g., IBS or kinship estimates)
3. Spatial analysis:
   - Map sample locations (GPS from metadata)
   - Correlate genetic distance vs geographic distance (isolation by distance)
   - Do closely related pairs cluster spatially?
4. Summary of findings: is there real signal? batch effects? contamination?

**Deliverables**: `notebooks/02_genomic_qc.ipynb`, `notebooks/03_exploratory_analysis.ipynb`, `pixi.toml`

---

---

## Step 5: Ginkgo Workflow & Allelic Dropout Mitigation

**Goal**: Formalise all analysis as a reproducible ginkgo workflow, and address allelic dropout before kinship inference.

**Tasks**:
1. Create `anokin/workflow.py` with a `@flow` defining the full DAG (notebooks 01–07 as `@task('notebook')` nodes)
2. Create `ginkgo.toml` project configuration (paths, thresholds, parameters)
3. **Notebook `notebooks/04_dropout_filtering.ipynb`**:
   - Per-locus F_IS filtering: remove markers with F_IS > 0.3 (most dropout-affected)
   - Explore read-depth information from SNP_mapping files to set depth-aware filters
   - Recalculate sample-level heterozygosity and call rates on cleaned marker set
   - Compare allele frequency spectra before/after dropout filtering
   - Output: `data/geno_dropout_filtered.csv` — stricter filtered genotype matrix

**Deliverables**: `anokin/workflow.py`, `ginkgo.toml`, `notebooks/04_dropout_filtering.ipynb`

---

## Step 6: Formal Kinship Inference (KING-robust)

**Goal**: Classify all pairwise relationships using a method robust to population structure and genotyping error.

**Notebook `notebooks/05_kinship_inference.ipynb`**:
1. Implement KING-robust kinship estimator on dropout-filtered genotypes
2. Classify pairs into relationship categories:
   - Parent-offspring (PO): kinship ~ 0.25, IBS0 ~ 0
   - Full-sibling (FS): kinship ~ 0.25, IBS0 > 0
   - Half-sibling (HS): kinship ~ 0.125
   - Unrelated: kinship ~ 0
3. Validate top candidates against metadata (sex, date, location, plate — cross-plate pairs are more credible)
4. Resolve duplicate barcodes: determine which record is correct for each of the 6 duplicated sample_ids
5. Estimate genotyping error rates from identified PO pairs (Mendelian inconsistencies)
6. Output: `data/kin_pairs.csv` — classified kin pairs with kinship coefficients and metadata

**Deliverable**: `notebooks/05_kinship_inference.ipynb`, `data/kin_pairs.csv`

---

## Step 7: Spatial Kinship & Dispersal

**Goal**: Map kin pairs spatially and estimate dispersal distances.

**Notebook `notebooks/06_spatial_kinship.ipynb`**:
1. Overlay identified kin pairs on GPS map — lines connecting related individuals
2. Compute geographic distances for each kin-pair category (PO, FS, HS)
3. Compare kin-pair distances to null distribution (random pairs)
4. Estimate parent-offspring dispersal kernel if sufficient PO pairs exist
5. Visualise temporal patterns: collection date gaps for kin pairs (generational signal?)

**Deliverable**: `notebooks/06_spatial_kinship.ipynb`, `results/fig_kin_spatial.png`

---

## Step 8: CKMR Population Size Estimation

**Goal**: Estimate census population size using the close-kin mark-recapture framework.

**Notebook `notebooks/07_ckmr_estimation.ipynb`**:
1. Select kin-pair category for estimation (PO pairs are most robust for CKMR)
2. Apply the CKMR estimator: N ≈ (n₁ × n₂) / (2 × k), where k = number of PO pairs found between two sampling occasions
3. Account for: sampling fraction, sex ratio, temporal structure
4. Bootstrap confidence intervals
5. Sensitivity analysis: vary kinship thresholds, marker filters, error rates
6. Compare estimate to entomological expectations for *An. funestus* population density in the area

**Deliverable**: `notebooks/07_ckmr_estimation.ipynb`, updated `results/anokin-results.md`

---

## Execution Order

### Phase 1: Exploratory analysis (complete)
1. **Step 1** — write `docs/anokin-dataset.md` (initial version) ✅
2. **Step 2** — parse Report files, update dataset docs ✅
3. **Step 3** — build master metadata (notebook + CSV) ✅
4. **Step 4a** — set up pixi env ✅
5. **Step 4b** — genomic QC notebook ✅
6. **Step 4c** — exploratory analysis notebook ✅

### Phase 2: Kinship inference & CKMR (ginkgo workflow)
7. **Step 5a** — scaffold ginkgo workflow (`workflow.py`, `ginkgo.toml`)
8. **Step 5b** — dropout filtering notebook
9. **Step 6** — kinship inference notebook (depends on Step 5b)
10. **Step 7** — spatial kinship notebook (depends on Step 6)
11. **Step 8** — CKMR estimation notebook (depends on Steps 6 + 7)

Steps 1-4 are complete. Step 5 onwards runs as a ginkgo workflow with notebook tasks.

## Verification

### Phase 1 (complete)
- `docs/anokin-dataset.md` exists and is comprehensive ✅
- `data/master_metadata.csv` has one row per mosquito with GPS, species, sex, plate position ✅
- `pixi install` succeeds ✅
- All notebooks run end-to-end without errors ✅
- PCA plot shows meaningful structure (not random noise) ✅
- Geographic vs genetic distance plot shows whether IBD signal exists ✅

### Phase 2
- `ginkgo run` executes the full workflow end-to-end
- Dropout-filtered genotype matrix has reduced F_IS (target: mean < 0.15)
- KING-robust identifies ≥3 close-kin pairs (PO or FS) at kinship > 0.15
- Kin pairs validated against metadata (cross-plate, biologically plausible)
- Spatial kin-pair plot shows dispersal patterns
- CKMR population estimate has bootstrap confidence intervals
