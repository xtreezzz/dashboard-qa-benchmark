"""
Evaluation and comparison utilities.
"""
from typing import Dict, List, Any, Optional
from tabulate import tabulate
import json
import os
from datetime import datetime

try:
    from llm_judge import LLMJudge, evaluate_with_llm_judge
    LLM_JUDGE_AVAILABLE = True
except ImportError:
    LLM_JUDGE_AVAILABLE = False
    print("Warning: LLM Judge not available")


class Evaluator:
    """Evaluate framework results against benchmark answers."""
    
    @staticmethod
    def normalize_answer(answer: str) -> str:
        """Normalize answer for comparison."""
        return str(answer).strip().lower()
    
    @staticmethod
    def compare_answers(benchmark_answer: str, framework_answer: str, 
                       question: str = "", benchmark_reasoning: str = "",
                       use_llm_judge: bool = True) -> Dict[str, Any]:
        """Compare framework answer with benchmark answer.
        
        Args:
            benchmark_answer: Expected answer
            framework_answer: Answer from framework
            question: Original question (for LLM Judge)
            benchmark_reasoning: Reasoning for expected answer (for LLM Judge)
            use_llm_judge: Whether to use LLM Judge for evaluation
        """
        norm_benchmark = Evaluator.normalize_answer(benchmark_answer)
        norm_framework = Evaluator.normalize_answer(framework_answer)
        
        # Exact match
        exact_match = norm_benchmark == norm_framework
        
        # Contains match (framework answer contains benchmark)
        contains_match = norm_benchmark in norm_framework
        
        # Numeric match (for numerical answers with tolerance)
        numeric_match = False
        try:
            bench_num = float(benchmark_answer)
            frame_num = float(framework_answer)
            # Allow 1% tolerance
            numeric_match = abs(bench_num - frame_num) / max(abs(bench_num), 1e-10) < 0.01
        except (ValueError, TypeError):
            pass
        
        # Overall match from rule-based evaluation
        rule_based_match = exact_match or contains_match or numeric_match
        
        # LLM Judge evaluation
        llm_judge_result = None
        llm_judge_log = None
        final_match = rule_based_match
        
        if use_llm_judge and LLM_JUDGE_AVAILABLE and question:
            try:
                judge = LLMJudge()
                llm_result = judge.evaluate(
                    question=question,
                    expected_answer=benchmark_answer,
                    actual_answer=framework_answer,
                    reasoning=benchmark_reasoning
                )
                
                llm_judge_result = {
                    "is_correct": llm_result["is_correct"],
                    "confidence": llm_result["confidence"],
                    "explanation": llm_result["explanation"]
                }
                
                # Build detailed log with prompt and response
                llm_judge_log = {
                    "prompt": judge.build_evaluation_prompt(
                        question, benchmark_answer, framework_answer, benchmark_reasoning
                    ),
                    "response": llm_result.get("raw_response", ""),
                    "model": judge.model,
                    "result": llm_judge_result,
                    "reproduction_code": Evaluator._generate_llm_judge_code(
                        question, benchmark_answer, framework_answer, benchmark_reasoning, judge.model
                    )
                }
                
                # LLM Judge match is independent from rule-based
                llm_judge_match = llm_result["is_correct"]
                
                # Final match: prefer LLM Judge if available, otherwise use rule-based
                final_match = llm_judge_match if llm_judge_result else rule_based_match
                    
            except Exception as e:
                llm_judge_log = {"error": str(e)}
                llm_judge_match = None
        
        # Store both results separately
        result = {
            "exact_match": exact_match,
            "contains_match": contains_match,
            "numeric_match": numeric_match,
            "rule_based_match": rule_based_match,
            "llm_judge_match": llm_judge_result["is_correct"] if llm_judge_result else None,
            "is_match": final_match,  # Final decision (prefers LLM Judge)
            "benchmark_answer": benchmark_answer,
            "framework_answer": framework_answer,
            "llm_judge": llm_judge_result,
            "llm_judge_log": llm_judge_log
        }
        
        return result
    
    @staticmethod
    def _generate_llm_judge_code(question: str, expected: str, actual: str, reasoning: str, model: str = None) -> str:
        """Generate Python code to reproduce LLM Judge evaluation."""
        code = f'''"""Reproduce LLM Judge Evaluation"""
import os
from openai import OpenAI

# Initialize client (set OPENAI_API_KEY environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Evaluation prompt
question = """{question}"""
expected_answer = """{expected}"""
actual_answer = """{actual}"""
reasoning = """{reasoning}"""

prompt = f"""Evaluate if the actual answer is correct for the given question.

Question: {{question}}
Expected Answer: {{expected_answer}}
Reasoning: {{reasoning}}
Actual Answer: {{actual_answer}}

Evaluate if the actual answer is semantically equivalent to the expected answer.
Consider:
1. Different phrasings of the same answer
2. Numerical values with minor formatting differences
3. Answers embedded in longer explanations

Respond in JSON format:
{{
  "is_correct": true/false,
  "confidence": 0.0-1.0,
  "explanation": "brief explanation"
}}
"""

response = client.chat.completions.create(
    model="{model or 'gpt-5-nano'}",
    messages=[{{"role": "user", "content": prompt}}],
    temperature=0.0,
    max_completion_tokens=200
)

result = response.choices[0].message.content
print(result)
'''
        return code


