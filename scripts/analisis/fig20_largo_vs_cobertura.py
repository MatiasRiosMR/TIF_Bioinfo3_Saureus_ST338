#!/usr/bin/env python3
"""Figura 20: largo del contig vs. cobertura de k-mers (SPAdes, corrida completa).
Entrada: contigs.fasta de SPAdes. Uso:
  python3 analisis/fig20_largo_vs_cobertura.py 03_assembly/S1_full/contigs.fasta Figura20.png
"""
import re, sys
import numpy as np
import matplotlib.pyplot as plt

fasta, out = sys.argv[1], sys.argv[2]
L, C = [], []
with open(fasta) as f:
    for line in f:
        if line.startswith('>'):            # >NODE_1_length_178006_cov_309.546915
            p = line[1:].split('_')
            L.append(int(p[3])); C.append(float(p[5]))
L, C = np.array(L), np.array(C)

plt.rcParams.update({'font.family': 'serif', 'font.size': 14})
fig, ax = plt.subplots(figsize=(10, 7))
short = L < 500
low   = ~short & (C < 20)
high  = ~short & (C >= 100)
ax.scatter(L[short], C[short], s=8, c='#b0b0b0', alpha=.5, lw=0,
           label=f'Menos de 500 pb (n = {short.sum():,})'.replace(',', ' '))
ax.scatter(L[low], C[low], s=10, c='#d55e00', alpha=.6, lw=0,
           label=f'500 pb o más, cobertura < 20 (n = {low.sum():,})'.replace(',', ' '))
ax.scatter(L[high], C[high], s=14, c='#0072b2', alpha=.85, lw=0,
           label=f'500 pb o más, cobertura ≥ 100 (n = {high.sum()})')
ax.set_xscale('log'); ax.set_yscale('log')
ax.axvline(500, c='k', ls=':', lw=1)
for y in (20, 100):
    ax.axhline(y, c='k', ls='--', lw=1)
    ax.text(ax.get_xlim()[1]*.9, y*1.15, str(y), ha='right', fontsize=12)
ax.set_xlabel('Largo del contig (pb)'); ax.set_ylabel('Cobertura de k-mers')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.legend(loc='upper center', bbox_to_anchor=(.5, -.15), frameon=False)
fig.savefig(out, dpi=210, bbox_inches='tight')
