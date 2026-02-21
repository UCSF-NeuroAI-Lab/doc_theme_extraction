# CLAUDE.md

## Project

Document theme extraction pipeline using DocETL with Azure OpenAI (UCSF VERSA endpoint).

## Setup

```bash
uv venv && source .venv/bin/activate
pip install docetl
pip install "pyrate-limiter==3.7.0"
```

## Credentials

All in `.env`, auto-loaded by DocETL:

- `AZURE_API_KEY` — VERSA API key (base64-encoded)
- `AZURE_API_BASE` — `https://unified-api.ucsf.edu/general`
- `AZURE_API_VERSION` — `2024-12-01-preview`

## Models

- LLM: `azure/gpt-4.1-2025-04-14`
- Embeddings: `azure/text-embedding-3-large-1`

## Running

```bash
docetl run pipeline.yaml          # run pipeline, outputs to results/
python generate_report.py         # JSON → markdown report
python visualize_themes.py        # JSON → chart
```

## Pipeline stages

1. `extract_themes` (map) — LLM extracts themes + verbatim quotes per document
2. `unnest_themes` (unnest) — flattens to one row per theme
3. `deduplicate_themes` (resolve) — embedding-based blocking + LLM merge
4. `fix_canonical_theme` (code_map) — fixes singleton theme names
5. `summarize_themes` (reduce) — groups by theme, synthesizes with sources + quotes

## Key files

- `pipeline.yaml` — pipeline definition
- `data/dataset.json` — input documents
- `results/` — all outputs (JSON, markdown, charts, intermediates)
- `METHOD.md` — methodology documentation

## Notes

- DocETL uses LiteLLM; Azure models use `azure/` prefix
- `pyrate-limiter==3.7.0` is required (v2.x and v4.x break imports)
- Blocking threshold is 0.4; lower catches more semantic overlaps
- Intermediates saved at `results/intermediate/` for debugging
