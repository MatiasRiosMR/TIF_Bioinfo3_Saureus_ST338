#!/usr/bin/env bash
# TP Final Bioinformática 3 - aislamiento B378 (ST338, SRR26803856)
# Se ejecuta desde cualquier carpeta; PROJ es la carpeta del proyecto.
set -euo pipefail
PROJ="${PROJ:-$HOME/tp_final}"
cd "$PROJ"
# Sección 2.3.2 - Métricas del ensamblado completo con awk
# ENTORNO: ninguno especial | PLATAFORMA: computadora personal
# SPAdes nombra los contigs NODE_n_length_L_cov_C: campo 4 = largo, campo 6 = cobertura de k-mers.
FA=03_assembly/S1_full/contigs.fasta

# Número de contigs y largo total
grep -c '>' "$FA"
awk '!/^>/{s+=length($0)} END{print s}' "$FA"

# Contigs de 500 pb o más y de menos de 500 pb
LC_ALL=C awk -F_ '/^>/{L=$4; C=$6; if(L>=500){n1++; s1+=L} else {n2++; s2+=L; c2+=C}} \
  END{print "≥500 pb:", n1, "contigs,", s1, "pb"; \
  print "<500 pb:", n2, "contigs,", s2, "pb, cobertura media", c2/n2}' "$FA"

# N50 y L50 de los contigs de 500 pb o más
awk '/^>/{if(s>=500)print s; s=0; next}{s+=length($0)} END{if(s>=500)print s}' "$FA" | sort -rn | \
  awk '{l[NR]=$1; t+=$1} END{for(i=1;i<=NR;i++){a+=l[i]; if(a>=t/2){print "N50:", l[i], "L50:", i; exit}}}'

# Contigs de 500 pb o más por cobertura de k-mers (>=100, 20-100 y <20)
LC_ALL=C awk -F_ '/^>/ && $4>=500 {c=$6; L=$4; if(c>=100){a++; sa+=L} else if(c>=20){b++; sb+=L} else {d++; sd+=L}} \
  END{print "cov >=100:", a, "contigs,", sa, "pb"; print "cov 20-100:", b, "contigs,", sb, "pb"; \
  print "cov <20:", d, "contigs,", sd, "pb"}' "$FA"

# Contenido de GC por grupo de cobertura (contigs de 500 pb o más)
LC_ALL=C awk -F_ '/^>/{ok=($4>=500); g=($6>=100)?"cov>=100":"cov<100"; next} \
  ok{gc[g]+=gsub(/[GCgc]/,"&"); t[g]+=length($0)} \
  END{for(g in t) print g, t[g], 100*gc[g]/t[g]}' "$FA"
