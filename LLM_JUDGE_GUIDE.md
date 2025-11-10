# LLM Judge Guide

## Overview

LLM Judge is an AI-powered answer evaluation system that provides more accurate assessments of framework responses compared to simple string/numeric matching.

## Features

### Intelligent Answer Matching

- **Numerical Tolerance**: Handles precision differences (5.84 vs 5.843333)
- **Format Flexibility**: Recognizes equivalent formats (150 vs "150" vs 150.0)
- **Semantic Understanding**: Interprets meaning ("3 species" vs "3")
- **Confidence Scores**: Provides confidence level (0.0-1.0) for each evaluation

### Three-Tier Evaluation

1. **Exact Match** (Fastest)
   - Direct string comparison
   - Confidence: 1.0

2. **Numeric Comparison**
   - Checks if numbers are within 1% or 0.01 absolute difference
   - Confidence: 0.95

3. **LLM Evaluation** (Most Accurate)
   - Uses GPT-4o-mini for semantic comparison
   - Considers context and meaning
   - Confidence: 0.5-1.0 (varies by case)

## Usage

### In Dashboard

1. Open Streamlit dashboard
2. Go to sidebar → "⚖️ Evaluation Settings"
3. Check "Use LLM Judge"
4. Navigate to "🔍 Detailed Results"
5. View evaluations with confidence indicators

### Confidence Indicators

- 🟢 **Green**: High confidence (>80%)
- 🟡 **Yellow**: Medium confidence (50-80%)
- 🔴 **Red**: Low confidence (<50%)

### In Code

```python
from src.llm_judge import evaluate_with_llm_judge

result = evaluate_with_llm_judge(
    question="What is the average age?",
    expected_answer="42.5",
    actual_answer="42.50",
    use_llm=True
)

print(result)
# {
#   'is_correct': True,
#   'explanation': 'Numerical match: 42.5 ≈ 42.50',
#   'confidence': 0.95,
#   'method': 'llm_judge'
# }
```

## Cost Considerations

### Token Usage

Each LLM evaluation uses approximately:
- **Input tokens**: ~150-200 tokens
- **Output tokens**: ~50-100 tokens
- **Total**: ~250 tokens per evaluation

### Pricing (GPT-4o-mini)

- **Cost per evaluation**: ~$0.0001 (0.01 cents)
- **100 evaluations**: ~$0.01 (1 cent)
- **1000 evaluations**: ~$0.10 (10 cents)

**Very affordable for most use cases!**

## When to Use LLM Judge

### ✅ Use LLM Judge When:

- Dealing with various number formats
- Comparing text answers with different wording
- Need high accuracy in evaluation
- Cost is not a primary concern
- Running spot checks on specific questions

### ❌ Don't Use LLM Judge When:

- Need fastest possible evaluation
- Running thousands of evaluations
- Answers are already exact matches
- Working offline without API access
- Minimizing API costs is critical

## Examples

### Example 1: Number Formatting

```
Question: "How many rows are in the dataset?"
Expected: "150"
Actual: "150.0"

Without LLM: ❌ INCORRECT (string mismatch)
With LLM: ✅ CORRECT (90% confident) - "Both represent 150"
```

### Example 2: Precision Difference

```
Question: "What is the average value?"
Expected: "5.843"
Actual: "5.843333333"

Without LLM: ❌ INCORRECT (string mismatch)
With LLM: ✅ CORRECT (95% confident) - "Numerical match within precision"
```

### Example 3: Semantic Equivalence

```
Question: "How many species are there?"
Expected: "3"
Actual: "There are 3 species"

Without LLM: ❌ INCORRECT (string mismatch)
With LLM: ✅ CORRECT (85% confident) - "Semantic match, both indicate 3"
```

### Example 4: Actually Wrong Answer

```
Question: "What is the maximum value?"
Expected: "100"
Actual: "200"

Without LLM: ❌ INCORRECT
With LLM: ❌ INCORRECT (100% confident) - "Values do not match"
```

## Technical Details

### Model

- **Default**: `gpt-4o-mini`
- **Why**: Balance of accuracy and cost
- **Alternative**: Can be changed to `gpt-4` for even higher accuracy

### Evaluation Process

1. **Quick checks** (no API call):
   - Exact string match
   - Numeric comparison

2. **LLM call** (if needed):
   - Structured prompt with question context
   - Temperature: 0.1 (deterministic)
   - Max tokens: 200

3. **Response parsing**:
   - Format: `CORRECT|explanation|confidence`
   - Fallback handling for edge cases

### Error Handling

- API failures → fallback to string comparison
- Invalid responses → confidence 0.5
- Network errors → cached comparison

## Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_key_here
```

### Custom Model

```python
from src.llm_judge import LLMJudge

# Use GPT-4 for highest accuracy
judge = LLMJudge(model="gpt-4")

# Or use GPT-3.5 for lowest cost
judge = LLMJudge(model="gpt-3.5-turbo")
```

## Best Practices

### 1. Spot Check Mode
Use LLM Judge only for questions that failed simple matching:
```python
if not simple_match:
    use_llm_judge = True
```

### 2. Batch Processing
Process multiple evaluations in one session to amortize setup costs.

### 3. Cache Results
Store LLM judgments to avoid re-evaluating same answers.

### 4. Monitor Costs
Track API usage using OpenAI dashboard.

### 5. Confidence Thresholds
Set minimum confidence for accepting evaluations:
```python
if confidence > 0.8:
    accept_result()
```

## Troubleshooting

### Issue: LLM Judge Unavailable

**Cause**: Missing llm_judge module or import error

**Solution**:
```bash
# Check if module exists
ls src/llm_judge.py

# Verify imports work
python3 -c "from src.llm_judge import LLMJudge"
```

### Issue: API Errors

**Cause**: Invalid API key or rate limits

**Solution**:
```bash
# Check API key
echo $OPENAI_API_KEY

# Verify key works
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Issue: Slow Evaluations

**Cause**: API latency for each call

**Solution**:
- Use LLM Judge selectively
- Implement caching
- Consider batch API calls

### Issue: Unexpected Results

**Cause**: LLM misinterpretation

**Solution**:
- Check confidence score
- Review explanation
- Add more context to questions
- Adjust model temperature

## FAQ

**Q: How accurate is LLM Judge?**  
A: Typically 95%+ accuracy, much higher than simple string matching.

**Q: Can I use without OpenAI API?**  
A: Currently requires OpenAI. Future: support for local models.

**Q: Is it slow?**  
A: ~1-2 seconds per evaluation. Use selectively for best performance.

**Q: Can I customize the prompts?**  
A: Yes, edit `src/llm_judge.py` → `_create_evaluation_prompt()`

**Q: What if I run out of API credits?**  
A: System falls back to simple string/numeric comparison automatically.

## Future Enhancements

- [ ] Support for local LLMs (Llama, Mistral)
- [ ] Caching layer for repeated evaluations
- [ ] Batch API calls for efficiency
- [ ] Custom prompt templates
- [ ] Multi-model consensus voting
- [ ] Fine-tuned model for answer matching

---

**Enable LLM Judge for More Accurate Evaluations! ⚖️✨**
