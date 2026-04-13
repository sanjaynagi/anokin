"""AnoKin — ginkgo workflow for close-kin mark-recapture analysis."""

import ginkgo
from ginkgo import file, flow, notebook, task

cfg = ginkgo.config("ginkgo.toml")

# ---------------------------------------------------------------------------
# Tasks — each wraps a notebook and declares its file outputs
# ---------------------------------------------------------------------------


@task("notebook")
def genomic_qc(*, snp_2: file, snp_3: file, metadata: file):
    return notebook(
        path="notebooks/02_genomic_qc.ipynb",
        outputs="data/geno_filtered.csv",
    )


@task("notebook")
def exploratory_analysis(*, geno_filtered: file, metadata: file):
    return notebook(
        path="notebooks/03_exploratory_analysis.ipynb",
        outputs=["results/fig_pca.png", "results/fig_ibs.png", "results/fig_spatial.png"],
    )


@task("notebook")
def dropout_filtering(*, geno_filtered: file, snp_mapping_2: file, snp_mapping_3: file, metadata: file):
    return notebook(
        path="notebooks/04_dropout_filtering.ipynb",
        outputs="data/geno_dropout_filtered.csv",
    )


@task("notebook")
def kinship_inference(*, geno_dropout_filtered: file, metadata: file):
    return notebook(
        path="notebooks/05_kinship_inference.ipynb",
        outputs="data/kin_pairs.csv",
    )


@task("notebook")
def spatial_kinship(*, kin_pairs: file, metadata: file):
    return notebook(
        path="notebooks/06_spatial_kinship.ipynb",
        outputs="results/fig_kin_spatial.png",
    )


@task("notebook")
def ckmr_estimation(*, kin_pairs: file, metadata: file):
    return notebook(
        path="notebooks/07_ckmr_estimation.ipynb",
        outputs="results/ckmr_estimates.csv",
    )


@task("notebook")
def halfsib_analysis(*, kin_pairs: file, geno_dropout_filtered: file, metadata: file):
    return notebook(
        path="notebooks/08_halfsib_analysis.ipynb",
        outputs="results/halfsib_analysis.csv",
    )


# ---------------------------------------------------------------------------
# Flow — wires the DAG
# ---------------------------------------------------------------------------


@flow
def main():
    # Input files
    snp_2 = cfg["data"]["snp_2"]
    snp_3 = cfg["data"]["snp_3"]
    metadata = cfg["data"]["metadata"]
    snp_mapping_2 = "data/Report_DMo25-3087_SNP_mapping_2.csv"
    snp_mapping_3 = "data/Report_DMo25-3087_SNP_mapping_3.csv"

    # Phase 1: QC & exploration (existing notebooks)
    qc = genomic_qc(snp_2=snp_2, snp_3=snp_3, metadata=metadata)
    explore = exploratory_analysis(geno_filtered=qc, metadata=metadata)

    # Phase 2: Kinship & CKMR (new notebooks)
    dropout = dropout_filtering(
        geno_filtered=qc,
        snp_mapping_2=snp_mapping_2,
        snp_mapping_3=snp_mapping_3,
        metadata=metadata,
    )
    kinship = kinship_inference(geno_dropout_filtered=dropout, metadata=metadata)
    spatial = spatial_kinship(kin_pairs=kinship, metadata=metadata)
    ckmr = ckmr_estimation(kin_pairs=kinship, metadata=metadata)
    halfsib = halfsib_analysis(kin_pairs=kinship, geno_dropout_filtered=dropout, metadata=metadata)

    return [explore, spatial, ckmr, halfsib]
