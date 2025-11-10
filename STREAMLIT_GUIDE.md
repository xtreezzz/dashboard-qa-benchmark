# Streamlit Dashboard Guide

Interactive web-based dashboard for visualizing and analyzing DataFrame Q&A benchmark results.

## 🚀 Quick Start

### Launch the Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Alternative: Specify Port

```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📊 Features

### 1. Overview Page (📈)

Main dashboard showing high-level metrics:

- **Total Runs**: Number of benchmark runs executed
- **Datasets**: Number of unique datasets tested
- **Average Accuracy**: Overall accuracy across all frameworks
- **Top Framework**: Best performing framework

**Visualizations:**
- Accuracy by Framework (table with mean, std dev, count)
- Accuracy Distribution (box plot)
- Performance by Dataset (grouped bar chart)

### 2. Detailed Results (🔍)

Question-by-question analysis of benchmark runs:

**Features:**
- Select specific benchmark run by date and dataset
- View summary statistics for all frameworks
- Analyze individual questions with:
  - Ground truth answer and reasoning
  - Each framework's answer and reasoning
  - Match status (✅ correct / ❌ incorrect)
  - Execution logs (if available)
  - Error messages (if any)

**Use Case:** Deep dive into why a framework succeeded or failed on specific questions

### 3. Compare Frameworks (📊)

Side-by-side framework comparison:

**Metrics:**
- Overall Performance Table:
  - Average Accuracy
  - Standard Deviation
  - Min/Max Accuracy
  - Total Correct/Questions
  - Success Rate

**Visualizations:**
- Performance Radar Chart (Accuracy, Correctness, Reliability)
- Head-to-Head Win Rate (pie chart showing dataset wins)

**Use Case:** Determine which framework is best for your use case

### 4. Historical Trends (⏱️)

Track performance changes over time:

**Visualizations:**
- Framework Accuracy Over Time (line chart)
- Dataset-Specific Trends (scatter plot with question counts)
- 7-Run Moving Average (smoothed trend line)

**Use Case:** Monitor improvements/regressions, identify patterns

### 5. Raw Data (🗂️)

Access and export raw results:

**Features:**
- Download as CSV
- Download as JSON
- Column selection for custom views
- Descriptive statistics

**Use Case:** Further analysis in external tools (Excel, Jupyter, etc.)

## 🎛️ Filters & Navigation

### Sidebar Filters

**Dataset Filter:**
- Select specific dataset or "All"
- Affects all views except Detailed Results

**Framework Filter:**
- Select specific framework or "All"
- Useful for focusing on one framework's performance

**Navigation:**
- Radio buttons to switch between pages
- Current page highlighted

## 📈 Usage Scenarios

### Scenario 1: First-Time User

1. Launch dashboard: `streamlit run streamlit_app.py`
2. Go to **Overview** page
3. Check overall statistics
4. Review performance by dataset chart
5. Identify best/worst performing datasets

### Scenario 2: Framework Selection

1. Navigate to **Compare Frameworks**
2. Review overall performance table
3. Check radar chart for balanced performance
4. Look at win rate to see which framework excels
5. Make selection based on your priorities (accuracy vs reliability)

### Scenario 3: Debugging Failed Questions

1. Go to **Detailed Results**
2. Select the problematic benchmark run
3. Click on the failed question
4. Review framework responses
5. Check execution logs for errors
6. Compare reasoning between frameworks

### Scenario 4: Performance Monitoring

1. Navigate to **Historical Trends**
2. View accuracy over time chart
3. Select specific dataset for detailed trend
4. Check moving average for overall trajectory
5. Identify when performance changed

### Scenario 5: Data Export

1. Go to **Raw Data**
2. Select columns to include
3. Download as CSV or JSON
4. Import into Excel/Python for custom analysis

## 🎨 Visual Elements

### Color Coding

- **PandasAI**: Orange (#ff7f0e)
- **Sketch**: Green (#2ca02c)
- **LangChain**: Red (#d62728)

### Status Indicators

- ✅ **Correct**: Green, bold
- ❌ **Incorrect**: Red, bold

### Charts

- **Box Plot**: Distribution and outliers
- **Bar Chart**: Comparison across categories
- **Line Chart**: Trends over time
- **Scatter Plot**: Individual data points with size/color
- **Radar Chart**: Multi-dimensional comparison
- **Pie Chart**: Proportional representation

## 💡 Tips & Tricks

### Performance

1. **Caching**: Results are cached automatically - reload page to refresh
2. **Large Datasets**: Use filters to reduce data volume
3. **Slow Loading**: Close and reopen specific visualizations

### Data Interpretation

1. **Accuracy**: Higher is better, but check consistency (std dev)
2. **Win Rate**: Shows which framework is best most often
3. **Moving Average**: Smooths out noise in historical trends
4. **Error Count**: Zero errors indicates reliability

### Workflow

1. **Start Broad**: Begin with Overview, narrow down
2. **Compare First**: Use framework comparison before detailed analysis
3. **Historical Context**: Check trends to understand current results
4. **Export Last**: Download data after filtering and analysis

## 🔧 Technical Details

### Data Source

Dashboard reads from `results/` directory:
- Format: `<dataset>_results_<timestamp>.json`
- Auto-discovers all result files
- Sorts by timestamp (newest first)

### Requirements

```
streamlit>=1.39
plotly>=5.18
pandas==2.1.4
```

Install: `pip install --user streamlit plotly`

### File Structure

```python
streamlit_app.py
├── load_results_from_file()    # Load single JSON result
├── get_all_results_files()     # Discover all results
├── parse_result_filename()     # Extract metadata
├── aggregate_all_results()     # Combine into DataFrame
└── display_*()                 # Page-specific rendering
```

## 🚨 Troubleshooting

### Issue: Installation fails on Streamlit Cloud (default Python 3.13)

**Symptom:** The build log shows `_PyLong_AsByteArray` compilation errors while
trying to install `pandas==2.1.4`.

**Solution:**
1. Pull the latest repository version — the new `runtime.txt` file pins the
   app to Python 3.12, which provides pre-built wheels for `pandas==2.1.4`.
2. Redeploy (Streamlit Cloud: `Settings → Advanced settings → Clear cache` →
   `Deploy`), or rerun `pip install -r requirements.txt` locally with Python
   3.12.
3. If you must stay on Python 3.13, override the pandas pin with
   `pip install "pandas>=2.2.3"` after deployment to pick up the newer wheels.

### Issue: No results found

**Solution:**
1. Run benchmarks first: `python3 main.py --dataset iris --save-results`
2. Check `results/` directory exists
3. Verify JSON files are present

### Issue: Dashboard won't start

**Solution:**
1. Check Streamlit is installed: `streamlit --version`
2. Try different port: `streamlit run streamlit_app.py --server.port 8502`
3. Check for port conflicts: `lsof -i :8501`

### Issue: Charts not displaying

**Solution:**
1. Verify Plotly is installed: `python3 -c "import plotly; print(plotly.__version__)"`
2. Clear browser cache
3. Try different browser

### Issue: Old data showing

**Solution:**
1. Click "Rerun" button in top-right
2. Or refresh page (Cmd/Ctrl + R)
3. Or clear cache: Hamburger menu → Clear cache

## 📊 Example Workflows

### Quick Health Check

```bash
# Run a benchmark
python3 main.py --dataset iris --save-results

