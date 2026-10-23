#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# ESTADO: PLANIFICADO, todavía no se ejecutó. Revisar y ajustar antes de correr.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Secciones 2.5 y 2.8 - Alineamiento de las lecturas contra MRSA252 y perfil de cobertura para IGV
# ENTORNO: tif_bioinfo3 (Bowtie2, SAMtools, deepTools) | PLATAFORMA: computadora personal
bowtie2-build 05_reference/MRSA252.fasta 05_reference/MRSA252
bowtie2 -p 8 -x 05_reference/MRSA252 \
  -1 02_trim/S1_R1.fq.gz -2 02_trim/S1_R2.fq.gz 2> logs/bt2_ref.log \
  | samtools sort -@ 4 -o 09_igv/S1_ref.bam
samtools index 09_igv/S1_ref.bam

# Perfil de cobertura normalizado (bigWig) para IGV
G=$(cut -f2 05_reference/MRSA252.fasta.fai)
bamCoverage -b 09_igv/S1_ref.bam -o 09_igv/S1_ref.bw --binSize 50 \
  --normalizeUsing RPGC --effectiveGenomeSize "$G" -p 4

# Índice del ensamblado filtrado para cargarlo en IGV
samtools faidx 03_assembly/S1_full/contigs_cov100.fasta

# QUAST del ensamblado filtrado contra MRSA252 (Sección 2.5)
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate quast_env
quast.py 03_assembly/S1_full/contigs_cov100.fasta \
  -r 05_reference/MRSA252.fasta -o 04_assembly_qc/quast_cov100 -t 4
