#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.4 - Ensamblado filtrado: contigs de 500 pb o más con cobertura de k-mers >= 100
# ENTORNO: ninguno especial | PLATAFORMA: computadora personal
# Entrada de la anotación (Prokka) y la tipificación; el ensamblado reportado sigue siendo el completo.
# Fecha: 20/10/2026. Confirmado por los docentes el 21/10/2026.
LC_ALL=C awk -F_ '/^>/{keep=($6>=100 && $4>=500)} keep' \
  03_assembly/S1_full/contigs.fasta > 03_assembly/S1_full/contigs_cov100.fasta
grep -c '>' 03_assembly/S1_full/contigs_cov100.fasta                                  # esperado: 74
awk '!/^>/{s+=length($0)} END{print s}' 03_assembly/S1_full/contigs_cov100.fasta      # esperado: 2790840
