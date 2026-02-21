# Method

## Overview

This pipeline uses [DocETL](https://github.com/ucbepic/docetl) to extract, deduplicate, and synthesize themes from a corpus of web-scraped documents. DocETL orchestrates a sequence of LLM-powered and non-LLM operations defined in a declarative YAML pipeline.

## Pipeline Architecture

The pipeline follows a four-stage architecture:

```
Map (LLM) → Unnest → Resolve (LLM) → Reduce (LLM)
```

### Stage 1: Theme Extraction (Map)

Each document is processed independently by the LLM to extract 3–5 themes. For each theme, the model returns:

- A short canonical phrase (2–5 words)
- A verbatim quote from the source text supporting the theme
- A content type classification (`article`, `minimal`, or `error`)
- A brief content summary

Documents that are inaccessible (e.g., access-denied pages) are tagged as `error` and filtered in downstream analysis.

### Stage 2: Unnest

The list of themes per document is flattened so each theme becomes its own row, preserving the source URL, verbatim quote, and document metadata. This transforms the data from one-row-per-document to one-row-per-theme.

### Stage 3: Deduplication and Merging (Resolve)

Semantically similar themes across documents are identified and merged using DocETL's resolve operation:

1. **Blocking**: Embedding-based similarity (using `text-embedding-3-large`) filters candidate pairs above a cosine similarity threshold (0.4), avoiding exhaustive pairwise comparison.
2. **Comparison**: An LLM evaluates each candidate pair to determine if two themes refer to the same concept, even when worded differently (e.g., "perseverance" vs. "overcoming adversity").
3. **Resolution**: Matched themes are merged under a single canonical name via an LLM prompt.
4. **Post-processing**: A deterministic code step ensures singleton themes (those not matched with any other) retain their original short theme name rather than defaulting to a summary string.

### Stage 4: Synthesis (Reduce)

Themes are grouped by their canonical name. For each group, the LLM produces:

- A narrative synthesis of how the theme manifests across sources
- The list of source URLs where the theme was found
- The most illustrative verbatim quotes

## Configuration

- **LLM**: Azure OpenAI (`gpt-4.1-2025-04-14`) via LiteLLM
- **Embedding model**: Azure OpenAI (`text-embedding-3-large-1`)
- **Blocking threshold**: 0.4 cosine similarity
- **Intermediate checkpoints**: Saved after each stage for inspection and reproducibility

## Outputs

| File | Description |
|------|-------------|
| `results/theme_results.json` | Structured JSON with all theme reports, sources, and quotes |
| `results/theme_report.md` | Human-readable markdown report generated from the JSON |
| `results/theme_analysis.png` | Bar chart of theme prevalence and source coverage |
| `results/intermediate/` | Per-stage checkpoint files |

## Limitations

- Theme quality depends on the completeness and diversity of the input corpus. With few documents or highly diverse sources, most themes will be single-source.
- The deduplication threshold (0.4) balances recall against false merges. Lower values catch more semantic overlaps but risk merging distinct concepts.
- Verbatim quotes are LLM-extracted and may occasionally be paraphrased rather than exact copies.
