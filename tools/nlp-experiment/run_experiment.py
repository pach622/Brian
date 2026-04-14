"""Run all summarization algorithms on the abstract corpus and collect metrics."""
import json
import time
from statistics import mean, stdev
from collections import defaultdict

from abstracts import ABSTRACTS
from summarize import (
    ALGORITHMS, rouge_n, rouge_l,
    compression_ratio, tokenize, split_sentences,
)

N_SENTENCES = 3

def run_one(abstract, conclusion):
    per_algo = {}
    for name, fn in ALGORITHMS.items():
        start = time.perf_counter()
        summary_sents = fn(abstract, n_sentences=N_SENTENCES)
        elapsed = time.perf_counter() - start
        summary = " ".join(summary_sents)
        per_algo[name] = {
            "summary": summary,
            "summary_sentences": summary_sents,
            "elapsed_ms": elapsed * 1000,
            "rouge1": rouge_n(conclusion, summary, n=1),
            "rouge2": rouge_n(conclusion, summary, n=2),
            "rougeL": rouge_l(conclusion, summary),
            "compression": compression_ratio(abstract, summary),
        }
    return per_algo

def main():
    print(f"Running 4 algorithms on {len(ABSTRACTS)} real PubMed abstracts...")
    print(f"Target summary length: {N_SENTENCES} sentences")
    print("Reference: each abstract's final 'Conclusion' sentence (author-written)")
    print()

    all_results = []
    per_algo_scores = defaultdict(lambda: defaultdict(list))

    for i, a in enumerate(ABSTRACTS):
        results = run_one(a["abstract"], a["conclusion"])
        all_results.append({
            "pmid": a["pmid"],
            "topic": a["topic"],
            "word_count": len(a["abstract"].split()),
            "results": results,
        })
        for algo, metrics in results.items():
            for m, v in metrics.items():
                if isinstance(v, (int, float)):
                    per_algo_scores[algo][m].append(v)
        print(f"  [{i+1}/{len(ABSTRACTS)}] PMID {a['pmid']} - {a['topic']}")

    # Aggregate
    print("\n" + "=" * 72)
    print(f"{'Algorithm':<12} {'ROUGE-1':>10} {'ROUGE-2':>10} {'ROUGE-L':>10} {'Time (ms)':>12} {'Compress':>10}")
    print("=" * 72)
    summary_table = {}
    for algo in ALGORITHMS:
        r1 = mean(per_algo_scores[algo]["rouge1"])
        r2 = mean(per_algo_scores[algo]["rouge2"])
        rl = mean(per_algo_scores[algo]["rougeL"])
        t = mean(per_algo_scores[algo]["elapsed_ms"])
        c = mean(per_algo_scores[algo]["compression"])
        print(f"{algo:<12} {r1:>10.3f} {r2:>10.3f} {rl:>10.3f} {t:>12.2f} {c:>10.3f}")
        summary_table[algo] = {
            "rouge1_mean": r1, "rouge1_std": stdev(per_algo_scores[algo]["rouge1"]),
            "rouge2_mean": r2, "rouge2_std": stdev(per_algo_scores[algo]["rouge2"]),
            "rougeL_mean": rl, "rougeL_std": stdev(per_algo_scores[algo]["rougeL"]),
            "time_ms_mean": t, "time_ms_std": stdev(per_algo_scores[algo]["elapsed_ms"]),
            "compression_mean": c,
        }
    print()

    # Save everything to a JSON file for the article
    with open("/tmp/nlp-experiment/results.json", "w") as f:
        json.dump({
            "summary": summary_table,
            "per_paper": all_results,
            "n_abstracts": len(ABSTRACTS),
            "n_sentences": N_SENTENCES,
        }, f, indent=2)
    print(f"Saved detailed results to /tmp/nlp-experiment/results.json")

    # Print one example comparison
    print("\n" + "=" * 72)
    print("EXAMPLE: Abstract", all_results[0]["pmid"], "-", all_results[0]["topic"])
    print("=" * 72)
    print("\n[Reference (author's conclusion)]")
    print(ABSTRACTS[0]["conclusion"])
    for algo in ALGORITHMS:
        print(f"\n[{algo}]")
        print(all_results[0]["results"][algo]["summary"])

if __name__ == "__main__":
    main()
