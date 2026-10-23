#!/usr/bin/env python3
"""Figura 20: mapa de genes (Prokka) de los 11 contigs de multiples copias y de la region ebh (NODE_15).
Uso: python3 fig26_prokka_multicopia_ebh.py prokka.gff3 contigs.fasta salida.png
Los contigs de Prokka (BLAGNNMM_n) se asignan a NODE_n por largo."""
import sys,re
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
gff,fa,out=sys.argv[1:4]
NODES=[91,99,147,76,597,45,66,85,201,987,1251]
info={}
for l in open(fa):
    m=re.match(r">NODE_(\d+)_length_(\d+)_cov_([\d.]+)",l)
    if m: info[int(m[1])]=(int(m[2]),float(m[3]))
bylen={}
for n,(L,c) in info.items(): bylen.setdefault(L,[]).append(n)
seq={}
for l in open(gff):
    if l.startswith("##sequence-region"):
        _,sid,a,b=l.split(); seq[sid]=int(b)
node_of={}
for s,L in seq.items():
    for n in bylen.get(L,[]):
        node_of[s]=n if n in NODES+[15] else node_of.get(s,n)
feats={n:[] for n in NODES+[15]}
for l in open(gff):
    if l.startswith("#") or l.startswith(">"): continue
    p=l.rstrip("\n").split("\t")
    if len(p)<9 or p[2] not in("CDS","rRNA","tRNA","tmRNA","ncRNA"): continue
    n=node_of.get(p[0])
    if n not in feats: continue
    a={k:v for k,v in (x.split("=",1) for x in p[8].split(";") if "=" in x)}
    feats[n].append((int(p[3]),int(p[4]),p[6],p[2],a.get("gene",""),a.get("product","")))
def cat(t,g,pr):
    pl=pr.lower()
    if t in("rRNA","tRNA","tmRNA"): return "ARN ribosomal / tRNA","#4e79a7"
    if "transposase" in pl or "insertion" in pl or g.startswith(("bin","hin")) or "invertase" in pl or "recombinase" in pl: return "Transposasa / invertasa","#f28e2b"
    if re.match(r"(bla|cad|mec)",g): return "Resistencia (bla, cad)","#e15759"
    if "hypothetical" in pl: return "Proteína hipotética","#bab0ac"
    return "Otra función","#59a14f"
fig=plt.figure(figsize=(11,9.5))
gs=fig.add_gridspec(2,1,height_ratios=[11,2.2],hspace=0.35)
ax=fig.add_subplot(gs[0]); seen={}
for i,n in enumerate(NODES):
    y=len(NODES)-i; L,c=info[n]
    ax.add_patch(Rectangle((0,y-0.03),L,0.06,color="#333",zorder=1))
    for s,e,st,t,g,pr in feats[n]:
        lab,col=cat(t,g,pr); seen[lab]=col
        x0,x1=(s,e) if st=="+" else (e,s)
        ax.add_patch(FancyArrowPatch((x0,y),(x1,y),arrowstyle="simple,head_width=7,head_length=5,tail_width=7",mutation_scale=1,color=col,zorder=2,lw=0))
        if g and abs(e-s)>400: ax.text((s+e)/2,y+0.28,g.split("_")[0],ha="center",fontsize=7.5,style="italic")
    ax.text(-0.01*21000,y,f"NODE_{n}\n{L:,} pb · cov {c:,.0f}×".replace(","," "),ha="right",va="center",fontsize=8)
ax.set_xlim(0,20600); ax.set_ylim(0.4,len(NODES)+0.7); ax.set_yticks([])
ax.set_xlabel("Posición en el contig (pb)"); ax.set_title("A. Genes anotados por Prokka en los 11 contigs de múltiples copias (k-mer cov > 600)",loc="left",fontsize=10)
for s in("top","right","left"): ax.spines[s].set_visible(False)
ax.legend([Rectangle((0,0),1,1,color=c) for c in seen.values()],list(seen),loc="lower right",fontsize=8,frameon=False)
ax2=fig.add_subplot(gs[1]); fe=sorted(feats[15]); idx=[k for k,f in enumerate(fe) if f[4].startswith("ebh")]
lo=max(0,fe[idx[0]][0]-3000); hi=min(info[15][0],fe[idx[-1]][1]+3000)
ax2.add_patch(Rectangle((lo,-0.03),hi-lo,0.06,color="#333"))
for s,e,st,t,g,pr in fe:
    if e<lo or s>hi: continue
    lab,col=cat(t,g,pr)
    if g.startswith("ebh"): col="#b07aa1"
    x0,x1=(s,e) if st=="+" else (e,s)
    ax2.add_patch(FancyArrowPatch((x0,0),(x1,0),arrowstyle="simple,head_width=9,head_length=6,tail_width=9",mutation_scale=1,color=col,lw=0))
    if g.startswith("ebh"): ax2.text((s+e)/2,0.35,f"{g} ({e-s+1:,} pb)".replace(","," "),ha="center",fontsize=8,style="italic")
ax2.set_xlim(lo,hi); ax2.set_ylim(-0.6,0.8); ax2.set_yticks([])
ax2.axvline(info[15][0],color="k",ls=":",lw=1); ax2.text(info[15][0],-0.45,"fin del contig",ha="right",fontsize=8); ax2.set_xlabel("Posición en NODE_15 (pb)"); ax2.set_title("B. Región ebh en NODE_15: dos CDS contiguos en la misma hebra",loc="left",fontsize=10)
for s in("top","right","left"): ax2.spines[s].set_visible(False)
fig.savefig(out,dpi=200,bbox_inches="tight")
