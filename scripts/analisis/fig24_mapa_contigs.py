#!/usr/bin/env python3
"""Figura 24: mapa de los contigs del ensamblado filtrado sobre MRSA252.

Lee el archivo PAF exportado por D-Genies (minimap2) y dibuja, sobre la posición
de la referencia, el alineamiento primario de cada contig (hebra en color),
los tramos de la referencia sin contigs y las posiciones de los contigs multicopia.

Uso (desde la carpeta del proyecto):
  python3 analisis/fig24_mapa_contigs.py \
      04_assembly_qc/dgenies_cov100/map_contigs_cov100_to_MRSA252.paf \
      04_assembly_qc/dgenies_cov100/fig24_mapa_contigs.png
Requiere: Python 3 y matplotlib (se usó Python 3.13 y matplotlib 3.11.2).
"""
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("paf", help="archivo PAF de D-Genies")
ap.add_argument("salida", help="imagen PNG de salida")
ap.add_argument("--min-bloque", type=int, default=5000,
                help="largo mínimo (pb) del alineamiento primario a graficar (por defecto 5000)")
ap.add_argument("--min-hueco", type=int, default=10000,
                help="largo mínimo (pb) de un tramo sin contigs para marcarlo (por defecto 10000)")
ap.add_argument("--multicopia", default="NODE_91,NODE_99,NODE_147",
                help="contigs multicopia a marcar, separados por coma")
ap.add_argument("--largo-ref", type=int, default=2902619, help="largo de MRSA252 (pb)")
a = ap.parse_args()

R = a.largo_ref
multi = set(a.multicopia.split(",")) if a.multicopia else set()

# 1) Lectura del PAF: columnas 1 (contig), 2 (largo), 5 (hebra), 8-9 (inicio/fin en la
#    referencia) y 11 (largo del bloque); tp:A:P marca el alineamiento primario.
bloques, pos_multi = [], []
for linea in open(a.paf):
    c = linea.rstrip("\n").split("\t")
    nombre = c[0].split("_length")[0]
    tp = [x for x in c[12:] if x.startswith("tp:")][0]
    ini, fin = int(c[7]), int(c[8])
    if nombre in multi:
        pos_multi.append((ini + fin) // 2)
    if tp == "tp:A:P" and int(c[10]) >= a.min_bloque:
        bloques.append((ini, fin, c[4], nombre.replace("NODE_", "N")))
bloques.sort()

# 2) Reparto en filas para que los bloques no se superpongan ni choquen sus rótulos
fin_fila, fila_de = [], []
for b in bloques:
    for i, f in enumerate(fin_fila):
        if b[0] > f + 32000:
            fin_fila[i] = b[1]
            fila_de.append(i)
            break
    else:
        fin_fila.append(b[1])
        fila_de.append(len(fin_fila) - 1)
n = len(fin_fila)

# 3) Tramos de la referencia sin contigs
huecos, fin = [], 0
for ini, f2 in sorted((b[0], b[1]) for b in bloques):
    if ini > fin + a.min_hueco:
        huecos.append((fin, ini))
    fin = max(fin, f2)
if R > fin + a.min_hueco:
    huecos.append((fin, R))

# 4) Figura
COL = {"+": "#0072B2", "-": "#D55E00"}   # azul: hebra directa; naranja: reversa
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, ax = plt.subplots(figsize=(11, 5.4), dpi=200)
alto = n * 1.9
for h in huecos:
    ax.add_patch(Rectangle((h[0] / 1e6, -0.9), (h[1] - h[0]) / 1e6, alto + 0.9, color="#9a9a9a", alpha=0.25, lw=0))
for b, i in zip(bloques, fila_de):
    y = i * 1.9
    ax.add_patch(Rectangle((b[0] / 1e6, y), (b[1] - b[0]) / 1e6, 0.8, color=COL[b[2]], lw=0))
    if b[1] - b[0] >= 70000:   # bloque ancho: nombre adentro
        ax.text((b[0] + b[1]) / 2e6, y + 0.4, b[3], ha="center", va="center", fontsize=6.5, color="white")
    else:                       # bloque angosto: nombre arriba, en vertical
        ax.text((b[0] + b[1]) / 2e6, y + 0.88, b[3], ha="center", va="bottom", fontsize=5.6, rotation=90)

# triángulos de los contigs multicopia (se agrupan las posiciones a menos de 10 kb)
grupos = []
for m in sorted(set(pos_multi)):
    if grupos and m - grupos[-1][-1] <= 10000:
        grupos[-1].append(m)
    else:
        grupos.append([m])
for g in grupos:
    ax.plot(sum(g) / len(g) / 1e6, -0.45, marker="v", color="black", ms=4.5, clip_on=False)

# leyenda
ax.plot([], [], "v", color="black", ms=4.5, label="Posiciones de los contigs multicopia (" + ", ".join(sorted(multi)) + ")")
ax.add_patch(Rectangle((0, 0), 0, 0, color=COL["+"], label="Contig en hebra directa"))
ax.add_patch(Rectangle((0, 0), 0, 0, color=COL["-"], label="Contig en hebra reversa"))
ax.add_patch(Rectangle((0, 0), 0, 0, color="#9a9a9a", alpha=0.4, label="Hueco de más de %d kb sin contigs" % (a.min_hueco // 1000)))

# rótulos: el hueco más grande y el contig que cruza el origen del cromosoma
mayor = max(huecos, key=lambda h: h[1] - h[0])
kb = ("%.1f" % ((mayor[1] - mayor[0]) / 1e3)).replace(".", ",")
ax.annotate(kb + " kb sin contigs", xy=((mayor[0] + mayor[1]) / 2e6, alto + 0.2),
            xytext=((mayor[0] + mayor[1]) / 2e6 - 0.3, alto + 1.5), fontsize=7.5, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", lw=0.6), annotation_clip=False)
cierre = [b for b in bloques if b[1] >= R - 5000]   # bloque que llega al final de la referencia
if cierre:
    b = cierre[0]
    ax.annotate("%s cruza el origen (0 / %s Mb)" % (b[3].replace("N", "NODE_"), ("%.2f" % (R / 1e6)).replace(".", ",")),
                xy=(b[1] / 1e6 - 0.02, fila_de[bloques.index(b)] * 1.9 + 0.4), xytext=(2.5, alto + 1.5),
                fontsize=7.5, ha="center", va="center", arrowprops=dict(arrowstyle="-", lw=0.6), annotation_clip=False)

ax.set_xlim(0, R / 1e6)
ax.set_ylim(-0.9, alto + 2.1)
ax.set_xlabel("Posición en MRSA252 (Mb)")
ax.set_yticks([])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, frameon=False, fontsize=7.5)
fig.subplots_adjust(top=0.97, bottom=0.2, left=0.02, right=0.99)
fig.savefig(a.salida)
print("bloques:", len(bloques), "| filas:", n, "| huecos:", len(huecos), "| guardado en", a.salida)
