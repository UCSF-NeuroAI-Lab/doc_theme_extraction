import json
import textwrap

with open("results/theme_results.json") as f:
    results = json.load(f)

results = [r for r in results if r["canonical_theme"] != "access_denied"]
results.sort(key=lambda r: r["_counts_prereduce_summarize_themes"], reverse=True)

lines = ["# Theme Extraction Report\n"]

multi = sum(1 for r in results if len(r["source_urls"]) > 1)
lines.append(f"**{len(results)} themes** extracted from "
             f"{len({u for r in results for u in r['source_urls']})} documents "
             f"({multi} cross-document, {len(results) - multi} single-document)\n")
lines.append("---\n")

for r in results:
    n_src = len(r["source_urls"])
    tag = "cross-document" if n_src > 1 else "single-document"
    mentions = r["_counts_prereduce_summarize_themes"]

    lines.append(f"## {r['canonical_theme']}")
    lines.append(f"*{mentions} mention(s) · {n_src} source(s) · {tag}*\n")
    lines.append(r["theme_report"] + "\n")

    lines.append("### Sources\n")
    for url in r["source_urls"]:
        lines.append(f"- {url}")
    lines.append("")

    lines.append("### Verbatim Quotes\n")
    for q in r["verbatim_examples"]:
        lines.append(f"> {q}\n")

    lines.append("---\n")

with open("results/theme_report.md", "w") as f:
    f.write("\n".join(lines))

print(f"Saved: theme_report.md ({len(results)} themes)")
