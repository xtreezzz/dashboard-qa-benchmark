# LLM Judge and Reproducibility Features

## Overview

The benchmark system now includes **mandatory LLM Judge evaluation** and **full reproducibility code** for every query and evaluation.

## What's New

### 1. **LLM Judge (Mandatory)**

Every framework answer is now evaluated using GPT-4o-mini as a judge, which provides:
- **Semantic understanding**: Can recognize when "150" and "There are 150 rows" mean the same thing
- **Numerical tolerance**: Handles rounding differences (e.g., 5.84 vs 5.843333)
- **Confidence scores**: 0.0-1.0 rating of how confident the judge is
- **Explanations**: Clear reasoning for why an answer is correct or incorrect

### 2. **Full Logging**

Every result now includes complete logs with:
- **Framework execution logs**: Full verbose output from PandasAI, Sketch, and LangChain
- **LLM Judge prompts**: Exact prompt sent to GPT-4o-mini for evaluation
- **LLM Judge responses**: Raw response from the LLM judge
- **Timestamps**: When each step was executed

### 3. **Reproduction Code**

Each result includes **ready-to-run Python code** to reproduce:
- **Framework queries**: Standalone code to reproduce PandasAI/Sketch/LangChain results
- **LLM Judge evaluation**: Standalone code to reproduce the judge's evaluation
- **Sample data**: First 10 rows of the dataset included in the code

## Result Structure

```json
{
  "metadata": {
    "dataset_name": "iris",
    "timestamp": "20251109_142417",
    "total_questions": 5,
    "has_dataset": true
  },
  "results": [
    {
      "question": "How many rows are in the dataset?",
      "benchmark": {
        "answer": "150",
        "reasoning": "The Iris dataset contains 150 samples"
      },
      "framework_results": {
        "PandasAI": {
          "answer": "150",
          "reasoning": "PandasAI processed the query...",
          "error": "",
          "logs": "[2025-11-09T14:24:17] Starting PandasAI query...",
          "reproduction_code": "\"\"\"Reproduce PandasAI Query\"\"\"\nimport pandas as pd...",
          "comparison": {
            "exact_match": true,
            "contains_match": true,
            "numeric_match": true,
            "rule_based_match": true,
            "is_match": true,
            "llm_judge": {
              "is_correct": true,
              "confidence": 1.0,
              "explanation": "Exact match"
            },
            "llm_judge_log": {
              "prompt": "Question: How many rows...",
              "response": "CORRECT|Exact match|1.0",
              "model": "gpt-4o-mini",
              "result": {...},
              "reproduction_code": "\"\"\"Reproduce LLM Judge Evaluation\"\"\"..."
            }
          }
        }
      }
    }
  ],
  "dataset_csv": "sepal length (cm),sepal width (cm)..."
}
```

## How to Use

### View Results in Streamlit

```bash
cd /Users/family/dashboard-qa-benchmark
python3 -m streamlit run streamlit_app.py
```

Navigate to **Detailed Results** to see:
- Download buttons for full logs
- Download button for dataset CSV
- LLM Judge evaluations with confidence scores

### Extract Reproduction Code

```python
import json

with open('results/iris_results_20251109_142417.json') as f:
    data = json.load(f)

# Get reproduction code for first question, PandasAI
q1 = data['results'][0]
pandasai_code = q1['framework_results']['PandasAI']['reproduction_code']

# Save to file and run
with open('reproduce_pandasai.py', 'w') as f:
    f.write(pandasai_code)

# Run it
# python reproduce_pandasai.py
```

### Extract LLM Judge Reproduction Code

```python
# Get LLM Judge reproduction code
comparison = q1['framework_results']['PandasAI']['comparison']
judge_code = comparison['llm_judge_log']['reproduction_code']

# Save and run
with open('reproduce_llm_judge.py', 'w') as f:
    f.write(judge_code)

# python reproduce_llm_judge.py
```

### View LLM Judge Details

