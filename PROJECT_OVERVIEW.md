# DataFrame Q&A Benchmark - Project Overview

Comprehensive benchmarking system for DataFrame Q&A frameworks with interactive visualization.

---

## 🎯 Project Goal

Compare and evaluate three popular DataFrame Q&A frameworks:
- **PandasAI** - AI-powered pandas agent
- **Sketch** - Pandas extension with AI capabilities  
- **LangChain Pandas Agent** - LangChain's DataFrame analysis tool

---

## 📊 Current Status

**Version**: 1.2.0  
**Status**: ✅ Production Ready  
**Datasets**: 11 (4 sklearn + 2 synthetic + 5 external)  
**Frameworks**: 3 (PandasAI, Sketch, LangChain)  
**Lines of Code**: ~2,500+  
**Documentation**: 12 guides

---

## 🚀 Key Features

### 1. Benchmark System
- ✅ Automated Q&A testing across datasets
- ✅ Ground truth comparison
- ✅ Detailed logging and error tracking
- ✅ JSON result export
- ✅ Command-line interface

### 2. Dataset Collection
- ✅ 4 sklearn datasets (iris, wine, diabetes, custom sales)
- ✅ 2 synthetic datasets (ecommerce, employees)
- ✅ 5 external datasets (titanic, happiness, supermarket, covid, stackoverflow)
- ✅ Pre-defined Q&A pairs for each
- ✅ Easy dataset addition

### 3. Interactive Dashboard (NEW!)
- ✅ Streamlit web interface
- ✅ 5 distinct views (Overview, Details, Compare, Trends, Raw Data)
- ✅ Interactive filters and navigation
- ✅ Rich visualizations (box plots, bar charts, line charts, radar, pie)
- ✅ Historical trend tracking
- ✅ CSV/JSON export
- ✅ Question-level debugging

### 4. Comprehensive Documentation
- ✅ Main README with quick start
- ✅ Streamlit dashboard guide (330+ lines)
- ✅ External datasets guide
- ✅ Synthetic datasets guide
- ✅ Testing procedures
- ✅ Logs inspection guide
- ✅ Quick reference cards

---

## 📁 Project Structure

```
dashboard-qa-benchmark/
├── Core Application
│   ├── main.py                          # CLI benchmark runner
│   ├── streamlit_app.py                 # Web dashboard (600+ lines)
│   ├── requirements-benchmarks.txt      # CLI dependencies only
│   ├── requirements-streamlit.txt       # Streamlit dashboard dependencies
│   └── requirements.txt                 # Primary Streamlit dependency list
│
├── Source Code
│   ├── src/benchmark_datasets.py        # Dataset loaders + Q&A
│   ├── src/external_datasets.py         # External dataset loaders
│   ├── src/synthetic_generator.py       # Synthetic data generation
│   ├── src/framework_integrations.py    # Framework wrappers
│   └── src/evaluation.py                # Result comparison
│
├── Scripts
│   ├── quickstart.sh                    # Initial setup
│   ├── benchmark_external.sh            # Run all external datasets
│   ├── start_dashboard.sh               # Launch Streamlit
│   ├── list_datasets.py                 # List available datasets
│   └── view_logs.py                     # Inspect execution logs
│
├── Documentation
│   ├── README.md                        # Main documentation
│   ├── STREAMLIT_GUIDE.md               # Dashboard guide
│   ├── DASHBOARD_QUICKSTART.md          # Quick dashboard reference
│   ├── EXTERNAL_DATASETS.md             # External datasets guide
│   ├── SYNTHETIC_DATASETS.md            # Synthetic datasets guide
│   ├── DATASETS_QUICK_REFERENCE.md      # All datasets overview
│   ├── QUICKSTART_GUIDE.md              # Getting started
│   ├── TESTING.md                       # Testing procedures
│   ├── LOGS_GUIDE.md                    # Log inspection
│   └── RESULTS.md                       # Results format
│
├── Changelogs
│   ├── CHANGELOG_EXTERNAL_DATASETS.md   # External datasets addition
│   └── CHANGELOG_STREAMLIT.md           # Dashboard feature
│
└── Results
    └── results/*.json                   # Benchmark results
```

