"""
Run all 24 queries with full questions and answers (no truncation).
Uses OpenAI directly since agent servers may not be available.
"""

import json
from datetime import datetime
from dotenv import load_dotenv
from agent_bm25s import load_agents, build_bm25_index, bm25_agent_urls
from interview import call_llm
import bm25s

# Load environment variables from .env file
load_dotenv()

def load_queries(filename: str = "queryList.json"):
    """Load queries from JSON file."""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def run_24_queries_full(agents_file: str = "agentList.json", 
                        queries_file: str = "queryList.json",
                        k: int = 3,
                        verbose: bool = True):
    """
    Run all 24 queries with full question and answer outputs (no truncation).
    Uses OpenAI directly to generate answers.
    
    Args:
        agents_file: Path to agents JSON file
        queries_file: Path to queries JSON file
        k: Number of top candidates to retrieve
        verbose: Print detailed output
    """
    # Open output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"full_queries_output_{timestamp}.txt"
    json_output_file = f"full_queries_results_{timestamp}.json"
    
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
            
            # Get top-k candidates using BM25
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
            
            log(f"\nGenerating interview with OpenAI...")
            
            # Interview by generating Q&A directly with OpenAI
            interview_results = []
            
            # Generate question
            sys_interviewer = (
                "You are an interviewing agent. Your goal is to evaluate whether a "
                "candidate agent is suitable for a TASK by asking it questions."
            )
            
            q_prompt = f"""
            TASK: {query_text}
            
            Generate ONE clear, concrete interview question you would ask a candidate agent
            to see if it can handle this task.
            Just output the question text.
            """
            question = call_llm(sys_interviewer, q_prompt)
            
            # Generate answer as if from the best matching agent
            best_agent_name = retrieved_agents[0] if retrieved_agents else "agent"
            sys_candidate = f"""You are a specialized software engineering agent named '{best_agent_name}'.
Your role is to provide expert guidance on this specific domain.
Answer the interviewer's question thoroughly and professionally."""
            
            answer_prompt = f"""
            TASK: {query_text}
            
            INTERVIEW QUESTION: {question}
            
            Please provide a comprehensive, detailed answer to help the interviewer understand
            your capability to handle this task.
            """
            
            answer = call_llm(sys_candidate, answer_prompt)
            
            # Generate evaluation
            eval_prompt = f"""
            You interviewed a candidate agent.
            
            TASK: {query_text}
            
            INTERVIEW QUESTION: {question}
            
            CANDIDATE ANSWER: {answer}
            
            On a scale from 1 to 10, how suitable is this agent for the task?
            Return STRICT JSON: {{"score": <int 1-10>, "justification": "<short reason>"}}
            """
            eval_json_str = call_llm(
                "You are a strict JSON-producing judge. No extra text.",
                eval_prompt,
                json_mode=True,
            )
            
            try:
                eval_data = json.loads(eval_json_str)
            except:
                eval_data = {"score": 5, "justification": "Unable to parse evaluation"}
            
            # Store result
            result = {
                "query_id": query_id,
                "query_text": query_text,
                "expected_agent": correct_agent,
                "retrieved_agents": retrieved_agents,
                "interview": {
                    "question": question,
                    "answer": answer,
                    "evaluation": eval_data
                }
            }
            
            interview_results.append(result)
            
            # Log full output (NO TRUNCATION)
            log(f"\n{'='*80}")
            log("=== FULL INTERVIEW RESULTS ===")
            log(f"{'='*80}\n")
            log(f"Question:\n{question}\n")
            log(f"{'-'*80}\n")
            log(f"Answer:\n{answer}\n")
            log(f"{'-'*80}\n")
            log(f"Evaluation: Score {eval_data.get('score', 0)}/10")
            log(f"Justification: {eval_data.get('justification', 'N/A')}\n")
            
            # Check if correct agent was retrieved
            is_correct_top1 = len(retrieved_agents) > 0 and retrieved_agents[0] == correct_agent
            is_correct_topk = correct_agent in retrieved_agents
            
            if is_correct_topk:
                status = "[CORRECT]"
            else:
                status = "[INCORRECT]"
            
            log(f"{status} - Expected: {correct_agent}, Retrieved: {retrieved_agents}\n")
            
            result["is_correct_top1"] = is_correct_top1
            result["is_correct_topk"] = is_correct_topk
            results.append(result)
        
        # Calculate metrics
        top1_correct = sum(1 for r in results if r["is_correct_top1"])
        top1_accuracy = top1_correct / len(queries) if len(queries) > 0 else 0
        
        topk_correct = sum(1 for r in results if r["is_correct_topk"])
        topk_recall = topk_correct / len(queries) if len(queries) > 0 else 0
        
        # Print summary
        log("\n" + "=" * 80)
        log("BENCHMARK SUMMARY - 24 QUERIES")
        log("=" * 80)
        log(f"Total Queries: {len(queries)}")
        log(f"Top-1 Accuracy: {top1_accuracy*100:.1f}% ({top1_correct}/{len(queries)} queries had correct agent at rank #1)")
        log(f"Top-{k} Recall: {topk_recall*100:.1f}% ({topk_correct}/{len(queries)} queries had correct agent in top-{k})")
        log(f"Top-K: {k}")
        log("=" * 80)
        
        # Save detailed results to JSON
        with open(json_output_file, "w", encoding="utf-8") as rf:
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
        
        log(f"\nDetailed results saved to {json_output_file}")
        log(f"Full text output saved to: {output_file}")

if __name__ == "__main__":
    run_24_queries_full(agents_file="agentList.json", queries_file="queryList.json", k=3, verbose=True)
