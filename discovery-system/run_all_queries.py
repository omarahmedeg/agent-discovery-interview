"""
Run all queries from queryList.json and calculate metrics.
"""

import json
from datetime import datetime
from dotenv import load_dotenv
from agent_bm25s import load_agents, build_bm25_index, bm25_agent_urls
from interview import interview_candidate

# Load environment variables from .env file
load_dotenv()

def load_queries(filename: str = "queryList.json"):
    """Load queries from JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def run_all_queries(agents_file: str = "agentList.json", 
                    queries_file: str = "queryList.json",
                    k: int = 3,
                    verbose: bool = True):
    """
    Run all queries and calculate metrics.
    
    Args:
        agents_file: Path to agents JSON file
        queries_file: Path to queries JSON file
        k: Number of top candidates to retrieve and interview
        verbose: Print detailed output
    """
    # Open output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"all_queries_output_{timestamp}.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        def log(msg):
            """Print to console and write to file"""
            print(msg)
            f.write(msg + "\n")
            f.flush()
        
        # Load agents and build index
        log(f"Loading agents from {agents_file}...")
        agents = load_agents(agents_file)
        retriever, corpus = build_bm25_index(agents)
        
        # Load queries
        log(f"Loading queries from {queries_file}...")
        queries = load_queries(queries_file)
        log(f"Loaded {len(queries)} queries\n")
        
        results = []
        
        for i, query_item in enumerate(queries, 1):
            query_id = query_item.get("id", f"Q{i}")
            query_text = query_item.get("text", "")
            correct_agent = query_item.get("correctAgentName", "")
            
            log("=" * 80)
            log(f"Query {query_id} ({i}/{len(queries)})")
            log(f"Text: {query_text}")
            log(f"Expected Agent: {correct_agent}")
            log("-" * 80)
            
            # Get top-k candidate URLs using BM25
            import bm25s
            try:
                import Stemmer
                STEMMER = Stemmer.Stemmer("english")
            except:
                STEMMER = None
                
            q_tokens = bm25s.tokenize([query_text], stopwords="en", stemmer=STEMMER)
            bm25_results, scores = retriever.retrieve(q_tokens, k=k)
            
            # Log BM25 rankings
            retrieved_agents = []
            for rank in range(bm25_results.shape[1]):
                doc_idx = int(bm25_results[0, rank])
                score = float(scores[0, rank])
                agent = agents[doc_idx]
                agent_name = agent.get("name", "unknown")
                retrieved_agents.append(agent_name)
                log(f"Rank {rank+1}  score={score:.3f}  name={agent_name}")
            
            # Get URLs for interviews
            candidate_urls = bm25_agent_urls(
                query=query_text,
                k=k,
                agents=agents,
                retriever=retriever,
                corpus=corpus,
                verbose=False
            )
            
            log(f"\nInterviewing {len(candidate_urls)} candidates...")
            
            # Interview each candidate
            interview_results = []
            for rank, url in enumerate(candidate_urls, 1):
                log(f"\n[{rank}/{len(candidate_urls)}] Interviewing: {url}")
                
                # Find agent name from URL
                agent_name = None
                for agent in agents:
                    from agent_bm25s import get_primary_url
                    if get_primary_url(agent) == url:
                        agent_name = agent.get("name")
                        break
                
                try:
                    result = interview_candidate(
                        candidate_url=url,
                        task=query_text
                    )
                    
                    interview_results.append({
                        "rank": rank,
                        "url": url,
                        "agent_name": agent_name,
                        "result": result
                    })
                    
                    if result:
                        log(f"=== Interview ===")
                        log(f"Task:       {result.get('task', '')[:100]}...")
                        log(f"Question:   {result.get('question', '')[:100]}...")
                        log(f"Answer:     {result.get('answer', '')[:200]}...")
                        log(f"Evaluation: {result.get('evaluation', {})}")
                        
                except Exception as e:
                    log(f"ERROR interviewing {agent_name}: {e}")
                    interview_results.append({
                        "rank": rank,
                        "url": url,
                        "agent_name": agent_name,
                        "result": None,
                        "error": str(e)
                    })
            
            # Check if correct agent was in top-k
            is_correct_top1 = len(retrieved_agents) > 0 and retrieved_agents[0] == correct_agent
            is_correct_topk = correct_agent in retrieved_agents
            
            if is_correct_topk:
                status = "[CORRECT]"
            else:
                status = "[INCORRECT]"
            
            log(f"\n{status} - Expected: {correct_agent}, Retrieved: {retrieved_agents}")
            
            results.append({
                "query_id": query_id,
                "query_text": query_text,
                "expected_agent": correct_agent,
                "retrieved_agents": retrieved_agents,
                "is_correct_top1": is_correct_top1,
                "is_correct_topk": is_correct_topk,
                "interviews": interview_results
            })
            log("")
        
        # Calculate metrics
        # Top-1 Accuracy: Percentage of queries where the correct agent is ranked #1
        top1_correct = sum(1 for r in results if r["is_correct_top1"])
        top1_accuracy = top1_correct / len(queries) if len(queries) > 0 else 0
        
        # Top-K Recall: Percentage of queries where the correct agent is in top-k
        topk_correct = sum(1 for r in results if r["is_correct_topk"])
        topk_recall = topk_correct / len(queries) if len(queries) > 0 else 0
        
        # Print summary
        log("=" * 80)
        log("BENCHMARK SUMMARY")
        log("=" * 80)
        log(f"Total Queries: {len(queries)}")
        log(f"Top-1 Accuracy: {top1_accuracy*100:.1f}% ({top1_correct}/{len(queries)} queries had correct agent at rank #1)")
        log(f"Top-{k} Recall: {topk_recall*100:.1f}% ({topk_correct}/{len(queries)} queries had correct agent in top-{k})")
        log(f"Top-K: {k}")
        log("=" * 80)
        
        # Save detailed results
        results_file = f"query_results_{timestamp}.json"
        with open(results_file, "w", encoding="utf-8") as rf:
            json.dump({
                "summary": {
                    "total_queries": len(queries),
                    "top1_correct": top1_correct,
                    "top1_accuracy": top1_accuracy,
                    "topk_correct": topk_correct,
                    "topk_recall": topk_recall,
                    "k": k
                },
                "results": results
            }, rf, indent=2)
        
        log(f"\nDetailed results saved to {results_file}")
        log(f"Output saved to: {output_file}")

if __name__ == "__main__":
    run_all_queries(agents_file="agentList.json", queries_file="queryList.json", k=3, verbose=True)
