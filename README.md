# Document Theme Extraction

LLM-powered pipeline for extracting, deduplicating, and synthesizing themes from a corpus of documents. Built with [DocETL](https://github.com/ucbepic/docetl) and Azure OpenAI.

## Quick Start

```bash
# Create environment and install
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Set credentials (see .env.example)
cp .env.example .env  # then fill in your keys

# Run the pipeline
docetl run pipeline.yaml

# Generate report and visualization
python scripts/generate_report.py
python scripts/visualize_themes.py
```

## Project Structure

```
├── pipeline.yaml           # DocETL pipeline definition
├── requirements.txt        # Python dependencies
├── scripts/
│   ├── generate_report.py  # JSON → Markdown report
│   └── visualize_themes.py # JSON → Chart
├── data/                   # Input documents (gitignored)
│   └── dataset.json
├── results/                # All outputs (gitignored)
│   ├── theme_results.json
│   ├── theme_report.md
│   ├── theme_analysis.png
│   └── intermediate/
├── METHOD.md               # Pipeline methodology
└── CLAUDE.md               # AI assistant context
```

## Pipeline

```
Extract themes + quotes (Map)
        ↓
Flatten to one row per theme (Unnest)
        ↓
Deduplicate similar themes (Resolve)
        ↓
Synthesize per theme with sources (Reduce)
```

See [METHOD.md](METHOD.md) for full details.

## Configuration

The pipeline uses Azure OpenAI via LiteLLM. Set the following in `.env`:

```
AZURE_API_KEY=your_key
AZURE_API_BASE=your_endpoint
AZURE_API_VERSION=2024-12-01-preview
```

Model and embedding settings are configured in `pipeline.yaml`.

## License

MIT
