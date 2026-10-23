# 03_assembly: ensamblado de novo

## Propósito
Ensamblado de las lecturas recortadas con SPAdes y ensamblado filtrado usado en la anotación y la tipificación.

## Herramientas
SPAdes 4.3.0 (modo `--isolate`, Python 3.14.7), entorno `tif_bioinfo3`. El filtro usa `awk`.

## Generado por
- `scripts/07_spades_completo.sh` → `S1_full/` (22 min 39 s, 4,6 GB de memoria máxima según `logs/spades_full.time`).
- `scripts/11_filtrar_cov100.sh` → `S1_full/contigs_cov100.fasta`.
Prueba previa con el 5 % de los pares: `scripts/06_spades_prueba_5pct.sh` (salida en `10_depth/test/`, no versionada).

## Archivos (en `S1_full/`)
| Archivo | Contenido |
|---|---|
| `contigs.fasta` | 17 258 contigs; encabezado `NODE_<n>_length_<L>_cov_<C>` (C = cobertura de k-mers) |
| `contigs_cov100.fasta`, `.fai` | 74 contigs de ≥500 pb con cobertura de k-mers ≥100 (2 790 840 pb) |
| `contigs.paths` | Caminos de los contigs en el grafo |
| `spades.log`, `params.txt`, `run_spades.sh`, `run_spades.yaml`, `dataset.info`, `input_dataset.yaml` | Registro y parámetros de la corrida |

Tamaño: 151 MB en disco (sin versionar los intermedios).

## Excluido por .gitignore
`K*/`, `tmp/`, `corrected/`, `misc/`, `pipeline_state/`, `mismatch_corrector/`, `assembly_graph*`, `before_rr.fasta` y `scaffolds.*`.
Se regeneran ejecutando de nuevo `scripts/07_spades_completo.sh` (requiere `02_trim/`).

## Nota
`spades.log`, `params.txt` y `run_spades.*` conservan rutas absolutas de la máquina de origen (generadas por SPAdes).

## Correspondencia con el informe
Sección de ensamblado (2.3) y de filtrado (2.4); tablas de métricas de SPAdes/QUAST.
