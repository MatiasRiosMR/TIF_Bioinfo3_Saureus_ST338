#!/usr/bin/env python3
"""Figura 23: profundidad real (Bowtie2 + samtools) vs. largo y vs. cobertura de k-mers.
Entradas:
  1) contigs.fasta de SPAdes (largo y cobertura de k-mers desde el nombre)
  2) tabla de `samtools coverage` (columnas: #rname startpos endpos numreads covbases coverage meandepth ...)
Generar la tabla con:
  samtools coverage 09_igv/S1_asm.bam > 04_assembly_qc/S1_coverage.tsv
Uso:
  python3 analisis/fig23_profundidad_real.py 03_assembly/S1_full/contigs.fasta 04_assembly_qc/S1_coverage.tsv Figura23.png
"""
import sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

fasta, covtsv, out = sys.argv[1:4]
rows = []
with open(fasta) as f:
    for line in f:
        if line.startswith('>'):
            p = line[1:].split('_')
            rows.append((line[1:].split()[0], int(p[3]), float(p[5])))
d = pd.DataFrame(rows, columns=['rname', 'len', 'kcov'])
s = pd.read_csv(covtsv, sep='\t').rename(columns={'#rname': 'rname'})
d = d.merge(s[['rname', 'meandepth']], on='rname')
d = d[d.meandepth > 0]

short = d.len < 500
low   = ~short & (d.kcov < 100)
high  = ~short & (d.kcov >= 100)
mean_high = np.average(d.meandepth[high], weights=d.len[high])   # media ponderada por largo
ratio = d.meandepth[high].sum() / d.kcov[high].sum()             # factor de proporcionalidad

plt.rcParams.update({'font.size': 12})
fig, (a, b) = plt.subplots(1, 2, figsize=(14, 5.6))
for ax, x, xl in ((a, d.len, 'Largo del contig (pb)'),
                  (b, d.kcov, 'Cobertura de k-mers (SPAdes)')):
    ax.scatter(x[short], d.meandepth[short], s=6, c='#999999', alpha=.4, lw=0)
    ax.scatter(x[low],   d.meandepth[low],   s=8, c='#d9604c', alpha=.6, lw=0)
    ax.scatter(x[high],  d.meandepth[high],  s=22, c='#2f6fb5', ec='white', lw=.5)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel(xl); ax.set_ylabel('Profundidad media de lecturas (×)')
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    ax.grid(alpha=.2)
a.axhline(mean_high, c='#2f6fb5', ls='--', lw=1.3)
a.scatter([], [], s=10, c='#d0d0d0', label='Menos de 500 pb')
a.scatter([], [], s=20, c='#e0988a', label='500 pb o más, k-mers < 100')
a.scatter([], [], s=30, c='#2f6fb5', label='500 pb o más, k-mers ≥ 100')
a.plot([], [], c='#2f6fb5', ls='--', label=f'{mean_high:.0f}× (media de los {high.sum()} contigs)')
a.legend(loc='lower right', frameon=False, fontsize=11)
xs = np.array([d.kcov.min()*.8, d.kcov.max()*1.3])
b.plot(xs, ratio*xs, c='#333', ls='--', lw=1.3,
       label=f'Esperado: profundidad = {ratio:.2f} × k-mers'.replace('.', ','))
b.legend(loc='lower right', frameon=False, fontsize=11)
a.text(-.02, 1.04, 'A', transform=a.transAxes, fontsize=16, weight='bold')
b.text(-.02, 1.04, 'B', transform=b.transAxes, fontsize=16, weight='bold')
fig.tight_layout(); fig.savefig(out, dpi=150)