---

## 🎨 Workflow

### Standard Workflow
```
1. Run Benchmark
   python3 main.py --dataset iris --save-results

2. Launch Dashboard
   ./start_dashboard.sh

3. Analyze Results
   - View overview metrics
   - Compare frameworks
   - Inspect failed questions
   - Track trends

4. Export Data
   - Download CSV/JSON
   - Further analysis
```

### Batch Workflow
```
1. Run All Datasets
   ./benchmark_external.sh

2. Launch Dashboard
   streamlit run streamlit_app.py

3. Comprehensive Analysis
   - Compare all frameworks
   - Identify best/worst datasets
   - Track historical performance
```

---

## 📊 Dashboard Views

### 📈 Overview
High-level metrics and performance summary

**Metrics:**
- Total runs
- Datasets tested
- Average accuracy
- Top framework

**Charts:**
- Accuracy distribution (box plot)
- Performance by dataset (bar chart)
- Framework statistics (table)

### 🔍 Detailed Results
Question-by-question analysis

**Features:**
- Select specific run
- View all questions
- Framework responses
- Execution logs
- Error messages

### 📊 Compare Frameworks
Side-by-side comparison

**Metrics:**
- Avg/Min/Max accuracy
- Success rate
- Error count

**Charts:**
- Radar chart comparison
- Win rate pie chart

### ⏱️ Historical Trends
Performance over time

**Charts:**
- Accuracy line chart
- Dataset-specific trends
- Moving average

### 🗂️ Raw Data
Data export and statistics

**Features:**
- CSV download
- JSON download
- Column selection
- Descriptive statistics

---

## 🔧 Technical Stack

### Core Technologies
- **Python 3.11+**
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations
- **Scikit-learn** - Built-in datasets

### Frameworks Under Test
- **PandasAI 2.2.0** - with LiteLLM
- **LangChain 0.3.0** - with experimental
- **Custom Sketch** - OpenAI-based wrapper

### Visualization
- **Streamlit 1.28.0** - Web dashboard
- **Plotly 5.18.0** - Interactive charts
- **Tabulate 0.9.0** - Terminal tables

### AI/LLM
- **OpenAI API** - GPT-4 for all frameworks
- **python-dotenv** - Environment management

---

## 📈 Performance Metrics

### Accuracy by Framework (Average)
- **PandasAI**: 77.8 - 100%
- **Sketch**: 25 - 100%
- **LangChain**: 50 - 100%

*Note: Varies by dataset and question complexity*

### Dataset Difficulty
- **Easy**: iris, sales, happiness (90%+ accuracy)
- **Medium**: wine, diabetes, titanic, supermarket (70-90%)
- **Challenging**: covid, stackoverflow (50-75%)

---

## 🎓 Use Cases

### 1. Framework Selection
**Goal**: Choose best framework for production

**Steps:**
1. Run benchmarks on relevant datasets
2. Launch dashboard
3. Compare frameworks view
4. Review accuracy, reliability, error rate
5. Make decision

### 2. Dataset Evaluation
**Goal**: Understand dataset difficulty

**Steps:**
1. Run all frameworks on dataset
2. Check detailed results
3. Identify challenging questions
4. Refine questions or data

### 3. Performance Monitoring
**Goal**: Track framework improvements

**Steps:**
1. Regular benchmark runs
2. Historical trends view
3. Monitor moving average
4. Identify regressions

### 4. Debugging
**Goal**: Fix failed questions

**Steps:**
1. Find failed question in detailed view
2. Review framework reasoning
3. Check execution logs
4. Identify root cause
5. Fix and re-test

### 5. Reporting
**Goal**: Share results with team

**Steps:**
1. Run comprehensive benchmarks
2. Export data from dashboard
3. Create custom visualizations
4. Present findings

---

## 🚀 Quick Start

### First Time Setup
```bash
# 1. Install dependencies (Streamlit UI)
pip install --user -r requirements.txt

# CLI benchmarks only
# pip install --user -r requirements-benchmarks.txt

# 2. Set API key
cp .env.example .env
# Edit .env with your OpenAI API key

# 3. Run first benchmark
python3 main.py --dataset iris --save-results

# 4. Launch dashboard
./start_dashboard.sh
```

