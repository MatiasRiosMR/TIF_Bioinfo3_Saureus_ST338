import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
OK,PAR,PEN="#2E7D32","#F9A825","#9E9E9E"
FILL={OK:"#E8F5E9",PAR:"#FFF8E1",PEN:"#F2F2F2"}
fig,ax=plt.subplots(figsize=(16,9)); ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")
def box(x,y,w,h,title,sub,st):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.12",fc=FILL[st],ec=st,lw=2))
    ax.text(x+w/2,y+h-0.22,title,ha="center",va="top",fontsize=9.5,fontweight="bold")
    n=title.count("\n")+1
    ax.text(x+w/2,y+h-0.28-0.27*n-0.15,sub,ha="center",va="top",fontsize=7.8,color="#333",linespacing=1.25)
def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=14,color="#555",lw=1.4))
ax.text(0.2,8.7,"Avance del TP Final · B378 (ST338) · 22/10/2026",fontsize=15,fontweight="bold",va="center")
ax.text(0.2,8.3,"Modalidad C, de novo + caracterización (consigna puntos 1 a 9, reproducción y nuevos análisis)",fontsize=9.5,color="#444",va="center")
# fila 1: pipeline
r1=[("Etapa 1\nActividad 1","Propuesta aprobada\n1 genoma (docentes)",OK),
("2.0 Datos","SRA NCBI · MRSA252\nentorno tif_bioinfo3",OK),
("2.1 Control\nde calidad","FastQC + MultiQC",OK),
("2.2 Recorte","Trimmomatic\n92,5 % de pares\nversión registrada",OK),
("2.3 Ensamblado","SPAdes 4.3.0 --isolate\n17 258 contigs\n74 con cob. ≥ 100",OK),
("2.4 Calidad del\nensamblado","QUAST (quast_env, por\nPython 3.14) · BUSCO\nBowtie2",OK)]
w,h,y=2.35,1.75,5.95
for i,(t,s,st) in enumerate(r1):
    x=0.2+i*2.6; box(x,y,w,h,t,s,st)
    if i: arrow(x-0.25,y+h/2,x,y+h/2)
# fila 2
r2=[("2.5 Comparación\ncon MRSA252","D-Genies · QUAST\n[párrafo pendiente]",PAR),
("2.6 Anotación","Prokka 1.14.6 (Galaxy)\n847 hipotéticas",OK),
("2.7 Análisis\nbiológico","BLAST+ · ABRicate · MLST\nPHASTEST\n[versión web · unzip PHASTEST]",PAR),
("2.8 Genome\nbrowser","IGV: ensamblado,\nGFF y lecturas",PEN),
("2.9 Estrategias\nde ensamblado","30× y 100×, iso y car\ntexto, tablas y Fig. 23 listos\nfalta ABRicate (BUSCO opc.)",PAR),
("2.10 y 2.11\nReproducción\ny nuevos análisis","Resultados 1 y 2 · Análisis 1 y 2\n[% de Chen · registros NCBI]",PAR)]
y2=3.55
for i,(t,s,st) in enumerate(r2):
    x=0.2+i*2.6; box(x,y2,w,h,t,s,st)
    if i: arrow(x-0.25,y2+h/2,x,y2+h/2)
arrow(13.0,y+0.0,13.0,y2+h+0.0) if False else None
# fila 3: redacción y entregas
r3=[("3 Reproducibilidad","scripts y versiones\n(faltan PHASTEST y\nD-Genies, web)",PAR),
("4 Decisiones","tabla casi completa\n[fechas por confirmar]",PAR),
("5, 6 y 7\nLimitaciones, conclusiones\ny artículo","por redactar",PEN),
("Figuras 19 a 25","imágenes por insertar\n(Fig. 23: fig23_informe.png)",PEN),
("Revisión final","reducir extensión\nactualizar índice\nquitar guía en rojo",PEN)]
y3=1.15
for i,(t,s,st) in enumerate(r3):
    x=0.2+i*3.1; box(x,y3,2.85,h,t,s,st)
# entregas
ax.text(0.2,0.78,"Fechas:",fontsize=9.5,fontweight="bold",va="center")
ax.text(1.3,0.78,"05/11 informe, artículo (3 a 10 págs., archivo aparte) y datos   ·   06/11 presentación oral (15 min, Bioinformágica)   ·   12/11 revisión por pares   ·   19/11 recuperatorio",fontsize=9,va="center")
# leyenda
for i,(c,l) in enumerate([(OK,"Hecho"),(PAR,"Hecho, con detalles por cerrar"),(PEN,"Pendiente")]):
    ax.add_patch(FancyBboxPatch((0.2+i*3.2,0.2),0.35,0.28,boxstyle="round,pad=0.01",fc=FILL[c],ec=c,lw=2))
    ax.text(0.7+i*3.2,0.34,l,fontsize=9,va="center")
plt.savefig("esquema_avance.png",dpi=170,bbox_inches="tight",facecolor="white")
