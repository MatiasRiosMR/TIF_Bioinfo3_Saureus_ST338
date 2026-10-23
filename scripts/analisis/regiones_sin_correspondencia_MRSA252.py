#!/usr/bin/env python3
"""Tramos de los contigs sin correspondencia con MRSA252 (a partir del PAF de minimap2/D-Genies).
Uso: python3 regiones_sin_correspondencia_MRSA252.py mapeo.paf contigs.fasta salida.tsv [largo_minimo=3000] [cov_kmer_minima=100] [largo_contig_minimo=500]
Fusiona los intervalos alineados de cada contig y lista los tramos sin alinear de largo_minimo o mas.
Tambien informa los contigs con cobertura de k-mers >= cov_kmer_minima que no estan en el PAF."""
import sys,re,collections
paf,fa,out=sys.argv[1:4]
minlen=int(sys.argv[4]) if len(sys.argv)>4 else 3000
mincov=float(sys.argv[5]) if len(sys.argv)>5 else 100
minctg=int(sys.argv[6]) if len(sys.argv)>6 else 500
L={};K={}
for l in open(fa):
    m=re.match(r">(NODE_(\d+)_length_(\d+)_cov_([\d.]+))",l)
    if m: L[int(m[2])]=int(m[3]); K[int(m[2])]=float(m[4])
al=collections.defaultdict(list)
for l in open(paf):
    p=l.split("\t"); n=int(re.match(r"NODE_(\d+)",p[0])[1]); al[n].append((int(p[2]),int(p[3])))
def merge(iv):
    o=[]
    for a,b in sorted(iv):
        if o and a<=o[-1][1]: o[-1][1]=max(o[-1][1],b)
        else: o.append([a,b])
    return o
sel=[n for n in L if K[n]>=mincov and L[n]>=minctg]
tot=sum(L[n] for n in sel); aligned=0; rows=[]
for n in sel:
    m=merge(al.get(n,[])); aligned+=sum(b-a for a,b in m); prev=0
    for a,b in m+[[L[n],L[n]]]:
        if a-prev>=minlen: rows.append((n,prev+1,a,a-prev))
        prev=b
    if n not in al and L[n]>=minlen: rows.append((n,1,L[n],L[n]))
with open(out,"w") as f:
    f.write("contig\tinicio\tfin\tlargo_pb\n")
    for n,a,b,d in sorted(rows,key=lambda x:-x[3]): f.write(f"NODE_{n}\t{a}\t{b}\t{d}\n")
print(f"contigs de {minctg} pb o mas con cov_kmer>={mincov:g}: {len(sel)}; total {tot} pb; alineados {aligned} pb ({100*aligned/tot:.2f} %); sin alinear {tot-aligned} pb; contigs sin PAF: {sum(1 for n in sel if n not in al)}")