### Daily Usage
```bash
# Run benchmark
python3 main.py --dataset <name> --save-results

# View results
streamlit run streamlit_app.py
```

---

## 📊 Statistics

### Project Metrics
- **Total Files**: 25+
- **Python Files**: 10
- **Documentation**: 12 files
- **Scripts**: 5
- **Lines of Code**: 2,500+
- **Lines of Docs**: 3,000+

### Dataset Coverage
- **Total Datasets**: 11
- **Total Questions**: 47
- **Domains**: Science, Business, Social, Healthcare, Transportation

### Framework Coverage
- **Frameworks**: 3
- **API Calls**: ~50 per full benchmark
- **Average Runtime**: 2-5 min per dataset

---

## 💡 Best Practices

### Benchmarking
1. Always use `--save-results` flag
2. Run on multiple datasets for comparison
3. Check logs for failed questions
4. Document any custom datasets

### Dashboard Usage
1. Start with Overview for big picture
2. Use filters to focus analysis
3. Export data for offline analysis
4. Check trends regularly

### Maintenance
1. Update frameworks regularly
2. Add new datasets as needed
3. Monitor API costs
4. Archive old results periodically

---

## 🔮 Future Roadmap

### Short Term
- [ ] Add more external datasets
- [ ] Implement custom dataset upload
- [ ] Add framework configuration options
- [ ] Improve error handling

### Medium Term
- [ ] Multi-model support (Claude, Gemini)
- [ ] Automated benchmarking schedule
- [ ] Performance alerts
- [ ] API for programmatic access

### Long Term
- [ ] Real-time benchmarking
- [ ] Collaborative features
- [ ] Custom visualization builder
- [ ] ML-based framework selection

---

## 🤝 Contributing

### Adding Datasets
1. Create loader in `src/external_datasets.py` or `src/synthetic_generator.py`
2. Add benchmark function in `src/benchmark_datasets.py`
3. Register in `AVAILABLE_DATASETS`
4. Document in relevant guide

### Adding Frameworks
1. Create wrapper in `src/framework_integrations.py`
2. Implement `FrameworkIntegration` interface
3. Add to main benchmark loop
4. Update documentation

### Improving Dashboard
1. Edit `streamlit_app.py`
2. Test all views
3. Update STREAMLIT_GUIDE.md
4. Add screenshots if relevant

---

## 📞 Support

### Documentation
- **General**: README.md
- **Dashboard**: STREAMLIT_GUIDE.md
- **Datasets**: EXTERNAL_DATASETS.md, SYNTHETIC_DATASETS.md
- **Testing**: TESTING.md
- **Logs**: LOGS_GUIDE.md

### Quick References
- **Datasets**: DATASETS_QUICK_REFERENCE.md
- **Dashboard**: DASHBOARD_QUICKSTART.md
- **Getting Started**: QUICKSTART_GUIDE.md

---

## ✅ Quality Metrics

### Testing
- ✅ All 11 datasets tested
- ✅ All 3 frameworks working
- ✅ All dashboard views functional
- ✅ Export functionality verified

### Documentation
- ✅ Comprehensive README
- ✅ Detailed guides for all features
- ✅ Quick reference cards
- ✅ Code comments

### Code Quality
- ✅ Modular architecture
- ✅ Error handling
- ✅ Logging system
- ✅ Type hints (partial)

---

## 🎉 Summary

**DataFrame Q&A Benchmark** is a complete solution for:
- ✅ Evaluating DataFrame Q&A frameworks
- ✅ Tracking performance over time
- ✅ Debugging failed questions
- ✅ Visualizing results interactively
- ✅ Making data-driven framework decisions

**Ready to use. Production-grade. Well-documented.**

---

**Launch Commands:**
```bash
# Run benchmark
python3 main.py --dataset iris --save-results

# Launch dashboard
./start_dashboard.sh

# List datasets
python3 list_datasets.py
```

**🎊 Enjoy benchmarking!**
