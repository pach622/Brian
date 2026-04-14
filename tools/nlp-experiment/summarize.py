"""Four extractive summarization algorithms implemented from scratch.

No neural models, no external summarization libraries - just numpy.
Input: an abstract. Output: the top-N most informative sentences, in original
order.

Algorithms:
1. Luhn (1958)       - word-frequency scoring, classic baseline
2. TextRank (2004)   - PageRank over sentence-similarity graph
3. LexRank (2004)    - eigenvector centrality on thresholded cosine-similarity graph
4. LSA (2001)        - top-K sentences from the singular value decomposition

Utilities: sentence splitter, tokenizer, stopword list, TF-IDF, ROUGE-N, ROUGE-L.
"""
import re
import string
import math
from collections import Counter
import numpy as np

# --- Stopwords: a practical English list (~180 words) ---
STOPWORDS = set("""
a an the and or but if while of to in on at by for with from as is are was were
be been being have has had do does did will would could should may might must
can shall this that these those i you he she it we they them him her his their
our its my your me us not no nor so than then there here when where why how
which who whom whose what all any both each few more most other some such only
own same too very s t can just don now also into over under between against
during before after above below because about against through during before
after between
""".split())


# --- Text processing utilities ---
SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9])')
TOKEN_RE = re.compile(r"[a-zA-Z]+")

def split_sentences(text):
    text = text.strip()
    if not text:
        return []
    sentences = SENT_SPLIT_RE.split(text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]

def tokenize(text, remove_stopwords=True):
    tokens = [t.lower() for t in TOKEN_RE.findall(text)]
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return tokens

def tf_idf_matrix(sentences):
    """Build a sentence x vocab TF-IDF matrix."""
    tokenized = [tokenize(s) for s in sentences]
    vocab = sorted(set(w for sent in tokenized for w in sent))
    v_idx = {w: i for i, w in enumerate(vocab)}
    n_sent = len(sentences)

    tf = np.zeros((n_sent, len(vocab)))
    for i, sent_tokens in enumerate(tokenized):
        if not sent_tokens:
            continue
        counts = Counter(sent_tokens)
        total = sum(counts.values())
        for w, c in counts.items():
            tf[i, v_idx[w]] = c / total

    df = np.zeros(len(vocab))
    for sent_tokens in tokenized:
        for w in set(sent_tokens):
            df[v_idx[w]] += 1
    idf = np.log((n_sent + 1) / (df + 1)) + 1  # smoothed idf

    return tf * idf


