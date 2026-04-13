# AnoKin Dataset Reference

This document describes the complete AnoKin dataset: field sampling data and DArTseq genomic data for ~900 *Anopheles funestus* mosquitoes collected from Lake Kanyaboli, Siaya County, western Kenya.

---

## Study Overview

- **Species**: *Anopheles funestus* (primary target); also collected *An. gambiae s.l.*, *An. coustani*, and others
- **Site**: Lake Kanyaboli, Siaya County, western Kenya (NE corner, overlapping ATSB trial cluster 38)
- **Sampling design**: Cross-sectional entomological survey; wedge-shaped area (~3km × 3km); 4 quadrants sampled over multiple days
- **Collection method**: Prokopack aspirator, indoor household aspiration, 06:00–10:00
- **Target**: ≥250 *An. funestus* per quadrant (≥1000 total)
- **Sequencing**: DArTseq (RADseq-like GBS) by SeqArt Africa (ILRI, Nairobi); NovaseqX, single-read 138 cycles
- **Reference genome**: VectorBase-68 *Anopheles funestus* AfunGA1

---

## File Inventory

### Genomic Data (`data/`)

| File | Size | Rows | Cols | Description |
|------|------|------|------|-------------|
| `Report_DMo25-3087_SilicoDArT_1.csv` | 226 MB | 109,822 | 909 | SilicoDArT presence/absence markers |
| `Report_DMo25-3087_SNP_2.csv` | 274 MB | 126,195 | 918 | SNP genotypes (ref + alt allele rows) |
| `Report_DMo25-3087_SNP_3.csv` | 223 MB | 101,895 | 918 | SNP genotypes (additional loci) |
| `Report_DMo25-3087_SNP_mapping_2.csv` | 146 MB | 63,101 | 920 | SNP mapping/annotation + read counts |
| `Report_DMo25-3087_SNP_mapping_3.csv` | 119 MB | 50,951 | 920 | SNP mapping/annotation + read counts |
| `seqart_sample_tracking_file.csv` | 47 KB | 944 | 9 | Plate layout (PlateID, Row, Column, Species) |
| `metadata.xlsx` | 28 KB | — | — | Additional metadata |
| `kemri_sequencing_plate.xlsx` | 72 KB | — | — | KEMRI plate layout |

### ODK Field Data (`sampling/odk/`)

| File | Rows | Description |
|------|------|-------------|
| `ckmr_sampling.csv` | 29 | Household-level data (GPS, building type) — day 1 only |
| `ckmr_uvlt.csv` | 132 | UV light trap household visits (GPS, building type, barcodes) — main GPS source |
| `ckmr_morpho_id.csv` | 285 | Morpho-ID sessions (barcode, household-id, collector) |
| `ckmr_morpho_id-mosquito_data.csv` | 994 | Individual mosquito records (species, sex, blood-fed, sample_id) |

---

## DArTseq Report Format

All Report files share a multi-row header structure (rows 1–6 are metadata, row 7 is column names, data starts at row 8):

| Header Row | Content | Example |
|------------|---------|---------|
| 1 | Order ID | `*` (metadata cols), `DMo25-3087` (sample cols) |
| 2 | Batch/Run ID | `*`, `910425164001` |
| 3 | Plate number | `*`, `1`, `2`, `3`, ... (up to 8 plates) |
| 4 | Well row | `*`, `A`–`H` |
| 5 | Well column | `*`, `1`–`12` |
| 6 | Species label | `*`, `"none [Original species: Anopheles_funestus]"` |
| 7 | Column names | Marker metadata columns + sample ep-barcodes |

### SilicoDArT File (`_SilicoDArT_1.csv`)

Presence/absence of restriction fragments. **One row per marker**.

- **Metadata columns** (1–15): `CloneID`, `AlleleSequence`, `TrimmedSequence`, `Chrom_*`, `ChromPosTag_*`, `AlnCnt_*`, `AlnEvalue_*`, `Strand_*`, `CallRate`, `OneRatio`, `PIC`, `AvgReadDepth`, `StDevReadDepth`, `Qpmr`, `Reproducibility`
- **Sample columns** (16–909): 894 samples, values are `1` (present), `0` (absent), or `-` (missing)
- **Markers**: ~109,815 SilicoDArT markers
- **Genotype encoding**: Binary (1/0) — presence/absence of the restriction fragment

### SNP Files (`_SNP_2.csv`, `_SNP_3.csv`)

SNP genotypes. **Two rows per SNP locus** (reference allele row + alternative allele row).

- **Metadata columns** (1–24): `AlleleID`, `CloneID`, `AlleleSequence`, `TrimmedSequence`, `Chrom_*`, `ChromPosTag_*`, `ChromPosSnp_*`, `AlnCnt_*`, `AlnEvalue_*`, `Strand_*`, `SNP`, `SnpPosition`, `CallRate`, `OneRatioRef`, `OneRatioSnp`, `FreqHomRef`, `FreqHomSnp`, `FreqHets`, `PICRef`, `PICSnp`, `AvgPIC`, `AvgCountRef`, `AvgCountSnp`, `RepAvg`
- **Sample columns** (25–918): 894 samples, values are `1` (allele present), `0` (absent), or `-` (missing)
- **SNP_2**: ~63,094 SNP loci (126,188 rows ÷ 2)
- **SNP_3**: ~50,944 SNP loci (101,888 rows ÷ 2)
- **AlleleID format**: `CloneID|F|0--pos:Ref>Alt` (ref row) and `CloneID|F|0-pos:Ref>Alt-pos:Ref>Alt` (alt row)
- **To get standard genotypes** (0/1/2): For each locus, combine ref and alt rows: `ref=1,alt=0` → homozygous ref (0); `ref=0,alt=1` → homozygous alt (2); `ref=1,alt=1` → heterozygous (1); `ref=-,alt=-` → missing

