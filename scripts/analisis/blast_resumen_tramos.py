#!/usr/bin/env python3
"""Resumen por tramo de la tabla de hits de blastn (NCBI web, Download > Hit Table (csv); 12 columnas, sin encabezado ni titulos).
Para cada tramo (consulta) y cada registro: se unen los alineamientos (HSP), cobertura = bases del tramo cubiertas / largo del tramo,
identidad = maxima de los HSP, mejor registro = el de mayor puntaje (bits). El largo del tramo se toma del final del nombre (..._19936pb).
Uso: python3 blast_resumen_tramos.py hits.csv resumen.tsv"""
import sys,csv,re
rows=[x for x in csv.reader(open(sys.argv[1])) if len(x)>=12]
Q={}
for x in rows: Q.setdefault(x[0],{}).setdefault(x[1],[]).append(x)
def cov(v,L):
    iv=sorted((min(int(y[6]),int(y[7])),max(int(y[6]),int(y[7]))) for y in v); m=[]
    for a,b in iv:
        if m and a<=m[-1][1]: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    return 100*sum(b-a+1 for a,b in m)/L
with open(sys.argv[2],"w") as f:
    f.write("tramo\tlargo_pb\tregistros_en_tabla\tregistros_cob90_id95\tmejor_registro\tidentidad_%\tcobertura_%\tpuntaje_bits\thsp_por_registro_mediana\n")
    for q,d in Q.items():
        L=int(re.search(r"_(\d+)pb$",q)[1])
        st=[(s,max(float(y[2]) for y in v),cov(v,L),max(float(y[11]) for y in v),len(v)) for s,v in d.items()]
        n=sum(1 for s,i,c,b,k in st if c>=90 and i>=95)
        top=max(st,key=lambda t:t[3]); ks=sorted(t[4] for t in st)
        f.write(f"{q}\t{L}\t{len(d)}\t{n}\t{top[0]}\t{top[1]:.2f}\t{top[2]:.0f}\t{top[3]:.0f}\t{ks[len(ks)//2]}\n")