# --- Algorithm 1: Luhn (1958) ---
def summarize_luhn(text, n_sentences=3):
    """Score sentences by the density of high-frequency content words."""
    sentences = split_sentences(text)
    if len(sentences) <= n_sentences:
        return sentences

    all_tokens = tokenize(text)
    freq = Counter(all_tokens)
    # "Significant" words: top quartile by frequency, excluding very rare words
    cutoff = max(2, sorted(freq.values(), reverse=True)[len(freq) // 4])
    significant = {w for w, c in freq.items() if c >= cutoff}

    scores = []
    for s in sentences:
        tokens = tokenize(s, remove_stopwords=False)
        sig_positions = [i for i, t in enumerate(tokens) if t in significant]
        if len(sig_positions) < 2:
            scores.append(0)
            continue
        # Luhn's formula: square of count of significant words divided by
        # the span containing them
        span = sig_positions[-1] - sig_positions[0] + 1
        score = (len(sig_positions) ** 2) / span
        scores.append(score)

    # Pick top-N but return in original order
    top_idx = sorted(sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_sentences])
    return [sentences[i] for i in top_idx]


# --- Algorithm 2: TextRank (Mihalcea & Tarau, 2004) ---
def summarize_textrank(text, n_sentences=3, damping=0.85, tol=1e-4, max_iter=100):
    """PageRank-style ranking of sentences by a cosine similarity graph."""
    sentences = split_sentences(text)
    if len(sentences) <= n_sentences:
        return sentences

    mat = tf_idf_matrix(sentences)
    # Cosine similarity
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = mat / norms
    sim = normalized @ normalized.T
    np.fill_diagonal(sim, 0)  # no self-similarity

    # Row-normalize into a transition matrix
    row_sums = sim.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    M = sim / row_sums

    n = len(sentences)
    scores = np.ones(n) / n
    for _ in range(max_iter):
        new_scores = (1 - damping) / n + damping * (M.T @ scores)
        if np.linalg.norm(new_scores - scores) < tol:
            break
        scores = new_scores

    top_idx = sorted(sorted(range(n), key=lambda i: scores[i], reverse=True)[:n_sentences])
    return [sentences[i] for i in top_idx]


# --- Algorithm 3: LexRank (Erkan & Radev, 2004) ---
def summarize_lexrank(text, n_sentences=3, threshold=0.1, tol=1e-4, max_iter=100):
    """Power iteration on thresholded binary similarity graph."""
    sentences = split_sentences(text)
    if len(sentences) <= n_sentences:
        return sentences

    mat = tf_idf_matrix(sentences)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = mat / norms
    sim = normalized @ normalized.T

    # Threshold: only keep edges above the similarity threshold
    adj = (sim >= threshold).astype(float)
    np.fill_diagonal(adj, 0)

    # Normalize to make it a stochastic matrix
    row_sums = adj.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    M = adj / row_sums

    n = len(sentences)
    scores = np.ones(n) / n
    for _ in range(max_iter):
        new_scores = M.T @ scores
        new_scores = new_scores / new_scores.sum()  # renormalize
        if np.linalg.norm(new_scores - scores) < tol:
            break
        scores = new_scores

    top_idx = sorted(sorted(range(n), key=lambda i: scores[i], reverse=True)[:n_sentences])
    return [sentences[i] for i in top_idx]


# --- Algorithm 4: LSA (Steinberger & Jezek, 2004) ---
def summarize_lsa(text, n_sentences=3):
    """Rank sentences by strength in the top singular vectors of TF-IDF matrix."""
    sentences = split_sentences(text)
    if len(sentences) <= n_sentences:
        return sentences

    mat = tf_idf_matrix(sentences)  # shape (n_sent, vocab)
    # SVD: mat = U @ diag(S) @ Vt. Rows of U are sentences in latent space.
    try:
        U, S, Vt = np.linalg.svd(mat, full_matrices=False)
    except np.linalg.LinAlgError:
        return sentences[:n_sentences]

    # Keep top k singular values corresponding to the "topics"
    k = min(n_sentences, len(S))
    # For each sentence, score by the weighted length of its projection
    # onto the top-k topic space
    sent_scores = np.sqrt((U[:, :k] ** 2 * (S[:k] ** 2)).sum(axis=1))

    top_idx = sorted(sorted(range(len(sentences)), key=lambda i: sent_scores[i], reverse=True)[:n_sentences])
    return [sentences[i] for i in top_idx]


# --- ROUGE from scratch ---
def _n_grams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def rouge_n(reference, candidate, n=1):
    """ROUGE-N F1 between reference and candidate strings."""
    ref_tokens = tokenize(reference, remove_stopwords=False)
    cand_tokens = tokenize(candidate, remove_stopwords=False)
    ref_ngrams = Counter(_n_grams(ref_tokens, n))
    cand_ngrams = Counter(_n_grams(cand_tokens, n))

    overlap = sum((ref_ngrams & cand_ngrams).values())
    if overlap == 0:
        return 0.0

    precision = overlap / max(1, sum(cand_ngrams.values()))
    recall = overlap / max(1, sum(ref_ngrams.values()))
    return 2 * precision * recall / (precision + recall)

def _lcs_length(a, b):
    """Length of the longest common subsequence (LCS) of token lists a and b."""
    if not a or not b:
        return 0
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
    return dp[m][n]

def rouge_l(reference, candidate):
    """ROUGE-L F1 based on longest common subsequence."""
    ref_tokens = tokenize(reference, remove_stopwords=False)
    cand_tokens = tokenize(candidate, remove_stopwords=False)
    lcs = _lcs_length(ref_tokens, cand_tokens)
    if lcs == 0:
        return 0.0
    precision = lcs / len(cand_tokens)
    recall = lcs / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)


# --- Additional metrics ---
def compression_ratio(original, summary):
    ow = len(tokenize(original, remove_stopwords=False))
    sw = len(tokenize(summary, remove_stopwords=False))
    return sw / max(1, ow)


ALGORITHMS = {
    "Luhn": summarize_luhn,
    "TextRank": summarize_textrank,
    "LexRank": summarize_lexrank,
    "LSA": summarize_lsa,
}
