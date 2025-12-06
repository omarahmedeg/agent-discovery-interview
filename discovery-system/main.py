from dotenv import load_dotenv
from agent_bm25s import load_agents, build_bm25_index, bm25_agent_urls
from interview import interview_candidate
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def load_queries(path: str = "queryList.json") -> list[dict]:
    """Load queries from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        queries = json.load(f)
    if not isinstance(queries, list):
        raise ValueError("queries file must contain a JSON array")
    return queries

def main():
    # Open output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"demo_output_{timestamp}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        def log(msg):
            """Print to console and write to file"""
            print(msg)
            f.write(msg + "\n")
            f.flush()
        
        # 1) Load agents and build BM25 index (using agentList.json)
        agents = load_agents("agentList.json")
        retriever, corpus = build_bm25_index(agents)

        # 2) Load queries from queryList.json
        queries = load_queries("queryList.json")
        
        # 3) Demo: Use the first query
        if not queries:
            log("No queries found in queryList.json")
            return
        
        first_query = queries[0]
        query_text = first_query.get("text", "")
        query_id = first_query.get("id", "unknown")
        
        log(f"\n{'='*80}")
        log(f"DEMO: Processing Query {query_id}")
        log(f"Query: {query_text}")
        log(f"{'='*80}\n")
        
        # 4) Run BM25 to get candidate URLs
        log("Running BM25 search...")
        candidate_urls = bm25_agent_urls(
            query=query_text, 
            k=2, 
            agents=agents, 
            retriever=retriever, 
            corpus=corpus, 
            verbose=False  # We'll manually log the results
        )
        
        # Log BM25 results manually
        from agent_bm25s import doc_text
        import bm25s
        try:
            import Stemmer
            STEMMER = Stemmer.Stemmer("english")
        except:
            STEMMER = None
            
        q_tokens = bm25s.tokenize([query_text], stopwords="en", stemmer=STEMMER)
        results, scores = retriever.retrieve(q_tokens, k=2)
        
        for i in range(results.shape[1]):
            doc_idx = int(results[0, i])
            score = float(scores[0, i])
            agent = agents[doc_idx]
            name = agent.get("name", "unknown")
            log(f"Rank {i+1}  score={score:.3f}  name={name}")

        # 5) Interview each candidate
        log(f"\n{'='*80}")
        log(f"Found {len(candidate_urls)} candidate agents to interview")
        log(f"{'='*80}\n")
        
        for url in candidate_urls:
            log(f"\n{'='*80}")
            log(f"Interviewing candidate: {url}")
            log(f"{'='*80}")
            result = interview_candidate(candidate_url=url, task=query_text)
            log(f"\nInterview Result:")
            log(f"{'-'*80}")
            log(json.dumps(result, indent=2))
            log(f"{'-'*80}\n")
        
        log(f"\n{'='*80}")
        log(f"Output saved to: {output_file}")
        log(f"{'='*80}")

if __name__ == "__main__":
    main()