#!/usr/bin/env python3
"""Figura de contexto genomico (Analisis 2): contexto genomico de los genes de virulencia y tramos de B378 sin correspondencia con MRSA252.
Salida A: mapa circular de MRSA252: genes de virulencia, cobertura de los contigs de B378 (ventanas de 10 kb) y tramos propios de B378.
Salida B: histogramas del GC de ventanas del mismo largo tomadas de las regiones que si alinean (5000 ventanas) y GC observado de cada tramo (prueba empirica, bilateral).
Uso: python3 fig29_contexto_genomico.py mapeo.paf contigs.fasta tramos.tsv salida_A.png salida_B.png tabla_gc.tsv"""
import sys,re,random,collections
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
paf,fa,tr,outA,outB,tsv=sys.argv[1:7]
random.seed(1)
seq={};K={};cur=None
for l in open(fa):
    l=l.strip()
    if l[0]==">":
        m=re.match(r">NODE_(\d+)_length_(\d+)_cov_([\d.]+)",l); cur=int(m[1]); seq[cur]=[]; K[cur]=float(m[3])
    else: seq[cur].append(l)
seq={n:"".join(v).upper() for n,v in seq.items() if K[n]>=100 and len("".join(v))>=500}
blocks=collections.defaultdict(list); REF=0
for l in open(paf):
    p=l.split("\t"); n=int(re.match(r"NODE_(\d+)",p[0])[1]); REF=int(p[6])
    blocks[n].append((int(p[2]),int(p[3]),p[4],int(p[7]),int(p[8])))
def toref(n,q):
    best=None
    for qs,qe,st,ts,te in blocks.get(n,[]):
        d=0 if qs<=q<=qe else min(abs(q-qs),abs(q-qe))
        if best is None or d<best[0]: best=(d,qs,qe,st,ts,te)
    if best is None: return None
    d,qs,qe,st,ts,te=best; q=min(max(q,qs),qe); f=(q-qs)/max(qe-qs,1)
    return ts+f*(te-ts) if st=="+" else te-f*(te-ts)
# genes: (nombre, contig, posicion en el contig, grupo). Coordenadas de ABRicate (sdrE, cap8K, mecA), tblastn (sasA) y Prokka (clpL, ebh).
G=[("sdrE",16,5300,"inf"),("sasA (sraP)",5,41800,"inf"),("cap8K",4,76600,"port"),("clpL",3,28000,"port"),("ebh",15,60000,"port"),("mecA",60,2950,"res")]
COL={"inf":"#D55E00","port":"#0072B2","res":"#009E73"}
genes=[(g,toref(n,p),c) for g,n,p,c in G]
tracts=[]
for l in list(open(tr))[1:]:
    c,a,b,d=l.split(); n=int(c[5:]); a=int(a); b=int(b); d=int(d)
    if n in blocks and n in seq and not (a==1 and b==len(seq[n])):
        tracts.append((c,a,b,d,toref(n,max(a-1,1)),seq[n][a-1:b]))
tracts=sorted(tracts,key=lambda x:x[4])   # numerados segun la posicion en MRSA252
def gc(s): return 100*(s.count("G")+s.count("C"))/max(len(s),1)
aligned=[]
for n,bl in blocks.items():
    if n in seq:
        for qs,qe,*_ in bl: aligned.append(seq[n][qs:qe])
aligned=[s for s in aligned if len(s)>=3000]
w=[len(s) for s in aligned]
def nullgc(L):
    out=[]
    for _ in range(5000):
        s=random.choices(aligned,weights=w)[0]
        if len(s)<L: continue
        i=random.randrange(0,len(s)-L+1); out.append(gc(s[i:i+L]))
    return out
