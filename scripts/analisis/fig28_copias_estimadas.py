#!/usr/bin/env python3
"""Figura 22: numero estimado de copias de los 11 contigs de multiples copias.
copias = profundidad media del contig / mediana de la profundidad media de los contigs de 50 kb o mas (cromosoma).
Uso: python3 fig28_copias_estimadas.py S1_coverage.tsv salida.png copias_estimadas_S1.tsv"""
import sys,re,statistics
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
cov,out,tsv=sys.argv[1:4]
rows={}
for l in open(cov):
    if l[0]=="#": continue
    p=l.split("\t"); m=re.match(r"NODE_(\d+)_length_(\d+)_cov_([\d.]+)",p[0])
    if m: rows[int(m[1])]=(int(m[2]),float(m[3]),float(p[6]))
ref=statistics.median(d for L,k,d in rows.values() if L>=50000)
CL={91:"ARN ribosomal",99:"ARN ribosomal",147:"ARN ribosomal",76:"Elemento de inserción",597:"Elemento de inserción",45:"Compatible con plásmido (blaZ, Tn552)",66:"Bloque de profago",85:"Bloque de profago",201:"Bloque de profago",987:"Región de profago (NODE_987)",1251:"Repetición no codificante"}
COL={"ARN ribosomal":"#0072B2","Elemento de inserción":"#E69F00","Compatible con plásmido (blaZ, Tn552)":"#009E73","Bloque de profago":"#CC79A7","Región de profago (NODE_987)":"#D55E00","Repetición no codificante":"#555555"}
order=[91,99,147,76,597,1251,45,66,85,201,987]
data=[(n,)+rows[n]+(rows[n][2]/ref,) for n in order]
with open(tsv,"w") as f:
    f.write("contig\tlargo_pb\tcov_kmer\tprofundidad_media\tcopias_estimadas\tclase\n")
    for n,L,k,d,c in data: f.write(f"NODE_{n}\t{L}\t{k:.0f}\t{d:.0f}\t{c:.1f}\t{CL[n]}\n")
fig,ax=plt.subplots(figsize=(9,5))
for i,(n,L,k,d,c) in enumerate(data):
    y=len(data)-i
    ax.barh(y,c,color=COL[CL[n]],height=0.65)
    ax.text(c+0.15,y,f"{c:.1f}×  ({d:,.0f}×)".replace(","," "),va="center",fontsize=8.5)
    ax.text(-0.15,y,f"NODE_{n}  ({L:,} pb)".replace(","," "),ha="right",va="center",fontsize=8.5)
ax.axvline(1,color="k",ls="--",lw=1); ax.text(1.05,len(data)+0.7,"1 copia (cromosoma)",fontsize=8.5)
ax.set_xlim(0,13.5); ax.set_ylim(0.3,len(data)+1.2); ax.set_yticks([])
ax.set_xlabel(f"Copias estimadas (profundidad del contig / {ref:,.0f}×)".replace(","," "))
ax.legend([plt.Rectangle((0,0),1,1,color=c) for c in COL.values()],list(COL),loc="lower right",fontsize=8,frameon=False)
for s in("top","right","left"): ax.spines[s].set_visible(False)
ax.set_title("Copias estimadas de los contigs de múltiples copias",loc="left",fontsize=10)
fig.tight_layout(); fig.savefig(out,dpi=200)
