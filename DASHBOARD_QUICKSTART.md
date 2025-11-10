# 📊 Dashboard Quick Start

## Launch Dashboard

```bash
./start_dashboard.sh
```

or

```bash
streamlit run streamlit_app.py
```

Opens at: **http://localhost:8501**

---

## 5 Main Views

### 1. 📈 Overview
- Total runs, datasets, avg accuracy
- Framework comparison table
- Performance charts

### 2. 🔍 Detailed Results
- Select specific benchmark run
- Question-by-question analysis
- View framework responses & logs

### 3. 📊 Compare Frameworks
- Side-by-side performance
- Radar chart comparison
- Win rate analysis

### 4. ⏱️ Historical Trends
- Accuracy over time
- Dataset-specific trends
- Moving average

### 5. 🗂️ Raw Data
- Export to CSV/JSON
- Custom column selection
- Data statistics

---

## Quick Actions

### Filter by Dataset
Sidebar → Dataset dropdown → Select dataset

### Filter by Framework
Sidebar → Framework dropdown → Select framework

### Export Data
Raw Data page → Download buttons

### Refresh Data
Top-right corner → "Rerun" button

---

## Common Tasks

### Compare All Frameworks
1. Go to "Compare Frameworks"
2. Review performance table
3. Check radar chart

### Debug Failed Question
1. Go to "Detailed Results"
2. Select problematic run
3. Click failed question
4. Review logs

### Track Improvements
1. Go to "Historical Trends"
2. Select dataset
3. View trend line

---

## Keyboard Shortcuts

- **R** - Rerun app
- **C** - Clear cache
- **Cmd/Ctrl + K** - Command palette

---

## Need Help?

Full guide: [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)

---

**Pro Tip:** Run benchmarks regularly to build historical data for trend analysis!
