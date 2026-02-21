import json
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "Helvetica Neue",
    "font.size": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

with open("results/theme_results.json") as f:
    results = json.load(f)

results = [r for r in results if r["canonical_theme"] != "access_denied"]
results.sort(key=lambda r: r["_counts_prereduce_summarize_themes"], reverse=True)

themes = [r["canonical_theme"] for r in results]
counts = [r["_counts_prereduce_summarize_themes"] for r in results]
n_sources = [len(r["source_urls"]) for r in results]

fig, ax = plt.subplots(figsize=(12, 10))

y = np.arange(len(themes))
bar_colors = ["#1b4332" if s > 1 else "#74c69d" for s in n_sources]

ax.barh(y, counts, color=bar_colors, height=0.65, edgecolor="none")
ax.set_yticks(y)
ax.set_yticklabels(themes, fontsize=14)
ax.invert_yaxis()
ax.set_xlabel("Merged theme mentions (raw extractions to canonical theme)",
              fontsize=13, labelpad=12)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", labelsize=12)
ax.set_xlim(0, max(counts) + 1.8)
ax.set_title("Theme Prevalence Across Ultramarathon Sources",
             fontsize=20, fontweight="bold", loc="left", pad=20)

for i, (c, s) in enumerate(zip(counts, n_sources)):
    label = f"{s} doc" if s == 1 else f"{s} docs"
    ax.text(c + 0.15, i, label, va="center", fontsize=12, color="#555")

legend_elements = [
    plt.Rectangle((0, 0), 1, 1, fc="#1b4332",
                  label="Cross-document (2+ sources)"),
    plt.Rectangle((0, 0), 1, 1, fc="#74c69d",
                  label="Single document"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=13,
          frameon=False, handlelength=1.2, handleheight=1.2)

plt.savefig("results/theme_analysis.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.savefig("results/theme_analysis.pdf", bbox_inches="tight", facecolor="white")
print("Saved: theme_analysis.png and theme_analysis.pdf")