plt.rcParams.update({"font.size":11})
PINK="#CC79A7"; DPINK="#9B3C73"
# cobertura de B378 sobre MRSA252 en ventanas de 10 kb
cov=np.zeros(REF//1000+2,dtype=bool)
for n,bl in blocks.items():
    if n in seq:
        for qs,qe,st,ts,te in bl: cov[min(ts,te)//1000:max(ts,te)//1000+1]=True
WIN=10
fr=[cov[i*WIN:(i+1)*WIN].mean() for i in range(REF//1000//WIN+1)]
def ang(p): return 90-360*p/REF
def ring(r0,r1,p0,p1,color,minw=0):
    a0,a1=ang(p0),ang(p1)
    if abs(a0-a1)<minw: m=(a0+a1)/2; a0,a1=m+minw/2,m-minw/2
    ax.add_patch(Wedge((0,0),r1,a1,a0,width=r1-r0,facecolor=color,edgecolor="none"))
# ---------- Figura 23: mapa circular ----------
figA,ax=plt.subplots(figsize=(8.6,8.6)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-1.62,1.62); ax.set_ylim(-1.5,1.62)
cm=plt.get_cmap("Blues")
for i,f in enumerate(fr): ring(0.76,0.89,i*WIN*1000,min((i+1)*WIN*1000,REF),cm(0.08+0.92*f))
ring(0.90,1.0,0,REF,"#444")
for m in np.arange(0,REF,500000):
    a=np.radians(ang(m)); ax.text(np.cos(a)*0.95,np.sin(a)*0.95,f"{m/1e6:.1f}".replace(".",","),ha="center",va="center",fontsize=8,color="white",fontweight="bold")
for i,(c,a0,b0,d,p,sq) in enumerate(tracts):
    ring(0.66,0.74,p,p+max(d,1),PINK,minw=2.2)
    pm=p+d/2; a=np.radians(ang(pm)); r=0.60-0.09*(i%3)
    ax.plot([np.cos(a)*0.66,np.cos(a)*(r+0.045)],[np.sin(a)*0.66,np.sin(a)*(r+0.045)],color=PINK,lw=0.9)
    ax.text(np.cos(a)*r,np.sin(a)*r,str(i+1),ha="center",va="center",fontsize=11,fontweight="bold",color=DPINK)
for g,p,c in genes:
    a=np.radians(ang(p)); ca,sa=np.cos(a),np.sin(a)
    ax.plot([ca*1.0,ca*1.22],[sa*1.0,sa*1.22],color=COL[c],lw=1.2)
    ax.scatter([ca*1.03],[sa*1.03],s=60,color=COL[c],zorder=4,edgecolor="white",lw=0.8)
    ax.text(ca*1.25,sa*1.25,g,ha="left" if ca>=0 else "right",va="center",fontsize=11,style="italic")
ax.text(0,0.18,"MRSA252",ha="center",fontsize=13,fontweight="bold")
ax.text(0,0.08,"2,9 Mb",ha="center",fontsize=11,color="#444")
ax.text(0,-0.04,"Tramos propios de B378",ha="center",fontsize=9,color=DPINK)
for i,(c,a0,b0,d,p,sq) in enumerate(tracts):
    ax.text(0,-0.13-0.068*i,f"{i+1}  {c} · {d/1000:.1f} kb".replace(".",","),ha="center",fontsize=8.5,color="#333")
h=[plt.Line2D([],[],marker="o",ls="",color=COL[k],markersize=8) for k in COL]+[plt.Line2D([],[],marker="s",ls="",color=PINK,markersize=8),plt.Line2D([],[],marker="s",ls="",color=cm(0.95),markersize=8),plt.Line2D([],[],marker="s",ls="",color=cm(0.1),markersize=8)]
ax.legend(h,["Gen de infección","Gen de portación","mecA","Tramo propio de B378","Alinea con B378","Sin cobertura de B378"],loc="lower center",bbox_to_anchor=(0.5,-0.04),ncol=3,fontsize=10,frameon=False)
# ---------- Figura 24: histogramas de GC ----------
rows=[];nul={}
for i,(c,a0,b0,d,p,sq) in enumerate(tracts):
    nl=nullgc(d); v=gc(sq)
    pv=min(1,2*min(sum(1 for x in nl if x<=v),sum(1 for x in nl if x>=v))/len(nl)); pv=max(pv,1/len(nl))
    rows.append((i+1,c,a0,b0,d,v,sum(nl)/len(nl),pv)); nul[i]=nl
figB,axs=plt.subplots(2,3,figsize=(9.6,7.6))
fmt=plt.FuncFormatter(lambda x,_: f"{x:g}".replace(".",","))
for i,bx in enumerate(axs.flat):
    n,c,a0,b0,d,v,m,pv=rows[i]; sig=pv<0.05/len(rows)
    bx.hist(nul[i],bins=30,color="#C9CED6",edgecolor="white",lw=0.4)
    bx.axvline(v,color="#B2182B" if sig else PINK,lw=2.6)
    bx.axvline(m,color="#555",ls="--",lw=1)
    bx.set_title(f"{n}  {c} ({d/1000:.1f} kb)".replace(".",","),fontsize=11,loc="left",fontweight="bold" if sig else "normal")
    ptxt=("p < 0,001" if pv<0.001 else f"p = {pv:.3f}".replace(".",","))+(" *" if sig else "")
    lo,hi=bx.get_xlim(); bx.set_xlim(min(lo,v-0.8),max(hi,v+0.8))
    right=v<m
    bx.text(0.97 if right else 0.03,0.95,f"GC = {v:.1f} %".replace(".",",")+"\n"+ptxt,transform=bx.transAxes,ha="right" if right else "left",va="top",fontsize=10,color="#B2182B" if sig else "#222")
    bx.xaxis.set_major_formatter(fmt)
    for s_ in("top","right"): bx.spines[s_].set_visible(False)
    if i%3==0: bx.set_ylabel("Ventanas")
    if i>=3: bx.set_xlabel("GC (%)")
    bx.tick_params(labelsize=9)
h=[plt.Line2D([],[],color="#B2182B",lw=2.6),plt.Line2D([],[],color=PINK,lw=2.6),plt.Line2D([],[],color="#555",ls="--",lw=1),plt.Rectangle((0,0),1,1,color="#C9CED6")]
figB.legend(h,["Tramo de B378 (p < 0,008)","Tramo de B378","Media de las ventanas","Ventanas de regiones que alinean"],loc="lower center",ncol=4,fontsize=9.5,frameon=False)
figB.tight_layout(rect=(0,0.05,1,1))
figA.savefig(outA,dpi=200,bbox_inches="tight"); figB.savefig(outB,dpi=200)
with open(tsv,"w") as f:
    f.write("n\tcontig\tinicio\tfin\tlargo_pb\tGC_tramo\tGC_medio_ventanas\tp_empirico\n")
    for r in rows: f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]:.2f}\t{r[6]:.2f}\t{r[7]:.4f}\n")
print(open(tsv).read())
