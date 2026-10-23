#!/usr/bin/env python3
"""Figura 21: BLAST (NCBI, nt) de los 5 contigs de multiples copias sin funcion asignada.
A: colinealidad de NODE_66, NODE_85, NODE_201 y NODE_987 en registros de NCBI (coordenadas relativas, orientadas).
B: copias por registro (hits casi completos, >=95 % id y >=95 % cobertura) entre los 100 mejores registros de cada contig.
Uso: python3 fig27_blast_multicopia.py salida.png hits1.csv [hits2.csv ...]   (outfmt 10/tab de NCBI, 12 columnas)"""
import sys,re,collections
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
out=sys.argv[1]; rows={}
for f in sys.argv[2:]:
    for l in open(f):
        l=l.rstrip("\n")
        if not l or l[0]=="#": continue
        p=l.split("\t") if "\t" in l else l.split(",")
        if len(p)==12:
            p[0]=p[0].split("_length")[0]; rows[tuple(p)]=1
rows=list(rows)
L={"NODE_66":2924,"NODE_85":1795,"NODE_201":1122,"NODE_987":606,"NODE_1251":552}
COL={"NODE_66":"#0072B2","NODE_85":"#E69F00","NODE_201":"#009E73","NODE_987":"#CC79A7","NODE_1251":"#555555"}
near=collections.defaultdict(lambda:collections.defaultdict(list))
for p in rows:
    q=p[0]
    if q in L and int(p[3])>=0.95*L[q] and float(p[2])>=95:
        near[q][p[1]].append((int(p[8]),int(p[9])))
recs=["OR901656.1","OR157981.1","PQ516280.1","PP952055.1","PZ447477.1","MG029512.1","CP092825.1","CP053185.1"]
fig,(ax,bx)=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={"width_ratios":[1.7,1]})
for i,a in enumerate(recs):
    y=len(recs)-i
    s66=near["NODE_66"][a]
    if not s66: continue
    s0,e0=s66[0]; sign=1 if e0>s0 else -1
    ax.plot([0,17000],[y,y],color="#bbb",lw=1,zorder=0)
    for q in ("NODE_66","NODE_85","NODE_201","NODE_987"):
        for s,e in near[q].get(a,[]):
            rs,re_=(s-s0)*sign,(e-s0)*sign
            if min(rs,re_)<-500 or max(rs,re_)>17500: continue
            ax.add_patch(FancyArrowPatch((rs,y),(re_,y),arrowstyle="simple,head_width=9,head_length=6,tail_width=9",mutation_scale=1,color=COL[q],lw=0))
    ax.text(-400,y,a,ha="right",va="center",fontsize=8.5)
    if len(s66)>1: ax.text(17200,y,f"{len(s66)} copias del bloque",va="center",fontsize=8,color="#444")
for q,x,dy in (("NODE_66",1500,0.75),("NODE_85",3900,0.75),("NODE_201",5900,0.45),("NODE_987",15500,0.75)):
    ax.text(x,len(recs)+dy,q,color=COL[q],ha="center",fontsize=9,fontweight="bold")
ax.set_xlim(-500,20500); ax.set_ylim(0.3,len(recs)+1.3); ax.set_yticks([])
ax.set_xlabel("Posición relativa al inicio de NODE_66 (pb, orientada)")
ax.set_title("A. NODE_66, 85 y 201 son un solo bloque de 5,8 kb",loc="left",fontsize=10)
for s in("top","right","left"): ax.spines[s].set_visible(False)
w=0.15; bins=["1","2","3–9","≥10"]
def b(n): return 0 if n==1 else 1 if n==2 else 2 if n<10 else 3
for k,q in enumerate(L):
    c=[0]*4
    for a,h in near[q].items(): c[b(len(h))]+=1
    bx.bar([j+(k-2)*w*1.2 for j in range(4)],c,width=w,color=COL[q],label=q)
bx.set_xticks(range(4)); bx.set_xticklabels(bins); bx.set_xlabel("Copias por registro"); bx.set_ylabel("Registros de NCBI (entre los 100 mejores)")
bx.set_title("B. Copias por registro",loc="left",fontsize=10); bx.legend(frameon=False,fontsize=8)
for s in("top","right"): bx.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(out,dpi=200)