# Launch dashboard
streamlit run streamlit_app.py

# Check Overview page
# ✓ Accuracy looks good
# ✓ No errors
```

### Framework Comparison Study

```bash
# Run multiple datasets
./benchmark_external.sh

# Launch dashboard
streamlit run streamlit_app.py

# Go to Compare Frameworks
# Review performance table
# Check radar chart
# Decision: Choose PandasAI for accuracy, LangChain for reliability
```

### Detailed Question Analysis

```bash
# Found an issue in results
streamlit run streamlit_app.py

# Navigate to Detailed Results
# Select failed run
# Click problematic question
# Review logs → Found: incorrect column name
# Fix in code
```

## 🎯 Best Practices

1. **Regular Benchmarking**: Run benchmarks regularly to build historical data
2. **Consistent Naming**: Keep dataset names consistent for trend analysis
3. **Save Results**: Always use `--save-results` flag
4. **Review Logs**: Check execution logs for failed questions
5. **Export Data**: Download data periodically for backup

## 🔄 Updates

To update the dashboard:

1. Pull latest code
2. Restart Streamlit: Ctrl+C, then `streamlit run streamlit_app.py`
3. Or use "Rerun" button in browser

## 📞 Need Help?

- Check `README.md` for general usage
- See `TESTING.md` for running benchmarks
- Review `LOGS_GUIDE.md` for log analysis
- Consult `RESULTS.md` for result format details

---

**Launch Command:**
```bash
streamlit run streamlit_app.py
```

**Default URL:** http://localhost:8501

**Enjoy analyzing your benchmarks! 📊✨**
