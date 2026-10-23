#!/usr/bin/env python3
"""Figura 25: profundidad de las lecturas de B378 a lo largo de MRSA252.

Entrada: salida de `samtools depth -a` (columnas: cromosoma, posición, profundidad).
Dibuja la profundidad media por ventana, relativa a la mediana del cromosoma
(1 = profundidad típica), marca los tramos de MRSA252 sin lecturas (con su tamaño)
y rotula los picos de profundidad alta.

Uso (desde la carpeta del proyecto):
  samtools depth -a 09_igv/S1_ref.bam > 09_igv/S1_ref.depth.tsv
  python3 analisis/fig25_cobertura_MRSA252.py 09_igv/S1_ref.depth.tsv 09_igv/fig25_cobertura.png
Requiere: Python 3, numpy y matplotlib.
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("depth", help="salida de samtools depth -a")
ap.add_argument("salida", help="imagen PNG de salida")
ap.add_argument("--ventana", type=int, default=2000, help="largo de la ventana en pb (por defecto 2000)")
ap.add_argument("--min-sin-cobertura", type=int, default=5000,
                help="largo mínimo (pb) de un tramo con profundidad 0 para marcarlo (por defecto 5000)")
ap.add_argument("--ymax", type=float, default=3.0, help="máximo del eje vertical (por defecto 3)")
ap.add_argument("--pico", type=float, default=2.0, help="profundidad relativa mínima para rotular un pico (por defecto 2)")
a = ap.parse_args()

# 1) Profundidad por posición
prof = np.loadtxt(a.depth, usecols=2, dtype=np.int32)
n = len(prof)
med = float(np.median(prof))

# 2) Media por ventana, relativa a la mediana
w = a.ventana
nv = n // w
rel = prof[: nv * w].reshape(nv, w).mean(axis=1) / med
x = (np.arange(nv) + 0.5) * w / 1e6

# 3) Tramos de profundidad 0 de al menos --min-sin-cobertura pb
cero = prof == 0
tramos, i = [], 0
while i < n:
    if cero[i]:
        j = i
        while j < n and cero[j]:
            j += 1
        if j - i >= a.min_sin_cobertura:
            tramos.append((i, j))
        i = j
    else:
        i += 1
# se agrupan los tramos separados por menos de 30 kb para rotularlos juntos
grupos = []
for t in tramos:
    if grupos and t[0] - grupos[-1][-1][1] < 30000:
        grupos[-1].append(t)
    else:
        grupos.append([t])

# 4) Picos: máximo local de cada zona con profundidad relativa >= --pico (separados por 30 kb)
picos = []
for k in np.argsort(rel)[::-1]:
    if rel[k] < a.pico:
        break
    if all(abs(x[k] - p[0]) > 0.03 for p in picos):
        picos.append((x[k], rel[k]))

# 5) Figura
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, ax = plt.subplots(figsize=(11, 3.6), dpi=200)
ax.grid(axis="y", color="#dddddd", lw=0.6, zorder=0)
for g in grupos:
    ini, fin = g[0][0], g[-1][1]
    ax.axvspan(ini / 1e6, fin / 1e6, color="#9a9a9a", alpha=0.35, lw=0, zorder=1)
    kb = sum(t[1] - t[0] for t in g) / 1e3
    ax.text((ini + fin) / 2e6, a.ymax * 0.97, ("%.1f" % kb).replace(".", ",") + " kb", ha="center", va="top",
            fontsize=6.8, rotation=90)
ax.fill_between(x, np.minimum(rel, a.ymax), step="mid", color="#0072B2", alpha=0.85, lw=0, zorder=2)
ax.axhline(1, color="black", lw=0.7, ls="--", zorder=3)
for px, py in picos:
    ax.plot(px, min(py, a.ymax) , marker="v", color="#D55E00", ms=4, zorder=4, clip_on=False)
    ax.text(px, min(py, a.ymax) + 0.07, ("%.2f" % px).replace(".", ","), ha="center", va="bottom", fontsize=6.3,
            color="#D55E00", rotation=90, clip_on=False)
ax.set_xlim(0, n / 1e6)
ax.set_ylim(0, a.ymax)
ax.set_xlabel("Posición en MRSA252 (Mb)")
ax.set_ylabel("Profundidad relativa")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.plot([], [], color="#0072B2", lw=6, label="Profundidad media por ventana de %d kb (1 = mediana, %.0f×)" % (w / 1000, med))
ax.add_patch(plt.Rectangle((0, 0), 0, 0, color="#9a9a9a", alpha=0.5,
                           label="Tramos de %d kb o más sin lecturas (tamaño total del grupo)" % (a.min_sin_cobertura // 1000)))
ax.plot([], [], "v", color="#D55E00", ms=4, label="Pico de %g× o más (posición en Mb)" % a.pico)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=False, fontsize=7.2)
fig.subplots_adjust(bottom=0.3, left=0.07, right=0.99, top=0.88)
fig.savefig(a.salida)
print("posiciones:", n, "| mediana:", med, "| tramos sin cobertura:", len(tramos), "| picos rotulados:", len(picos))
for t in tramos:
    print("  %d-%d (%d pb)" % (t[0] + 1, t[1], t[1] - t[0]))
