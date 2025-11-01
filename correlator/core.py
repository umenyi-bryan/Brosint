from collections import defaultdict

def correlate(evidence):
    grouped = defaultdict(list)
    for e in evidence:
        grouped[e.get("source")].append(e)
    hypotheses = []
    for src, evs in grouped.items():
        score = sum(20 for e in evs if e["type"] in ["breach","profile_found"])
        hypotheses.append({
            "identity": src,
            "confidence": min(100, score),
            "signals": evs
        })
    return {"summary": {"sources": len(grouped)}, "hypotheses": hypotheses}
