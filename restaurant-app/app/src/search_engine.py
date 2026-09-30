"""
Ultra-Fast AI Search Engine for Isarva Restaurant POS.
Executes sub-2ms BM25 ranking, role/module filtering, troubleshooting lookup,
and LLM Context Prompt building.
"""
import os
import re
import time
from typing import Dict, List, Any, Optional, Tuple
import orjson

from .ai_indexer import tokenize, build_ai_index

class POSSearchEngine:
    _instance = None

    def __init__(self, index_path: Optional[str] = None):
        if not index_path:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            index_path = os.path.join(app_dir, "content", "pos_knowledge_index.json")

        if not os.path.exists(index_path):
            print(f"Index not found at {index_path}. Building now...")
            index_path = build_ai_index()

        with open(index_path, "rb") as f:
            self.index_data = orjson.loads(f.read())

        self.metadata = self.index_data["metadata"]
        self.total_docs = self.index_data["total_docs"]
        self.avg_dl = self.index_data["avg_dl"]
        self.doc_lengths = self.index_data["doc_lengths"]
        self.idf_table = self.index_data["idf_table"]
        self.inverted_index = self.index_data["inverted_index"]
        self.role_map = self.index_data["role_map"]
        self.module_map = self.index_data["module_map"]
        self.troubleshooting = self.index_data["troubleshooting"]
        self.chunks = self.index_data["chunks"]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def search(
        self,
        query: str,
        role: Optional[str] = None,
        module: Optional[str] = None,
        top_k: int = 5,
        k1: float = 1.5,
        b: float = 0.75
    ) -> List[Dict[str, Any]]:
        """
        Executes ultra-fast BM25 scoring with exact phrase bonuses and role/module boosting.
        Returns top_k ranked chunk records with detailed match scores.
        """
        t0 = time.perf_counter()
        tokens = tokenize(query)
        if not tokens:
            return []

        # Candidate doc scores
        scores: Dict[str, float] = {}

        # Filter candidate pool if role is specified
        role_allowed = None
        if role:
            r_key = role.strip().lower()
            # Match partial role name (e.g. 'server' -> 'food server')
            matched_roles = [docs for k, docs in self.role_map.items() if r_key in k]
            if matched_roles:
                role_allowed = set()
                for d_list in matched_roles:
                    role_allowed.update(d_list)

        # Filter candidate pool if module is specified
        module_allowed = None
        if module:
            m_key = module.strip().lower()
            matched_modules = [docs for k, docs in self.module_map.items() if m_key in k]
            if matched_modules:
                module_allowed = set()
                for d_list in matched_modules:
                    module_allowed.update(d_list)

        # 1. BM25 calculation
        for term in tokens:
            if term not in self.inverted_index:
                continue

            idf = self.idf_table.get(term, 0.5)
            postings = self.inverted_index[term]

            for doc_id, tf in postings.items():
                if role_allowed is not None and doc_id not in role_allowed:
                    continue
                if module_allowed is not None and doc_id not in module_allowed:
                    continue

                doc_len = self.doc_lengths.get(doc_id, self.avg_dl)
                # BM25 TF formula
                tf_norm = (tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * (doc_len / self.avg_dl)))
                scores[doc_id] = scores.get(doc_id, 0.0) + (idf * tf_norm)

        # 2. Exact Query Phrase / Substring Matching Bonus
        query_norm = query.strip().lower()
        for doc_id in scores.keys():
            ch = self.chunks[doc_id]
            combined_text = f"{ch['section']} {ch['summary']} {' '.join(ch['keywords'])}".lower()

            if query_norm in combined_text:
                scores[doc_id] += 5.0  # Exact phrase boost

            # Title match boost
            if any(t in ch['section'].lower() for t in tokens):
                scores[doc_id] += 2.0

        # Sort by final score
        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        dur_ms = (time.perf_counter() - t0) * 1000

        results = []
        for doc_id, score in ranked_docs:
            ch = self.chunks[doc_id]
            results.append({
                "id": doc_id,
                "score": round(score, 3),
                "part": ch["part"],
                "section": ch["section"],
                "module": ch["module"],
                "where": ch["where"],
                "target_roles": ch["target_roles"],
                "summary": ch["summary"],
                "steps": ch["steps"],
                "key_notes": ch["key_notes"],
                "troubleshooting": ch.get("troubleshooting", []),
                "latency_ms": round(dur_ms, 2)
            })

        return results

    def troubleshoot(self, issue: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Fast direct troubleshooting match against the 19 common problem scenarios.
        """
        t0 = time.perf_counter()
        tokens = tokenize(issue)
        results = []

        for item in self.troubleshooting:
            prob_tokens = tokenize(item["problem"])
            # Jaccard / token overlap
            common = set(tokens).intersection(set(prob_tokens))
            if common:
                score = len(common) / max(1, len(prob_tokens))
                # Boost if phrase substring
                if issue.lower() in item["problem"].lower() or item["problem"].lower() in issue.lower():
                    score += 2.0
                results.append((score, item))

        results.sort(key=lambda x: x[0], reverse=True)
        dur_ms = (time.perf_counter() - t0) * 1000

        output = []
        for score, item in results[:top_k]:
            out = dict(item)
            out["match_score"] = round(score, 3)
            out["latency_ms"] = round(dur_ms, 2)
            output.append(out)

        return output

    def get_ai_context(self, query: str, role: Optional[str] = None, max_chunks: int = 3) -> str:
        """
        Formats top retrieved chunks into clean, token-budgeted AI prompt context.
        Ready to be passed to any LLM (Gemini, Claude, GPT) for zero-shot question answering.
        """
        results = self.search(query, role=role, top_k=max_chunks)
        tb_results = self.troubleshoot(query, top_k=2)

        lines = [
            f"# OFFICIAL KNOWLEDGE BASE: {self.metadata['product']} (v{self.metadata['version']})",
            f"Document: {self.metadata['title']} ({self.metadata['document_id']})",
            f"Portal URL: {self.metadata['app_url']}\n"
        ]

        if tb_results and tb_results[0]["match_score"] >= 0.5:
            lines.append("## HIGH RELEVANCE TROUBLESHOOTING RESOLUTION:")
            for tb in tb_results:
                if tb["match_score"] >= 0.5:
                    lines.append(f"- **Problem**: {tb['problem']}")
                    lines.append(f"  **Solution**: {tb['solution']}")
                    lines.append(f"  **Module / Path**: {tb['module']} -> {tb['where']}\n")

        lines.append("## RELEVANT PROCEDURES & MODULE GUIDANCE:")
        for r in results:
            lines.append(f"### [{r['id']}] {r['part']} - {r['section']}")
            lines.append(f"- **Module**: {r['module']} | **Screen Location**: `{r['where']}`")
            lines.append(f"- **Applicable Roles**: {', '.join(r['target_roles'])}")
            lines.append(f"- **Summary**: {r['summary']}")
            if r['steps']:
                lines.append("- **Steps**:")
                for st in r['steps']:
                    lines.append(f"  {st}")
            if r['key_notes']:
                lines.append("- **Key Rules & Warnings**:")
                for kn in r['key_notes']:
                    lines.append(f"  * {kn}")
            lines.append("")

        return "\n".join(lines)
