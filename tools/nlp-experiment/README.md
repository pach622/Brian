# NLP Scientific Summarization Experiment

Code for the article [Summarizing Scientific Abstracts: Do We Really Need LLMs?](https://brianphchan.com/caseStudies/scientificSummarization).

## Running

```
python3 run_experiment.py    # runs all 4 algorithms on 12 abstracts, prints table
python3 analyze_results.py   # additional analysis: sentence position preferences
```

Only dependency is `numpy`. No neural models, no internet access needed.

## Files

- `abstracts.py` — the 12 biomedical ML abstracts used as the corpus.
- `summarize.py` — Luhn, TextRank, LexRank, LSA, plus ROUGE-N and ROUGE-L, all from scratch.
- `run_experiment.py` — runs everything, prints the summary table, saves `results.json`.
- `analyze_results.py` — additional breakdown of which sentence positions each algorithm prefers.
- `fetch_pubmed.py` — a script to fetch fresh abstracts from NCBI if you want to extend the corpus (requires internet access to `eutils.ncbi.nlm.nih.gov`).
- `results.json` — cached results from the experiment run featured in the article.
