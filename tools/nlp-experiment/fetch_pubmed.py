"""Fetch PubMed abstracts with full-text article bodies for summarization experiment.

Uses NCBI E-utilities (esearch + efetch). No API key needed for small volumes.
"""
import json
import time
import urllib.parse
import requests
import xml.etree.ElementTree as ET

QUERY = "machine learning medical diagnosis"
N_RESULTS = 30
OUTFILE = "/tmp/nlp-experiment/pubmed_abstracts.json"

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def search(query, n):
    url = f"{BASE}/esearch.fcgi"
    r = requests.get(url, params={
        "db": "pubmed",
        "term": query,
        "retmax": n,
        "retmode": "json",
        "sort": "relevance",
    }, timeout=30)
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"]

def fetch_abstracts(ids):
    url = f"{BASE}/efetch.fcgi"
    r = requests.get(url, params={
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
    }, timeout=60)
    r.raise_for_status()
    return r.text

def parse_pubmed_xml(xml_text):
    root = ET.fromstring(xml_text)
    articles = []
    for art in root.findall(".//PubmedArticle"):
        try:
            title_elem = art.find(".//ArticleTitle")
            title = "".join(title_elem.itertext()) if title_elem is not None else ""

            # Collect abstract sections — some abstracts are structured (Background/Methods/Results)
            abs_parts = []
            for ab in art.findall(".//Abstract/AbstractText"):
                label = ab.get("Label", "")
                text = "".join(ab.itertext())
                if label:
                    abs_parts.append(f"{label}: {text}")
                else:
                    abs_parts.append(text)
            full_abstract = " ".join(abs_parts).strip()

            pmid_elem = art.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else ""

            year_elem = art.find(".//PubDate/Year")
            year = year_elem.text if year_elem is not None else ""

            if full_abstract and len(full_abstract.split()) >= 150:
                articles.append({
                    "pmid": pmid,
                    "title": title.strip(),
                    "abstract": full_abstract,
                    "year": year,
                    "word_count": len(full_abstract.split()),
                })
        except Exception as e:
            print(f"Skipping one article: {e}")
    return articles

def main():
    print(f"Searching PubMed for: '{QUERY}'...")
    ids = search(QUERY, N_RESULTS)
    print(f"Found {len(ids)} IDs")

    time.sleep(0.5)

    print("Fetching abstracts...")
    xml_text = fetch_abstracts(ids)

    print("Parsing...")
    articles = parse_pubmed_xml(xml_text)
    print(f"Got {len(articles)} usable articles with abstracts >= 150 words")

    with open(OUTFILE, "w") as f:
        json.dump(articles, f, indent=2)
    print(f"Saved to {OUTFILE}")

    if articles:
        word_counts = [a["word_count"] for a in articles]
        print(f"Word count stats: min={min(word_counts)}, max={max(word_counts)}, avg={sum(word_counts)//len(word_counts)}")

if __name__ == "__main__":
    main()
