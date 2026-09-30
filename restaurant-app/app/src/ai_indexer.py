"""
AI Indexer for Isarva Restaurant POS User Guide.
Builds an ultra-fast in-memory BM25 inverted index, role index, and structured JSONL chunks.
Target search latency: < 2ms.
"""
import math
import os
import re
from typing import Dict, List, Any
import orjson

from .pos_data_builder import get_pos_full_data

# Common English stop words
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself",
    "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more",
    "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only", "or",
    "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she", "should", "so",
    "some", "such", "t", "than", "that", "the", "their", "theirs", "them", "themselves", "then",
    "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "will", "with", "you", "your", "yours", "yourself", "yourselves"
}

def tokenize(text: str) -> List[str]:
    """Tokenize and normalize text into lowercase alphanumeric tokens."""
    tokens = re.findall(r'[a-zA-Z0-9_\-\./]+', text.lower())
    clean_tokens = []
    for t in tokens:
        # Strip trailing punctuation
        t_clean = t.strip('.-_/')
        if len(t_clean) >= 2 and t_clean not in STOP_WORDS:
            clean_tokens.append(t_clean)
    return clean_tokens

def build_ai_index():
    data = get_pos_full_data()
    chunks = data["chunks"]
    metadata = data["metadata"]
    slides_data = data["slides_data"]

    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(app_dir, "content")
    os.makedirs(content_dir, exist_ok=True)

    # 1. Save dedicated POS slides
    pos_slides_file = os.path.join(content_dir, "pos_slides_data.json")
    with open(pos_slides_file, "wb") as f:
        f.write(orjson.dumps(slides_data, option=orjson.OPT_INDENT_2))

    # Also merge into slides_data.json so CLI --slide POS-X works immediately
    main_slides_file = os.path.join(content_dir, "slides_data.json")
    if os.path.exists(main_slides_file):
        try:
            with open(main_slides_file, "rb") as f:
                existing = orjson.loads(f.read())
        except Exception:
            existing = {}
        existing.update(slides_data)
        with open(main_slides_file, "wb") as f:
            f.write(orjson.dumps(existing, option=orjson.OPT_INDENT_2))

    # 2. Build structured JSONL chunks for Vector / LLM Ingestion
    chunks_jsonl_file = os.path.join(content_dir, "pos_chunks.jsonl")
    with open(chunks_jsonl_file, "wb") as f:
        for ch in chunks:
            # Full text representation
            full_text = f"{ch['part']} | {ch['section']}\n"
            full_text += f"Module: {ch['module']} | Location: {ch['where']}\n"
            full_text += f"Target Roles: {', '.join(ch['target_roles'])}\n"
            full_text += f"Summary: {ch['summary']}\n"
            full_text += "Steps:\n" + "\n".join(ch['steps']) + "\n"
            if ch['key_notes']:
                full_text += "Important Notes:\n" + "\n".join(f"- {n}" for n in ch['key_notes']) + "\n"
            if ch['troubleshooting']:
                full_text += "Troubleshooting:\n" + "\n".join(f"- Q: {t['problem']} -> A: {t['solution']}" for t in ch['troubleshooting']) + "\n"

            record = {
                "id": ch["id"],
                "part": ch["part"],
                "section": ch["section"],
                "module": ch["module"],
                "where": ch["where"],
                "target_roles": ch["target_roles"],
                "summary": ch["summary"],
                "steps": ch["steps"],
                "key_notes": ch["key_notes"],
                "keywords": ch["keywords"],
                "troubleshooting": ch["troubleshooting"],
                "full_text": full_text
            }
            f.write(orjson.dumps(record) + b"\n")

    # 3. Build BM25 Inverted Index & Metadata
    total_docs = len(chunks)
    doc_lengths = {}
    inverted_index: Dict[str, Dict[str, int]] = {}  # term -> {doc_id: freq}
    role_map: Dict[str, List[str]] = {}
    module_map: Dict[str, List[str]] = {}
    troubleshooting_index: List[Dict[str, Any]] = []

    for ch in chunks:
        doc_id = ch["id"]

        # Aggregate searchable text with field weighting
        # We repeat summary, keywords, and section title to give them natural weighting
        weighted_corpus = (
            (ch["section"] + " ") * 3 +
            (ch["summary"] + " ") * 2 +
            " ".join(ch["keywords"]) * 3 +
            " ".join(ch["steps"]) + " " +
            " ".join(ch["key_notes"]) + " " +
            " ".join(ch["target_roles"]) + " " +
            ch["module"] + " " +
            ch["where"]
        )

        tokens = tokenize(weighted_corpus)
        doc_lengths[doc_id] = len(tokens)

        # Count frequencies
        freqs: Dict[str, int] = {}
        for t in tokens:
            freqs[t] = freqs.get(t, 0) + 1

        for term, freq in freqs.items():
            if term not in inverted_index:
                inverted_index[term] = {}
            inverted_index[term][doc_id] = freq

        # Map roles
        for r in ch["target_roles"]:
            r_norm = r.lower()
            if r_norm not in role_map:
                role_map[r_norm] = []
            role_map[r_norm].append(doc_id)

        # Map modules
        m_norm = ch["module"].lower()
        if m_norm not in module_map:
            module_map[m_norm] = []
        module_map[m_norm].append(doc_id)

        # Troubleshooting index
        for t in ch.get("troubleshooting", []):
            troubleshooting_index.append({
                "problem": t["problem"],
                "solution": t["solution"],
                "chunk_id": doc_id,
                "part": ch["part"],
                "section": ch["section"],
                "module": ch["module"],
                "where": ch["where"],
                "target_roles": ch["target_roles"]
            })

    avg_dl = sum(doc_lengths.values()) / max(1, total_docs)

    # Calculate IDF for all terms
    idf_table: Dict[str, float] = {}
    for term, posting in inverted_index.items():
        n_q = len(posting)
        # Standard Lucene/BM25 IDF formula
        idf_table[term] = math.log(1.0 + (total_docs - n_q + 0.5) / (n_q + 0.5))

    index_bundle = {
        "metadata": metadata,
        "total_docs": total_docs,
        "avg_dl": avg_dl,
        "doc_lengths": doc_lengths,
        "idf_table": idf_table,
        "inverted_index": inverted_index,
        "role_map": role_map,
        "module_map": module_map,
        "troubleshooting": troubleshooting_index,
        "chunks": {ch["id"]: ch for ch in chunks}
    }

    index_output_file = os.path.join(content_dir, "pos_knowledge_index.json")
    with open(index_output_file, "wb") as f:
        f.write(orjson.dumps(index_bundle))

    print(f"[SUCCESS] Built AI Knowledge Index:")
    print(f" - Documents indexed: {total_docs}")
    print(f" - Vocabulary size: {len(inverted_index)} distinct terms")
    print(f" - Troubleshooting rules: {len(troubleshooting_index)}")
    print(f" - Slide definitions saved: {pos_slides_file}")
    print(f" - Chunks JSONL saved: {chunks_jsonl_file}")
    print(f" - Compiled binary index: {index_output_file}")
    return index_output_file

if __name__ == "__main__":
    build_ai_index()
