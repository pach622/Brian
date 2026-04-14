"""Analyze which sentences each algorithm prefers (position in abstract)."""
import json
from collections import defaultdict, Counter
from abstracts import ABSTRACTS
from summarize import split_sentences, ALGORITHMS

# For each algorithm, track which sentence positions are picked
pos_counts = defaultdict(Counter)

for a in ABSTRACTS:
    sentences = split_sentences(a["abstract"])
    n = len(sentences)
    for algo, fn in ALGORITHMS.items():
        selected = fn(a["abstract"], n_sentences=3)
        for s in selected:
            try:
                idx = sentences.index(s)
                # Bucket by relative position
                pos_frac = idx / max(1, n - 1)
                if pos_frac < 0.33:
                    pos_counts[algo]["opening"] += 1
                elif pos_frac < 0.67:
                    pos_counts[algo]["middle"] += 1
                else:
                    pos_counts[algo]["closing"] += 1
            except ValueError:
                pass

print("Position preferences (fraction of selected sentences):")
print(f"{'Algorithm':<12} {'Opening':>10} {'Middle':>10} {'Closing':>10}")
for algo in ALGORITHMS:
    total = sum(pos_counts[algo].values()) or 1
    o = pos_counts[algo]["opening"] / total
    m = pos_counts[algo]["middle"] / total
    c = pos_counts[algo]["closing"] / total
    print(f"{algo:<12} {o:>10.2%} {m:>10.2%} {c:>10.2%}")

# Save position data
with open("/tmp/nlp-experiment/position_data.json", "w") as f:
    positions = {}
    for algo in ALGORITHMS:
        total = sum(pos_counts[algo].values()) or 1
        positions[algo] = {
            "opening": pos_counts[algo]["opening"] / total,
            "middle": pos_counts[algo]["middle"] / total,
            "closing": pos_counts[algo]["closing"] / total,
        }
    json.dump(positions, f, indent=2)
    print(f"\nSaved to /tmp/nlp-experiment/position_data.json")

# Also verify how often each algorithm includes the last sentence
print("\nFraction of abstracts where summary includes the FINAL sentence:")
for algo, fn in ALGORITHMS.items():
    hits = 0
    for a in ABSTRACTS:
        sentences = split_sentences(a["abstract"])
        selected = fn(a["abstract"], n_sentences=3)
        if sentences and sentences[-1] in selected:
            hits += 1
    print(f"  {algo:<12} {hits}/{len(ABSTRACTS)} ({hits/len(ABSTRACTS):.1%})")
