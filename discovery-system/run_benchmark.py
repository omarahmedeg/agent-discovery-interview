"""
Benchmark runner for agent discovery and interview pipeline.
This script:
1. Loads benchmark queries from benchmark_queries.json
2. For each query, uses BM25 to find top-k candidate agents
3. Interviews each candidate agent
4. Evaluates if the correct agent was selected
"""

import json
from agent_bm25s import load_agents, build_bm25_index, bm25_agent_urls
from interview import interview_candidate

def load_benchmark_queries(filename: str = "benchmark_queries.json"):
    """Load benchmark queries from JSON file."""
    with open(filename, "r") as f:
        return json.load(f)

def run_benchmark(agents_file: str = "software_agents.json", 
                  queries_file: str = "benchmark_queries.json",
                  k: int = 3,
                  verbose: bool = True):
    """
    Run the full benchmark.
    
    Args:
        agents_file: Path to agents JSON file
        queries_file: Path to benchmark queries JSON file
        k: Number of top candidates to retrieve and interview
        verbose: Print detailed output
    """
    # Load agents and build index
    print(f"Loading agents from {agents_file}...")
    agents = load_agents(agents_file)
    retriever, corpus = build_bm25_index(agents)
    
    # Load benchmark queries
    print(f"Loading benchmark queries from {queries_file}...")
    queries = load_benchmark_queries(queries_file)
    print(f"Loaded {len(queries)} benchmark queries\n")
    
    results = []
    correct_count = 0
    
    for i, query_item in enumerate(queries, 1):
        query_id = query_item["id"]
        query_text = query_item["text"]
        correct_agent = query_item["correctAgentName"]
        
        print("=" * 80)
        print(f"Query {query_id} ({i}/{len(queries)})")
        print(f"Text: {query_text[:100]}...")
        print(f"Expected Agent: {correct_agent}")
        print("-" * 80)
        
        # Get top-k candidate URLs using BM25
        candidate_urls = bm25_agent_urls(
            query=query_text,
            k=k,
            agents=agents,
            retriever=retriever,
            corpus=corpus,
            verbose=verbose
        )
        
        # Interview each candidate
        interview_results = []
        for rank, url in enumerate(candidate_urls, 1):
            print(f"\n[{rank}/{len(candidate_urls)}] Interviewing: {url}")
            
            # Find agent name from URL
            agent_name = None
            for agent in agents:
                if agent.get("url") == url:
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
                
                if verbose and result:
                    print(f"Interview result: {result[:200]}...")
            except Exception as e:
                print(f"ERROR interviewing {agent_name}: {e}")
                interview_results.append({
                    "rank": rank,
                    "url": url,
                    "agent_name": agent_name,
                    "result": None,
                    "error": str(e)
                })
        
        # Check if correct agent was in top-k
        retrieved_agent_names = [r["agent_name"] for r in interview_results]
        is_correct = correct_agent in retrieved_agent_names
        
        if is_correct:
            correct_count += 1
            status = "[CORRECT]"
        else:
            status = "[INCORRECT]"
        
        print(f"\n{status} - Expected: {correct_agent}, Retrieved: {retrieved_agent_names}")
        
        results.append({
            "query_id": query_id,
            "query_text": query_text,
            "expected_agent": correct_agent,
            "retrieved_agents": retrieved_agent_names,
            "is_correct": is_correct,
            "interviews": interview_results
        })
        print()
    
    # Calculate metrics
    # Top-1 Accuracy: Percentage of queries where the correct agent is ranked #1
    top1_correct = sum(1 for r in results if r["retrieved_agents"] and r["retrieved_agents"][0] == r["expected_agent"])
    top1_accuracy = top1_correct / len(queries)
    
    # Top-3 Recall: Percentage of queries where the correct agent is in top-3
    top3_recall = correct_count / len(queries)
    
    # Print summary
    print("=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"Total Queries: {len(queries)}")
    print(f"Top-1 Accuracy: {top1_accuracy*100:.1f}% ({top1_correct}/{len(queries)} queries had correct agent at rank #1)")
    print(f"Top-3 Recall: {top3_recall*100:.1f}% ({correct_count}/{len(queries)} queries had correct agent in top-3)")
    print(f"Top-K: {k}")
    print("=" * 80)
    
    # Save detailed results
    output_file = "benchmark_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "summary": {
                "total_queries": len(queries),
                "top1_correct": top1_correct,
                "top1_accuracy": top1_accuracy,
                "top3_correct": correct_count,
                "top3_recall": top3_recall,
                "k": k
            },
            "results": results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to {output_file}")
    
    return results

def main():
    """Run the benchmark with default settings."""
    run_benchmark(
        agents_file="software_agents.json",
        queries_file="benchmark_queries.json",
        k=3,  # Try top-3 agents for each query
        verbose=True
    )

if __name__ == "__main__":
    main()
