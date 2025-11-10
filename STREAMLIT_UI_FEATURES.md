# Streamlit UI Features - Reproduction Code Display

## New Features Added

### 🔄 Reproduction Code Display

For each framework query result, you can now view and download:

#### 1. **Framework Reproduction Code**
Located in expandable section: **"🔄 Reproduction Code"**

**What it shows:**
- Ready-to-run Python code to reproduce the exact query
- Includes first 10 rows of sample data
- Framework-specific setup (PandasAI/Sketch/LangChain)
- Complete query execution

**Features:**
- ✅ Syntax-highlighted Python code
- ✅ Download button to save as `.py` file
- ✅ Reminder to set `OPENAI_API_KEY` environment variable

**Example filename:** `reproduce_pandasai_q1.py`

#### 2. **Evaluation Details**
Located in expandable section: **"⚖️ Evaluation Details"**

**What it shows:**
- **Rule-Based Evaluation:**
  - Exact match check (✅/❌)
  - Contains match check (✅/❌)
  - Numeric match check (✅/❌)
  - Overall result (✅/❌)

- **🤖 LLM Judge Evaluation:**
  - Correctness verdict (✅/❌)
  - Confidence score with emoji (🟢/🟡/🔴)
  - Explanation of decision

#### 3. **LLM Judge Details**
Located under Evaluation Details: **"🔬 LLM Judge Details"**

**Sub-sections:**

##### a) 📝 Prompt sent to LLM Judge
- Full prompt that was sent to GPT-4o-mini
- Shows question, expected answer, actual answer, reasoning

##### b) 💬 Response from LLM Judge
- Raw response from GPT-4o-mini
- Format: `CORRECT|explanation|confidence` or `INCORRECT|explanation|confidence`

##### c) 🔄 LLM Judge Reproduction Code
- Ready-to-run Python code to reproduce the LLM Judge evaluation
- Uses OpenAI API directly
- Includes exact prompt and parameters

**Features:**
- ✅ Syntax-highlighted code
- ✅ Download button to save as `.py` file
- ✅ Exact reproduction of judge evaluation

**Example filename:** `reproduce_llm_judge_pandasai_q1.py`

## How to Access

### Step 1: Open Streamlit Dashboard
```bash
cd /Users/family/dashboard-qa-benchmark
python3 -m streamlit run streamlit_app.py
```

### Step 2: Navigate to Detailed Results
In the sidebar, select: **"🔍 Detailed Results"**

### Step 3: Select a Dataset and Question
1. Choose dataset from dropdown (e.g., "iris")
2. Select question number
3. Expand any framework section (PandasAI, Sketch, or LangChain)

### Step 4: Explore Reproduction Code
You'll see several expandable sections:
- 📋 **View Execution Logs** - Full framework execution logs
- 🔄 **Reproduction Code** - Framework query reproduction code
- ⚖️ **Evaluation Details** - Complete evaluation breakdown
  - 📝 **Prompt sent to LLM Judge** - LLM Judge input
  - 💬 **Response from LLM Judge** - LLM Judge output
  - 🔄 **LLM Judge Reproduction Code** - Judge evaluation reproduction code

## Visual Layout

```
┌─ PandasAI ✅ 🟢 ─────────────────────────────────┐
│                                                    │
│ ✅ CORRECT        Answer: 150                     │
│ Eval: LLM Judge   Reasoning: PandasAI processed...│
│                                                    │
│ ▶ 📋 View Execution Logs                          │
│   └─ Full logs with timestamps                    │
│      └─ 📥 Download Logs button                   │
│                                                    │
│ ▶ 🔄 Reproduction Code                            │
│   └─ Python code to reproduce query               │
│      └─ 📥 Download Reproduction Code button      │
│                                                    │
│ ▶ ⚖️ Evaluation Details                           │
│   ├─ Rule-Based: ✅ Exact ✅ Contains ✅ Numeric  │
│   └─ LLM Judge: ✅ Correct 🟢 100% confident      │
│                                                    │
│   ▶ 📝 Prompt sent to LLM Judge                   │
│     └─ Full evaluation prompt                     │
│                                                    │
│   ▶ 💬 Response from LLM Judge                    │
│     └─ Raw LLM response                           │
│                                                    │
│   ▶ 🔄 LLM Judge Reproduction Code                │
│     └─ Python code to reproduce evaluation        │
│        └─ 📥 Download LLM Judge Code button       │
└────────────────────────────────────────────────────┘
```

## Example: Using Downloaded Code

### Framework Reproduction Code
```bash
# Download the code from UI
# Save as: reproduce_pandasai_q1.py

# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run the code
python reproduce_pandasai_q1.py
```

### LLM Judge Reproduction Code
```bash
# Download the code from UI
# Save as: reproduce_llm_judge_pandasai_q1.py

# Set your API key
export OPENAI_API_KEY="your-key-here"

# Run the code
python reproduce_llm_judge_pandasai_q1.py
```

## Benefits

### 🔍 Full Transparency
- See exactly what code was executed
- View exact prompts sent to APIs
- Understand evaluation logic

### 🔄 Easy Reproducibility
- One-click download of reproduction code
- No manual code reconstruction needed
- Works immediately with API key

### 🐛 Debugging Made Easy
- Copy code and modify parameters
- Test with different inputs
- Understand failures

### 📚 Learning Tool
- See how each framework works
- Learn prompt engineering
- Understand evaluation methodology

## Confidence Score Indicators

| Emoji | Confidence | Meaning |
|-------|-----------|---------|
| 🟢 | > 80% | High confidence - very likely correct |
| 🟡 | 50-80% | Medium confidence - probably correct |
| 🔴 | < 50% | Low confidence - uncertain |

## Cost Information

Each LLM Judge evaluation costs approximately:
- **~$0.0001** per evaluation (GPT-4o-mini)
- Very low cost for high accuracy

## Tips

### 1. Compare Multiple Frameworks
Open multiple framework sections to compare:
- Different code approaches
- Different evaluation results
- Different confidence scores

### 2. Download for Later Analysis
Use download buttons to:
- Save code for offline review
- Build your own test suite
- Archive successful patterns

### 3. Modify and Test
Download reproduction code and:
- Change question parameters
- Test with different data
- Experiment with frameworks

### 4. Share with Team
- Download code snippets
- Share evaluation logic
- Document decisions

## Keyboard Shortcuts

- **Click expander** - Toggle section open/closed
- **Ctrl/Cmd + Click download** - Download without preview
- **Shift + Click expander** - Keep other sections open

## Technical Details

### Code Generation
- Sample data: First 10 rows of dataset
- Format: CSV embedded in code
- Libraries: Exact versions used in benchmark

### LLM Judge Prompt
- Question context included
- Expected vs actual answers
- Evaluation criteria listed
- Response format specified

### Download Formats
- Framework code: `.py` (Python)
- LLM Judge code: `.py` (Python)
- Logs: `.txt` (Plain text)

## Troubleshooting

### "Reproduction code not available"
- Older result files may not have reproduction code
- Re-run benchmarks to generate new results

### "Download button not working"
- Check browser download settings
- Try different browser
- Check file permissions

### "Code doesn't run"
- Ensure `OPENAI_API_KEY` is set
- Install required packages
- Check Python version (3.8+)

## Future Enhancements

Planned features:
- Copy code button (without download)
- Run code directly in browser
- Edit and test parameters
- Save modified versions

---

**Last Updated**: November 9, 2025
**Streamlit Version**: Latest
**Dashboard Port**: http://localhost:8501