```python
# Get LLM Judge evaluation
llm_judge = comparison['llm_judge']
print(f"Is Correct: {llm_judge['is_correct']}")
print(f"Confidence: {llm_judge['confidence']}")
print(f"Explanation: {llm_judge['explanation']}")

# View full prompt and response
log = comparison['llm_judge_log']
print(f"\nPrompt sent to GPT-4o-mini:\n{log['prompt']}")
print(f"\nResponse from GPT-4o-mini:\n{log['response']}")
```

## Example: Reproduce a Query

The reproduction code is **ready to run** - just copy and save to a file:

```python
"""Reproduce PandasAI Query"""
import pandas as pd
import os
from pandasai import Agent
from pandasai_litellm.litellm import LiteLLM

# Sample data (first 10 rows)
data_csv = """
sepal length (cm),sepal width (cm),petal length (cm),petal width (cm),species,species_name
5.1,3.5,1.4,0.2,0,setosa
4.9,3.0,1.4,0.2,0,setosa
...
"""

df = pd.read_csv(pd.io.common.StringIO(data_csv))

# Initialize PandasAI with LiteLLM
api_key = os.getenv("OPENAI_API_KEY")
llm = LiteLLM(model="gpt-3.5-turbo", api_key=api_key)

# Create agent and query
agent = Agent(df, config={"llm": llm, "verbose": True, "enable_cache": False})
question = """How many rows are in the dataset?"""
response = agent.chat(question)

print(f"Answer: {response}")
```

## Example: Reproduce LLM Judge

```python
"""Reproduce LLM Judge Evaluation"""
import os
from openai import OpenAI

# Initialize client (set OPENAI_API_KEY environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Evaluation prompt
question = """How many rows are in the dataset?"""
expected_answer = """150"""
actual_answer = """150"""
reasoning = """The Iris dataset contains 150 samples"""

prompt = f"""Evaluate if the actual answer is correct for the given question.

Question: {question}
Expected Answer: {expected_answer}
Reasoning: {reasoning}
Actual Answer: {actual_answer}

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
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0,
    response_format={"type": "json_object"}
)

result = response.choices[0].message.content
print(result)
```

## Benefits

### 1. **Full Transparency**
- See exactly what was sent to each framework
- See exactly what was sent to the LLM judge
- No hidden magic - everything is logged

### 2. **Reproducibility**
- Copy the code and run it yourself
- Verify results independently
- Debug issues easily

### 3. **Better Accuracy**
- LLM Judge catches semantic matches that simple string comparison misses
- Reduces false negatives from formatting differences
- Confidence scores help identify uncertain evaluations

### 4. **Scientific Rigor**
- Every evaluation is backed by complete evidence
- Results can be independently verified
- Methodology is fully transparent

## Cost

LLM Judge uses GPT-4o-mini which costs approximately:
- **$0.0001 per evaluation** (~$0.005 per full benchmark)
- **47 evaluations × 3 frameworks = 141 evaluations**
- **Total cost: ~$0.014 per full run of all 11 datasets**

This is negligible compared to the framework query costs and provides significant value in accuracy.

## Configuration

LLM Judge is now **mandatory** and always enabled. There is no opt-out option as it's integral to the evaluation system.

To disable for testing, you would need to modify `src/evaluation.py`:
```python
# In compare_answers() function
use_llm_judge=False  # Change to False
```

But this is **not recommended** for production benchmarks.

## Files

Key files for the new system:
- `src/evaluation.py` - Main evaluation logic with LLM Judge integration
- `src/llm_judge.py` - LLM Judge implementation
- `src/framework_integrations.py` - Framework wrappers with reproduction code generation
- `main.py` - Benchmark runner
- `streamlit_app.py` - Dashboard for viewing results

## Next Steps

1. **Run benchmarks**: `./run_all_benchmarks.sh`
2. **View results**: `python3 -m streamlit run streamlit_app.py`
3. **Extract code**: Use the examples above
4. **Verify results**: Run the reproduction code yourself

---

**Last Updated**: November 9, 2025
