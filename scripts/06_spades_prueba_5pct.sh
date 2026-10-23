#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.3.1 - Prueba con el 5 % de los pares (~40x)
# ENTORNO: tif_bioinfo3 (seqtk, SPAdes) | PLATAFORMA: computadora personal
# Submuestreo del 5 % de los pares (misma semilla en R1 y R2: se conservan los pares)
seqtk sample -s 42 02_trim/S1_R1.fq.gz 0.05 | gzip > 10_depth/test_R1.fq.gz
seqtk sample -s 42 02_trim/S1_R2.fq.gz 0.05 | gzip > 10_depth/test_R2.fq.gz

# Ensamblado de prueba, midiendo tiempo y memoria máxima
/usr/bin/time -v spades.py --isolate -1 10_depth/test_R1.fq.gz -2 10_depth/test_R2.fq.gz \
  -t 10 -m 12 -o 10_depth/test 2> logs/spades_test.time
grep -E "Elapsed|Maximum resident" logs/spades_test.time

# Número de contigs y largo total
grep -c '>' 10_depth/test/contigs.fasta
awk '!/^>/{s+=length($0)} END{print s}' 10_depth/test/contigs.fasta

# Contigs de 500 pb o más y de menos de 500 pb (LC_ALL=C: awk interpreta el punto decimal)
LC_ALL=C awk -F_ '/^>/{L=$4; C=$6; if(L>=500){n1++; s1+=L} else {n2++; s2+=L; c2+=C}} \
  END{print "≥500 pb:", n1, "contigs,", s1, "pb"; \
  print "<500 pb:", n2, "contigs,", s2, "pb, cobertura media", c2/n2}' 10_depth/test/contigs.fasta
grep '>' 10_depth/test/contigs.fasta | head -5