class ResultFormatter:
    """Format and display results."""
    
    @staticmethod
    def format_comparison_table(question: str, benchmark: Dict[str, str], 
                                framework_results: Dict[str, Any]) -> str:
        """Format results as a comparison table."""
        
        # Prepare data for table
        headers = ["Source", "Answer", "Reasoning", "Match"]
        rows = []
        
        # Benchmark row
        rows.append([
            "Benchmark",
            benchmark["answer"],
            benchmark["reasoning"],
            "✓ (Ground Truth)"
        ])
        
        # Framework rows
        for framework_name, result in framework_results.items():
            if result.error:
                rows.append([
                    framework_name,
                    "ERROR",
                    result.error[:60] + "..." if len(result.error) > 60 else result.error,
                    "✗"
                ])
            else:
                # Use LLM Judge for comparison
                comparison = Evaluator.compare_answers(
                    benchmark_answer=benchmark["answer"],
                    framework_answer=result.answer,
                    question=question,
                    benchmark_reasoning=benchmark.get("reasoning", ""),
                    use_llm_judge=True
                )
                
                # Store comparison result in result object for later serialization
                result.comparison = comparison
                
                match_symbol = "✓" if comparison["is_match"] else "✗"
                
                rows.append([
                    framework_name,
                    result.answer[:50] + "..." if len(result.answer) > 50 else result.answer,
                    result.reasoning[:60] + "..." if len(result.reasoning) > 60 else result.reasoning,
                    match_symbol
                ])
        
        # Create table
        table = tabulate(rows, headers=headers, tablefmt="grid", maxcolwidths=[15, 30, 40, 10])
        
        output = f"\n{'='*100}\n"
        output += f"QUESTION: {question}\n"
        output += f"{'='*100}\n"
        output += table
        output += f"\n{'='*100}\n"
        
        return output
    
    @staticmethod
    def format_summary(results: List[Dict[str, Any]]) -> str:
        """Format summary statistics."""
        total_questions = len(results)
        
        framework_stats = {}
        
        for result in results:
            for framework_name, framework_result in result["framework_results"].items():
                if framework_name not in framework_stats:
                    framework_stats[framework_name] = {
                        "total": 0,
                        "correct": 0,
                        "errors": 0
                    }
                
                framework_stats[framework_name]["total"] += 1
                
                if framework_result.error:
                    framework_stats[framework_name]["errors"] += 1
                else:
                    # Use comparison result if already computed (with LLM Judge)
                    if hasattr(framework_result, 'comparison'):
                        comparison = framework_result.comparison
                    else:
                        # Fallback to basic comparison
                        comparison = Evaluator.compare_answers(
                            benchmark_answer=result["benchmark"]["answer"],
                            framework_answer=framework_result.answer,
                            question=result["question"],
                            benchmark_reasoning=result["benchmark"].get("reasoning", ""),
                            use_llm_judge=True
                        )
                    
                    if comparison["is_match"]:
                        framework_stats[framework_name]["correct"] += 1
        
        # Create summary table
        headers = ["Framework", "Correct", "Errors", "Accuracy"]
        rows = []
        
        for framework_name, stats in framework_stats.items():
            accuracy = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
            rows.append([
                framework_name,
                f"{stats['correct']}/{stats['total']}",
                stats['errors'],
                f"{accuracy:.1f}%"
            ])
        
        summary = f"\n{'='*100}\n"
        summary += f"SUMMARY STATISTICS\n"
        summary += f"{'='*100}\n"
        summary += f"Total Questions: {total_questions}\n\n"
        summary += tabulate(rows, headers=headers, tablefmt="grid")
        summary += f"\n{'='*100}\n"
        
        return summary
    
    @staticmethod
    def save_results(results: List[Dict[str, Any]], dataset_name: str, output_dir: str, dataset_df=None):
        """Save results to JSON file with optional dataset."""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{dataset_name}_results_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Convert FrameworkResult objects to dicts
        serializable_results = []
        for result in results:
            serializable_result = {
                "question": result["question"],
                "benchmark": result["benchmark"],
                "framework_results": {
                    name: fr.to_dict() for name, fr in result["framework_results"].items()
                }
            }
            serializable_results.append(serializable_result)
        
        # Add dataset CSV if provided
        dataset_csv = None
        if dataset_df is not None:
            try:
                dataset_csv = dataset_df.to_csv(index=False)
            except Exception as e:
                print(f"Warning: Could not convert dataset to CSV: {e}")
        
        # Create output with metadata
        output_data = {
            "metadata": {
                "dataset_name": dataset_name,
                "timestamp": timestamp,
                "total_questions": len(results),
                "has_dataset": dataset_csv is not None
            },
            "results": serializable_results,
            "dataset_csv": dataset_csv
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nResults saved to: {filepath}")
        if dataset_csv:
            print(f"  ✓ Dataset CSV included ({len(dataset_csv)} bytes)")
        return filepath
