"""
LLM-based Judge for evaluating answer correctness.

Uses OpenAI GPT to determine if a framework's answer matches the expected answer,
handling differences in formatting, rounding, and semantic equivalence.
"""
import os
from typing import Dict, Any, Tuple, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMJudge:
    """LLM-based judge for answer evaluation."""
    
    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize LLM Judge.
        
        Args:
            model: OpenAI model to use (default: from EVAL_MODEL env var or gpt-5-nano)
            api_key: OpenAI API key (default: from OPENAI_API_KEY env var)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("EVAL_MODEL", "gpt-5-nano")
    
    def evaluate(
        self,
        question: str,
        expected_answer: str,
        actual_answer: str,
        reasoning: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluate if actual_answer matches expected_answer.
        
        Args:
            question: The question being answered
            expected_answer: The correct/expected answer
            actual_answer: The answer provided by the framework
            reasoning: Optional reasoning for the expected answer
        
        Returns:
            Dict with is_correct, explanation, confidence, raw_response
        """
        # Quick exact match check
        if str(expected_answer).strip().lower() == str(actual_answer).strip().lower():
            return {
                "is_correct": True,
                "explanation": "Exact match",
                "confidence": 1.0,
                "raw_response": "Exact match (pre-LLM)"
            }
        
        # Try numeric comparison
        try:
            exp_num = float(expected_answer)
            act_num = float(actual_answer)
            
            # Check if numbers are close (within 1% or 0.01 absolute)
            if abs(exp_num - act_num) < 0.01 or abs(exp_num - act_num) / max(abs(exp_num), 1) < 0.01:
                return {
                    "is_correct": True,
                    "explanation": f"Numerical match: {exp_num} ≈ {act_num}",
                    "confidence": 0.95,
                    "raw_response": f"Numerical match (pre-LLM): {exp_num} ≈ {act_num}"
                }
        except (ValueError, TypeError):
            pass
        
        # Use LLM for semantic evaluation
        prompt = self.build_evaluation_prompt(
            question, expected_answer, actual_answer, reasoning
        )
        
        try:
            # Build API call parameters
            call_params = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert judge evaluating if two answers to a data analysis question are equivalent. Consider numerical precision, formatting differences, and semantic meaning."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_completion_tokens": 1000  # Higher limit for gpt-5-nano reasoning tokens
            }
            
            # gpt-5 models don't support temperature parameter
            if not self.model.startswith('gpt-5'):
                call_params["temperature"] = 0.1
            
            response = self.client.chat.completions.create(**call_params)
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            is_correct, explanation, confidence = self._parse_llm_response(result_text)
            
            return {
                "is_correct": is_correct,
                "explanation": explanation,
                "confidence": confidence,
                "raw_response": result_text
            }
            
        except Exception as e:
            # Fallback to string comparison if LLM fails
            if str(expected_answer).strip() == str(actual_answer).strip():
                return {
                    "is_correct": True,
                    "explanation": "String match (LLM unavailable)",
                    "confidence": 0.8,
                    "raw_response": f"LLM Error: {str(e)[:50]}"
                }
            else:
                return {
                    "is_correct": False,
                    "explanation": f"No match (LLM error: {str(e)[:50]})",
                    "confidence": 0.5,
                    "raw_response": f"LLM Error: {str(e)[:50]}"
                }
    
    def build_evaluation_prompt(
        self,
        question: str,
        expected_answer: str,
        actual_answer: str,
        reasoning: str = ""
    ) -> str:
        """Build evaluation prompt for LLM (public method for logging)."""
        prompt = f"""Question: {question}

Expected Answer: {expected_answer}
Actual Answer: {actual_answer}
"""
        
        if reasoning:
            prompt += f"\nReasoning: {reasoning}\n"
        
        prompt += """
Evaluate if the Actual Answer is correct compared to the Expected Answer.

Consider:
- Numerical values may differ in precision (5.84 vs 5.843333)
- Formatting differences (150 vs 150.0 vs "150")
- Semantic equivalence (e.g., "3 species" vs "3")
- Minor rounding differences
- Different representations of the same value

Respond ONLY with:
CORRECT|<explanation>|<confidence 0.0-1.0>
or
INCORRECT|<explanation>|<confidence 0.0-1.0>

Example: CORRECT|Both answers represent 150 rows, formatting differs|0.95
"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Tuple[bool, str, float]:
        """Parse LLM response into structured result."""
        try:
            parts = response.split('|')
            
            if len(parts) >= 3:
                verdict = parts[0].strip().upper()
                explanation = parts[1].strip()
                confidence = float(parts[2].strip())
                
                is_correct = verdict == "CORRECT"
                return is_correct, explanation, confidence
            else:
                # Fallback parsing
                if "CORRECT" in response.upper():
                    return True, response, 0.7
                else:
                    return False, response, 0.7
                    
        except Exception as e:
            # Default to string comparison
            return False, f"Parse error: {str(e)}", 0.5
    
    def batch_evaluate(
        self,
        evaluations: list
    ) -> list:
        """
        Batch evaluate multiple answer pairs.
        
        Args:
            evaluations: List of dicts with keys: question, expected_answer, actual_answer
        
        Returns:
            List of evaluation results
        """
        results = []
        
        for item in evaluations:
            result = self.evaluate(
                question=item['question'],
                expected_answer=item['expected_answer'],
                actual_answer=item['actual_answer'],
                reasoning=item.get('reasoning', '')
            )
            
            results.append({
                'question': item['question'],
                'is_correct': result['is_correct'],
                'explanation': result['explanation'],
                'confidence': result['confidence'],
                'expected_answer': item['expected_answer'],
                'actual_answer': item['actual_answer']
            })
        
        return results


def evaluate_with_llm_judge(
    question: str,
    expected_answer: str,
    actual_answer: str,
    use_llm: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to evaluate a single answer.
    
    Args:
        question: The question
        expected_answer: Expected answer
        actual_answer: Actual answer from framework
        use_llm: Whether to use LLM judge (default True)
    
    Returns:
        Dict with is_correct, explanation, confidence
    """
    if not use_llm:
        # Simple comparison
        is_correct = str(expected_answer).strip().lower() == str(actual_answer).strip().lower()
        return {
            'is_correct': is_correct,
            'explanation': 'Exact string match' if is_correct else 'String mismatch',
            'confidence': 1.0 if is_correct else 0.0,
            'method': 'string_comparison'
        }
    
    judge = LLMJudge()
    result = judge.evaluate(
        question=question, 
        expected_answer=expected_answer, 
        actual_answer=actual_answer
    )
    
    return {
        'is_correct': result['is_correct'],
        'explanation': result['explanation'],
        'confidence': result['confidence'],
        'method': 'llm_judge'
    }
