# Estructura del repositorio

Árbol de trabajo completo, obtenido con:

```
tree -L 3 -I '00_raw*|02_trim|K*|.git|pipeline_state|misc|corrected|tmp|mismatch_corrector|assembly_graph*|scaffolds.*|before_rr.fasta|icarus_viewers|aligned_stats|basic_stats|contigs_reports|genome_stats|minimap_output|blastdb_contigs_cov100|multiqc_data|pistas|test|__pycache__|*.bt2'
```

Se omiten los directorios y archivos listados en `-I`: o bien están excluidos por `.gitignore` (datos crudos, recortados,
intermedios de SPAdes, índices `.bt2`, `pistas/`, `10_depth/test/`, base BLAST local, `icarus_viewers/`), o son subcarpetas
internas de QUAST y MultiQC (`aligned_stats/`, `basic_stats/`, `contigs_reports/`, `genome_stats/`, `multiqc_data/`) que se describen en el README de cada carpeta.
También existen en disco pero no se versionan los BAM/BAI y `09_igv/S1_ref.depth.tsv`.

```
.
├── 01_qc
│   ├── raw
│   │   ├── multiqc_report.html
│   │   ├── SRR26803856_1_fastqc.html
│   │   ├── SRR26803856_1_fastqc.zip
│   │   ├── SRR26803856_2_fastqc.html
│   │   └── SRR26803856_2_fastqc.zip
│   ├── README.md
│   └── trim
│       ├── multiqc_antes_despues_data
│       ├── multiqc_antes_despues.html
│       ├── S1_R1_fastqc.html
│       ├── S1_R1_fastqc.zip
│       ├── S1_R2_fastqc.html
│       └── S1_R2_fastqc.zip
├── 03_assembly
│   ├── README.md
│   └── S1_full
│       ├── contigs_cov100.fasta
│       ├── contigs_cov100.fasta.fai
│       ├── contigs.fasta
│       ├── contigs.paths
│       ├── dataset.info
│       ├── input_dataset.yaml
│       ├── params.txt
│       ├── run_spades.sh
│       ├── run_spades.yaml
│       └── spades.log
├── 04_assembly_qc
│   ├── busco_full
│   │   ├── busco_full_table.tsv
│   │   └── busco_short_summary.txt
│   ├── contigs_filtrados_atipicos.tsv
│   ├── dgenies_cov100
│   │   ├── map_contigs_cov100_to_MRSA252.paf
│   │   └── map_contigs_cov100_to_MRSA252.png
│   ├── gc_tramos_B378.tsv
│   ├── quast_cov100
│   │   ├── icarus.html
│   │   ├── quast.log
│   │   ├── report.html
│   │   ├── report.pdf
│   │   ├── report.tex
│   │   ├── report.tsv
│   │   ├── report.txt
│   │   ├── transposed_report.tex
│   │   ├── transposed_report.tsv
│   │   └── transposed_report.txt
│   ├── quast_full
│   │   ├── icarus.html
│   │   ├── quast.log
│   │   ├── report.html
│   │   ├── report.pdf
│   │   ├── report.tex
│   │   ├── report.tsv
│   │   ├── report.txt
│   │   ├── transposed_report.tex
│   │   ├── transposed_report.tsv
│   │   └── transposed_report.txt
│   ├── README.md
│   ├── regiones_sin_correspondencia_MRSA252.tsv
│   └── S1_coverage.tsv
├── 05_reference
│   ├── MRSA252.fasta
│   ├── MRSA252.fasta.fai
│   └── README.md
├── 06_annotation
│   ├── prokka
│   │   ├── B378_prokka_nodenames.gff3
│   │   ├── prokka_B378_err.txt
│   │   ├── prokka_B378_faa.fasta
│   │   ├── prokka_B378_ffn.fasta
│   │   ├── prokka_B378_fna.fasta
│   │   ├── prokka_B378_fsa.fasta
│   │   ├── prokka_B378_gbk.genbank
│   │   ├── prokka_B378_gff.gff3
│   │   ├── prokka_B378_log.txt
│   │   ├── prokka_B378_tbl.txt
│   │   ├── prokka_B378_tsv.tabular
│   │   └── prokka_B378_txt.txt
│   └── README.md
├── 07_typing
│   ├── mlst_S1.tsv
│   └── README.md
├── 08_genes_mge
│   ├── abricate_card_S1.tsv
│   ├── abricate_vfdb_S1.tsv
│   ├── blast_ncbi
│   │   ├── blast_multicopia_S1_hits_unificado.csv
│   │   ├── blast_multicopia_S1_resumen.tsv
│   │   └── raw
│   ├── copias_estimadas_S1.tsv
│   ├── phastest
│   │   ├── detail.txt
│   │   ├── phage_regions.fna
│   │   ├── predicted_genes.json
│   │   ├── predicted_phage_regions.json
│   │   └── summary.txt
│   ├── proteinas_genes_chen2024.fasta
│   ├── README.md
│   └── tblastn_genes_S1.tsv
├── 09_igv
│   ├── capturas_finales
│   │   ├── Figura_16_IGV_sin_cobertura_44-72kb.png
│   │   ├── Figura_17_IGV_zoom_borde_47231.png
│   │   ├── Figura_18_IGV_delecion_1598-1625kb.png
│   │   ├── Figura_19_IGV_zoom_borde_1602062.png
│   │   ├── Figura_20_IGV_cobertura_alta_745-757kb.png
│   │   ├── Figura_21_IGV_zoom_pico_752kb.png
│   │   ├── Figura_26_IGV_ensamblado_mecA_NODE_60.png
│   │   ├── Figura_27_IGV_ensamblado_ebh_NODE_15.png
│   │   └── README.md
│   ├── cargar_igv.batch
│   ├── contigs_B378_vs_MRSA252.bed
│   ├── fig25_cobertura.png
│   ├── README.md
│   ├── regiones_cov0.bed
│   ├── regiones_cov_alta.bed
│   ├── S1_asm.bam
│   ├── S1_asm.bam.bai
│   ├── S1_ref.bam
│   ├── S1_ref.bam.bai
│   ├── S1_ref.bw
│   ├── S1_ref_cobertura_cruda.bw
│   └── S1_ref.depth.tsv
├── 10_depth
│   ├── abricate_vfdb
│   │   ├── S1_100x_car_vfdb.tsv
│   │   ├── S1_100x_iso_vfdb.tsv
│   │   ├── S1_30x_car_vfdb.tsv
│   │   └── S1_30x_iso_vfdb.tsv
│   ├── metricas_submuestreos.tsv
│   ├── quast_comp
│   │   ├── icarus.html
│   │   ├── quast.log
│   │   ├── report.html
│   │   ├── report.pdf
│   │   ├── report.tex
│   │   ├── report.tsv
│   │   ├── report.txt
│   │   ├── transposed_report.tex
│   │   ├── transposed_report.tsv
│   │   └── transposed_report.txt
│   ├── README.md
│   ├── S1_100x_car
│   │   ├── contigs.fasta
│   │   ├── contigs.paths
│   │   ├── dataset.info
│   │   ├── input_dataset.yaml
│   │   ├── params.txt
│   │   ├── run_spades.sh
│   │   ├── run_spades.yaml
│   │   └── spades.log
│   ├── S1_100x_iso
│   │   ├── contigs.fasta
│   │   ├── contigs.paths
│   │   ├── dataset.info
│   │   ├── input_dataset.yaml
│   │   ├── params.txt
│   │   ├── run_spades.sh
│   │   ├── run_spades.yaml
│   │   └── spades.log
│   ├── S1_100x_R1.fq.gz
│   ├── S1_100x_R2.fq.gz
│   ├── S1_30x_car
│   │   ├── contigs.fasta
│   │   ├── contigs.paths
│   │   ├── dataset.info
│   │   ├── input_dataset.yaml
│   │   ├── params.txt
│   │   ├── run_spades.sh
│   │   ├── run_spades.yaml
│   │   ├── spades.log
│   │   └── warnings.log
│   ├── S1_30x_iso
│   │   ├── contigs.fasta
│   │   ├── contigs.paths
│   │   ├── dataset.info
│   │   ├── input_dataset.yaml
│   │   ├── params.txt
│   │   ├── run_spades.sh
│   │   ├── run_spades.yaml
│   │   ├── spades.log
│   │   └── warnings.log
│   ├── S1_30x_R1.fq.gz
│   ├── S1_30x_R2.fq.gz
│   ├── test_R1.fq.gz
│   └── test_R2.fq.gz
├── docs
├── envs
│   ├── quast_env.yml
│   └── tif_bioinfo3.yml
├── figuras
│   ├── fig23_informe.png
│   ├── fig26_prokka_multicopia_ebh.png
│   ├── fig27_blast_multicopia.png
│   ├── fig28_copias_estimadas.png
│   ├── fig29A_mapa.png
│   ├── fig29B_gc.png
│   ├── fig30.png
│   ├── FigX_gc_cobertura.png
│   └── README.md
├── logs
│   ├── bt2_asm.log
│   ├── bt2_ref.log
│   ├── conda_list_tif_bioinfo3.txt
│   ├── fasterq-dump.log
│   ├── prefetch_SRR26803856.log
│   ├── spades_100x_car.time
│   ├── spades_100x_iso.time
│   ├── spades_30x_car.time
│   ├── spades_30x_iso.time
│   ├── spades_full.time
│   ├── spades_submuestreos.log
│   ├── spades_test.time
│   ├── trimmomatic_S1.log
│   ├── vdb-validate.log
│   ├── wget-log
│   └── wget-log.1
├── README.md
└── scripts
    ├── 00_crear_carpetas.sh
    ├── 01_descarga_lecturas_ncbi.sh
    ├── 02_descarga_referencia.sh
    ├── 03_qc_lecturas_crudas.sh
    ├── 04_recorte_trimmomatic.sh
    ├── 05_qc_posterior_recorte.sh
    ├── 06_spades_prueba_5pct.sh
    ├── 07_spades_completo.sh
    ├── 08_metricas_ensamblado.sh
    ├── 09_quast_completo.sh
    ├── 10_cobertura_real_bowtie2.sh
    ├── 11_filtrar_cov100.sh
    ├── analisis
    │   ├── analisis_contigs_gc_cobertura.R
    │   ├── blast_resumen_tramos.py
    │   ├── esquema_avance.py
    │   ├── fig20_largo_vs_cobertura.py
    │   ├── fig23_informe.R
    │   ├── fig23_profundidad_real.py
    │   ├── fig24_mapa_contigs.py
    │   ├── fig25_cobertura_MRSA252.py
    │   ├── fig26_prokka_multicopia_ebh.py
    │   ├── fig27_blast_multicopia.py
    │   ├── fig28_copias_estimadas.py
    │   ├── fig29_contexto_genomico.py
    │   ├── fig30_profundidad_vs_ensamblado.py
    │   ├── fig30_profundidad_vs_ensamblado.R
    │   ├── grafico_n50_planificado.R
    │   ├── README.md
    │   └── regiones_sin_correspondencia_MRSA252.py
    ├── envs
    │   ├── exportar_entornos.sh
    │   └── README.md
    ├── galaxy
    │   ├── busco_galaxy.md
    │   ├── prokka_galaxy.md
    │   └── subir_archivos_a_galaxy.md
    ├── planificados
    │   ├── 12_comparacion_referencia_igv.sh
    │   └── 13_submuestreos_100x_30x.sh
    └── README.md
```

