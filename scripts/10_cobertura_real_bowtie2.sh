#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.4.1 - Profundidad real de cada contig (lecturas recortadas contra el ensamblado completo)
# ENTORNO: tif_bioinfo3 (Bowtie2 2.5.5, SAMtools 1.24) | PLATAFORMA: computadora personal
bowtie2-build 03_assembly/S1_full/contigs.fasta 09_igv/S1_asm
bowtie2 -p 8 -x 09_igv/S1_asm \
  -1 02_trim/S1_R1.fq.gz -2 02_trim/S1_R2.fq.gz 2> logs/bt2_asm.log \
  | samtools sort -@ 4 -o 09_igv/S1_asm.bam
samtools index 09_igv/S1_asm.bam
# Una fila por contig: lecturas alineadas, bases cubiertas, % cubierto y profundidad media
samtools coverage 09_igv/S1_asm.bam > 04_assembly_qc/S1_coverage.tsv
tail -n 5 logs/bt2_asm.log     # resumen de alineamiento (esperado: 96,75 % de alineamiento global)
