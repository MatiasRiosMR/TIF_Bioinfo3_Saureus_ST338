# 10_depth: efecto de la profundidad y del modo de SPAdes

## Propósito
Comparar el ensamblado completo (≈800×) con submuestreos de ≈100× y ≈30× ensamblados con `--isolate` (`_iso`) y `--careful` (`_car`),
y evaluar con QUAST y ABRicate (VFDB). Además contiene la prueba con el 5 % de los pares.

## Herramientas
seqtk 1.5 (`sample -s 42`), SPAdes 4.3.0, QUAST 5.3.0 (`quast_env`), ABRicate [VERIFICAR: versión].

## Generado por
- `scripts/06_spades_prueba_5pct.sh` → `test_R{1,2}.fq.gz`, `test/`.
- `scripts/planificados/13_submuestreos_100x_30x.sh` → `S1_{100x,30x}_R{1,2}.fq.gz` (fracciones 0,1311 y 0,0393), `S1_{100x,30x}_{iso,car}/`
  y `quast_comp/` (cabecera "PLANIFICADO"; las salidas existen [VERIFICAR: ejecución tal cual]). Tiempos: `logs/spades_*.time`.
- `metricas_submuestreos.tsv` → `scripts/analisis/fig30_profundidad_vs_ensamblado.py` (a partir de `quast_comp/report.tsv`).
- `abricate_vfdb/` → ABRicate con la base VFDB sobre cada `contigs.fasta` [VERIFICAR: comando; no está en los scripts].

## Archivos
| Ruta | Contenido |
|---|---|
| `metricas_submuestreos.tsv` | `ensamblado N50 NGA50 # contigs (>= 0 bp) Total length Genome fraction (%) # misassemblies`; 6 filas: completo, filtrado, 100x_iso, 100x_car, 30x_iso, 30x_car |
| `quast_comp/` | QUAST de los 6 ensamblados vs MRSA252 (`report.tsv`, `transposed_report.tsv`, html, pdf) |
| `S1_*/contigs.fasta`, `spades.log`, `params.txt`, etc. | Ensamblados por estrategia |
| `abricate_vfdb/S1_{100x,30x}_{iso,car}_vfdb.tsv` | Hits VFDB, mismas columnas que `08_genes_mge/abricate_vfdb_S1.tsv` |

Tamaño: ≈1 GB en disco (≈0,45 GB versionable: ensamblados y `quast_comp` 44 MB).

## Excluido por .gitignore
`*.fq.gz` (lecturas submuestreadas), `test/` (ensamblado de prueba), intermedios de SPAdes (`K*/`, `corrected/`, `scaffolds.*`, grafos, etc.) e `icarus_viewers/`.
Regenerar: ejecutar el script 13 (requiere `02_trim/`).

## Resultados clave (`metricas_submuestreos.tsv`)
N50: completo 43 072; filtrado 70 746; 100× iso 98 457; 30× iso 102 908. Fracción de MRSA252: 85,4–86,2 % en todas las estrategias.

## Correspondencia con el informe
Sección 2.9 (Análisis 1); figura de métricas (`figuras/fig30.png`, `figuras/fig23_informe.png`) [VERIFICAR: tablas y figuras].
