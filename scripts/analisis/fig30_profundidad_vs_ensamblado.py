#!/usr/bin/env python3
"""Figura 23 (Analisis 1): efecto de la profundidad de secuenciacion y del modo de SPAdes sobre las metricas de QUAST.
Entrada: el report.tsv de la corrida de QUAST con todos los ensamblados (una columna por ensamblado; filas 'metrica<TAB>valor1<TAB>valor2...').
Uso: python3 fig30_profundidad_vs_ensamblado.py 10_depth/quast_comp/report.tsv figura.png tabla.tsv"""
import sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
rep,out,tsv=sys.argv[1:4]
L=[l.rstrip("\n").split("\t") for l in open(rep)]
names=L[0][1:]; D={r[0]:r[1:] for r in L[1:]}
def val(k,i):
    try: return float(D[k][i].split()[0].replace(",",""))
    except (KeyError,ValueError,IndexError): return float("nan")
M=[("N50","N50 (kb)",1e3,False),("NGA50","NGA50 (kb)",1e3,False),("# contigs (>= 0 bp)","Contigs de cualquier largo (escala log)",1,True),("Total length","Largo total de los contigs de 500 pb o más (Mb)",1e6,False),("Genome fraction (%)","Fracción de MRSA252 cubierta (%)",1,False),("# misassemblies","Errores de ensamblado (misassemblies)",1,False)]
# QUAST muestra '# contigs (>= 0 bp)' y '# contigs'; se usa este ultimo (>= 500 pb)
PAL={"completo":"#444444","filtrado":"#888888"}
col=lambda n: "#0072B2" if "iso" in n else ("#D55E00" if "car" in n else PAL.get(n,"#999"))
fig,axs=plt.subplots(3,2,figsize=(9.2,9.4))
for ax,(k,t,div,lg) in zip(axs.flat,M):
    v=[val(k,i)/div for i in range(len(names))]
    ax.bar(range(len(v)),v,color=[col(n) for n in names],width=0.65)
    for i,x in enumerate(v): ax.text(i,x,(f"{x:.0f}" if float(x).is_integer() or x>=100 else f"{x:.1f}".replace(".",",")),ha="center",va="bottom",fontsize=8)
    if lg: ax.set_yscale("log")
    ax.set_xticks(range(len(v))); ax.set_xticklabels(names,rotation=35,ha="right",fontsize=9); ax.set_title(t,fontsize=9.5,loc="left")
    for s in("top","right"): ax.spines[s].set_visible(False)
h=[plt.Rectangle((0,0),1,1,color=c) for c in("#444444","#0072B2","#D55E00")]
fig.legend(h,["Ensamblado de referencia (completo o filtrado)","SPAdes --isolate","SPAdes --careful"],loc="lower center",ncol=3,fontsize=9,frameon=False)
fig.tight_layout(rect=(0,0.04,1,1)); fig.savefig(out,dpi=200)
with open(tsv,"w") as f:
    f.write("ensamblado\t"+"\t".join(k for k,_,_,_ in M)+"\n")
    for i,n in enumerate(names): f.write(n+"\t"+"\t".join(str(val(k,i)) for k,_,_,_ in M)+"\n")