### SNP Mapping Files (`_SNP_mapping_2.csv`, `_SNP_mapping_3.csv`)

Annotation and read-count data for the same SNP loci. **One row per allele** (same row count as corresponding SNP file).

- **Extra metadata columns** (1–26): Include `AlleleSequenceRef`, `AlleleSequenceSnp`, `TrimmedSequenceRef`, `TrimmedSequenceSnp` (both ref and alt sequences in each row)
- **Sample columns** (27–920): 894 samples — values are **read counts** (integers), not binary genotypes
- Correspond 1:1 with rows in the SNP files

---

## Sample Identifiers

**894 unique samples** in the genomic data, identified by ep-barcodes (e.g., `ep0000917698`).

### ID Linkage Chain

```
Genomic data (column headers, row 7)
    └── ep-barcode (e.g., ep0000844050)
         │
         ├── seqart_sample_tracking_file.csv
         │     PlateID + Row + Column → ep-barcode
         │     (odk_barcode column is EMPTY — not populated)
         │
         └── ckmr_morpho_id-mosquito_data.csv
               sample_id = ep-barcode
               PARENT_KEY → ckmr_morpho_id.KEY
                              │
                              ├── barcode (e.g., 000282)
                              └── household-id (e.g., A1-10-6-In)
                                    │
                                    ├── → ckmr_uvlt.csv (GPS, building data)
                                    │     via unique_code_indoor/outdoor or barcode
                                    │
                                    └── → ckmr_sampling.csv (GPS, building data)
                                          via barcode or unique_code
```

### Sample Overlap

| Set | Count |
|-----|-------|
| Genomic data (unique ep-barcodes) | 894 |
| ODK mosquito records (unique sample_ids) | 986 |
| In both genomic AND ODK | 892 |
| In genomic only | 2 |
| In ODK only | 102 |

The 102 ODK-only samples are likely non-*An. funestus* specimens (47 *An. coustani*, 23 *An. gambiae s.l.*, 10 other, plus some *An. funestus* that may have failed sequencing QC).

### Species Breakdown (ODK morpho ID)

| Species | Count |
|---------|-------|
| *An. funestus* | 914 |
| *An. coustani* | 47 |
| *An. gambiae s.l.* | 23 |
| Other | 10 |
| **Total** | 994 |

---

## GPS / Spatial Data

GPS coordinates are recorded per household in two ODK forms:

- **`ckmr_sampling.csv`**: 29 household records (appears to be day 1 only); columns `initialise-gps-Latitude`, `initialise-gps-Longitude`
- **`ckmr_uvlt.csv`**: 132 household records (main GPS source); same GPS columns; has both indoor and outdoor barcodes per house

The **`ckmr_morpho_id.csv`** form does NOT contain GPS — it must be joined via barcode or household-id to the GPS-containing forms.

### Household-ID Format

The household-id encodes `Team-Day-Household-Position`:
- Example: `A1-10-6-In` = Team A1, Day 10, Household 6, Indoor collection
- Teams: A1, C2, J2, S3, V1 (and others)
- The `unique_code` in sampling/uvlt uses the same convention in lowercase (e.g., `s3-1-8`)

---

## Known Data Quirks

1. **`seqart_sample_tracking_file.csv`**: The `odk_barcode` column is empty — plate positions cannot be linked to ODK via this file. Instead, use the ep-barcode sample IDs directly (they appear both as column headers in Report files and as `sample_id` in ODK mosquito data).

2. **Multi-row headers**: All Report CSVs have 6 metadata header rows before the actual column names (row 7). Standard `pd.read_csv()` will fail — use `skiprows=6` or `header=6`.

3. **Missing data encoded as `-`**: In genotype matrices, missing values are `-` (not `NA` or empty). Must be handled during parsing.

4. **SNP files have paired rows**: Each SNP locus occupies two rows (ref allele + alt allele). Must be combined to get standard 0/1/2 genotypes.

5. **GPS mismatch**: Only ~22 barcodes overlap between `ckmr_sampling` and `ckmr_morpho_id`. The `ckmr_uvlt` form (132 records, 264 unique codes) is the primary GPS source for most households.

6. **Case sensitivity in household-IDs**: Morpho-ID uses mixed case (e.g., `A1-10-6-In`) while sampling/uvlt uses lowercase (e.g., `a1-10-6-in`). Normalise to lowercase for joins.

7. **Plate layout**: 8 plates × 96 wells (8 rows A–H × 12 columns), but plates 1 and 2 have rows G and H with only 11 wells (columns 1–11, no column 12), giving 894 samples total rather than 8 × 96 = 768. Some plates appear to have more wells used.