## Archivo → origen → destino en el informe

Los números de figura y tabla del informe final no pudieron comprobarse desde el repositorio; solo las capturas de IGV llevan el
número en el nombre. El resto se marca [VERIFICAR]. Las rutas de scripts son relativas a la raíz.

| Archivo | Origen (script o herramienta) | Destino en el informe |
|---|---|---|
| `01_qc/raw/` | `scripts/03_qc_lecturas_crudas.sh` | QC de lecturas crudas (Sec. 2.1) [VERIFICAR: figuras/tablas] |
| `01_qc/trim/` | `scripts/05_qc_posterior_recorte.sh` | QC tras el recorte (Sec. 2.2.2) [VERIFICAR] |
| `logs/trimmomatic_S1.log` | `scripts/04_recorte_trimmomatic.sh` | Recorte (Sec. 2.2.1) [VERIFICAR] |
| `03_assembly/S1_full/contigs.fasta` | `scripts/07_spades_completo.sh` | Ensamblado completo (Sec. 2.3.2) [VERIFICAR] |
| `03_assembly/S1_full/contigs_cov100.fasta` | `scripts/11_filtrar_cov100.sh` | Ensamblado filtrado (Sec. 2.4) [VERIFICAR] |
| `04_assembly_qc/quast_full/` | `scripts/09_quast_completo.sh` | Evaluación del ensamblado completo [VERIFICAR] |
| `04_assembly_qc/quast_cov100/` | `scripts/planificados/12_comparacion_referencia_igv.sh` | Evaluación del ensamblado filtrado [VERIFICAR] |
| `04_assembly_qc/busco_full/` | Galaxy, `scripts/galaxy/busco_galaxy.md` | BUSCO [VERIFICAR] |
| `04_assembly_qc/dgenies_cov100/` | D-Genies (web); sin script | Comparación con MRSA252 [VERIFICAR] |
| `04_assembly_qc/S1_coverage.tsv` | `scripts/10_cobertura_real_bowtie2.sh` | Profundidad real por contig [VERIFICAR] |
| `04_assembly_qc/contigs_filtrados_atipicos.tsv` | `scripts/analisis/analisis_contigs_gc_cobertura.R` | Contigs atípicos [VERIFICAR] |
| `04_assembly_qc/regiones_sin_correspondencia_MRSA252.tsv` | `scripts/analisis/regiones_sin_correspondencia_MRSA252.py` | Tramos propios de B378 [VERIFICAR] |
| `04_assembly_qc/gc_tramos_B378.tsv` | `scripts/analisis/fig29_contexto_genomico.py` | GC de los tramos [VERIFICAR] |
| `05_reference/MRSA252.fasta` | `scripts/02_descarga_referencia.sh` | Datos de entrada (Sec. 2.0.5) [VERIFICAR] |
| `06_annotation/prokka/` | Galaxy, `scripts/galaxy/prokka_galaxy.md` | Anotación (Sec. 2.6) [VERIFICAR] |
| `06_annotation/prokka/B378_prokka_nodenames.gff3` | sin script registrado | Insumo de IGV (Figuras 26 y 27) [VERIFICAR: origen] |
| `07_typing/mlst_S1.tsv` | `mlst`; sin script | Resultado 1, tipificación [VERIFICAR] |
| `08_genes_mge/abricate_card_S1.tsv` | ABRicate (CARD); sin script | Resistencia [VERIFICAR] |
| `08_genes_mge/abricate_vfdb_S1.tsv` | ABRicate (VFDB); sin script | Virulencia [VERIFICAR] |
| `08_genes_mge/tblastn_genes_S1.tsv` | tBLASTn; sin script | Reproducción del Resultado 2 [VERIFICAR] |
| `08_genes_mge/copias_estimadas_S1.tsv` | `scripts/analisis/fig28_copias_estimadas.py` | Multicopia [VERIFICAR] |
| `08_genes_mge/blast_ncbi/` | BLASTn web de NCBI; resumen por `blast_resumen_tramos.py` [VERIFICAR] | Multicopia [VERIFICAR] |
| `08_genes_mge/phastest/` | PHASTEST (web); sin script | Profagos [VERIFICAR] |
| `09_igv/regiones_cov0.bed`, `regiones_cov_alta.bed` | derivadas de `S1_ref.depth.tsv` [VERIFICAR: comando] | Regiones sin cobertura y de cobertura alta [VERIFICAR] |
| `09_igv/S1_ref.bw`, `S1_ref.bam` | `scripts/planificados/12_comparacion_referencia_igv.sh` | Mapeo a MRSA252 [VERIFICAR] |
| `09_igv/fig25_cobertura.png` | `scripts/analisis/fig25_cobertura_MRSA252.py` | Cobertura a lo largo de MRSA252 [VERIFICAR: n.º de figura] |
| `09_igv/capturas_finales/Figura_16_*.png` a `Figura_21_*.png` | IGV (manual) con `09_igv/cargar_igv.batch` | Figuras 16–21 |
| `09_igv/capturas_finales/Figura_26_*.png`, `Figura_27_*.png` | IGV (manual) | Figuras 26 y 27 |
| `10_depth/metricas_submuestreos.tsv` | `scripts/analisis/fig30_profundidad_vs_ensamblado.py` | Análisis 1, métricas [VERIFICAR] |
| `10_depth/quast_comp/` | `scripts/planificados/13_submuestreos_100x_30x.sh` | Análisis 1, QUAST comparativo [VERIFICAR] |
| `10_depth/abricate_vfdb/` | ABRicate (VFDB); sin script | Análisis 1, virulencia por estrategia [VERIFICAR] |
| `figuras/fig23_informe.png` | `scripts/analisis/fig23_informe.R` | [VERIFICAR] |
| `figuras/fig26_prokka_multicopia_ebh.png` | `scripts/analisis/fig26_prokka_multicopia_ebh.py` | [VERIFICAR] |
| `figuras/fig27_blast_multicopia.png` | `scripts/analisis/fig27_blast_multicopia.py` | [VERIFICAR] |
| `figuras/fig28_copias_estimadas.png` | `scripts/analisis/fig28_copias_estimadas.py` | [VERIFICAR] |
| `figuras/fig29A_mapa.png`, `fig29B_gc.png` | `scripts/analisis/fig29_contexto_genomico.py` | [VERIFICAR] |
| `figuras/fig30.png` | `scripts/analisis/fig30_profundidad_vs_ensamblado.py` | [VERIFICAR] |
| `figuras/FigX_gc_cobertura.png` | `scripts/analisis/analisis_contigs_gc_cobertura.R` | [VERIFICAR] |
| `envs/*.yml`, `logs/conda_list_tif_bioinfo3.txt` | `scripts/envs/exportar_entornos.sh` | Entorno de software (Sec. 3.2) [VERIFICAR] |
