#!/usr/bin/env python3
"""Rank extracted grammar/article pages for phonotactics-distribution mining.

Input is plain text with form-feed page separators (pdftotext -layout output works
well). The script is deliberately conservative: it only prioritizes pages and emits
matched cues; it does not extract or invent linguistic records.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

CUES = {
    "syllable_structure": (4, [r"syllable structure", r"syllable template", r"\bonset(s)?\b", r"\bcoda(s)?\b", r"\bnucleus\b"]),
    "clusters": (4, [r"consonant cluster", r"cluster(s)?", r"phonotactic(s)?", r"co[- ]?occurr"]),
    "edges_position": (3, [r"word[- ]initial", r"word[- ]final", r"initial position", r"final position", r"intervocalic", r"position(al)? neutral"]),
    "harmony": (4, [r"vowel harmony", r"consonant harmony", r"harmony domain", r"harmoni[sz]"]),
    "prosody": (3, [r"\bstress\b", r"\btone\b", r"prosodic word", r"foot(ing)?", r"heavy syllable", r"mora"]),
    "distribution": (3, [r"distribution", r"complementary distribution", r"allophon", r"restricted to", r"occur(s|ring)? only", r"cannot occur"]),
    "morph_domain": (3, [r"morpheme boundary", r"suffix", r"prefix", r"root[- ]initial", r"lexical stratum", r"domain"]),
    "exceptions": (3, [r"exception", r"counterexample", r"loan(word)?", r"marginal", r"rare(ly)?", r"unattested", r"accidental gap", r"productive"]),
    "tables_formalism": (2, [r"table\s+\d+", r"figure\s+\d+", r"\*#?[CV]", r"->|→", r"/__|__/"]),
}


def rank_pages(text: str):
    pages = text.split("\f")
    out = []
    for page_no, page in enumerate(pages, start=1):
        low = page.lower()
        score = 0
        hits = defaultdict(list)
        for category, (weight, patterns) in CUES.items():
            for pat in patterns:
                found = re.findall(pat, low, flags=re.I)
                if found:
                    n = len(found)
                    score += weight * min(n, 4)
                    hits[category].append({"pattern": pat, "count": n})
        # Bonus for cue diversity, which tends to surface descriptive sections rather
        # than isolated mentions in bibliographies or discussion.
        score += 2 * max(0, len(hits) - 1)
        if score:
            out.append({
                "page": page_no,
                "score": score,
                "cue_categories": sorted(hits),
                "hits": dict(hits),
                "preview": re.sub(r"\s+", " ", page).strip()[:500],
            })
    return sorted(out, key=lambda x: (-x["score"], x["page"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="form-feed-separated extracted text")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--json", action="store_true", help="emit JSONL rather than TSV")
    args = ap.parse_args()
    ranked = rank_pages(args.input.read_text(encoding="utf-8", errors="replace"))[: args.top]
    if args.json:
        for row in ranked:
            print(json.dumps(row, ensure_ascii=False))
    else:
        print("page\tscore\tcues\tpreview")
        for row in ranked:
            preview = row["preview"].replace("\t", " ")
            print(f"{row['page']}\t{row['score']}\t{','.join(row['cue_categories'])}\t{preview}")


if __name__ == "__main__":
    main()
