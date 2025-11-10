#!/usr/bin/env python3
"""
Streamlit Dashboard for DataFrame Q&A Benchmark Visualization

Features:
- Load and view benchmark results from JSON files
- Compare framework performance across datasets
- View detailed question-by-question analysis
- Track accuracy trends over time
- Filter by dataset, framework, and date
"""
import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import io

# Add src to path for imports
sys.path.insert(0, 'src')

try:
    from llm_judge import LLMJudge, evaluate_with_llm_judge
    LLM_JUDGE_AVAILABLE = True
except ImportError:
    LLM_JUDGE_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="DataFrame Q&A Benchmark Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    .error-text {
        color: #dc3545;
        font-weight: bold;
    }
    .framework-pandasai {
        color: #ff7f0e;
    }
    .framework-sketch {
        color: #2ca02c;
    }
    .framework-langchain {
        color: #d62728;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_results_from_file(file_path: str) -> Dict[str, Any]:
    """Load benchmark results from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


@st.cache_data
def get_all_results_files() -> List[str]:
    """Get all result files from the results directory."""
    results_dir = Path("results")
    if not results_dir.exists():
        return []
    
    files = list(results_dir.glob("*_results_*.json"))
    return sorted([str(f) for f in files], reverse=True)


def parse_result_filename(filename: str) -> Dict[str, str]:
    """Parse dataset name and timestamp from filename."""
    basename = os.path.basename(filename)
    # Format: <dataset>_results_<timestamp>.json
    parts = basename.replace('.json', '').split('_results_')
    
    if len(parts) == 2:
        dataset = parts[0]
        timestamp = parts[1]
        try:
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            date_str = timestamp
        
        return {
            'dataset': dataset,
            'timestamp': timestamp,
            'date': date_str,
            'file': filename
        }
    return {'dataset': 'unknown', 'timestamp': '', 'date': '', 'file': filename}


# Don't cache this function - it needs to respond to toggle changes
def aggregate_all_results(use_llm_judge: bool = True) -> pd.DataFrame:
    """Aggregate accuracy from all result files.
    
    Args:
        use_llm_judge: If True, use LLM Judge results; if False, use rule-based results
    
    Note: Not cached to allow toggle to update results immediately
    """
    all_files = get_all_results_files()
    records = []
    
    for file_path in all_files:
        try:
            result = load_results_from_file(file_path)
            file_info = parse_result_filename(file_path)
            
            # Handle both old (list) and new (dict) formats
            if isinstance(result, list):
                # Old format: list of questions
                questions = result
            elif isinstance(result, dict) and 'results' in result:
                # New format with metadata
                questions = result['results']
                total_questions = len(questions)
                
                # Calculate stats per framework
                framework_stats = {}
                for question in questions:
                    for fw_name, fw_result in question.get('framework_results', {}).items():
                        if fw_name not in framework_stats:
                            framework_stats[fw_name] = {'correct': 0, 'total': 0, 'errors': 0}
                        
                        framework_stats[fw_name]['total'] += 1
                        
                        if fw_result.get('error'):
                            framework_stats[fw_name]['errors'] += 1
                        else:
                            # Use saved comparison result
                            if 'comparison' in fw_result:
                                comparison = fw_result['comparison']
                                
                                # Choose between rule-based and LLM Judge results
                                if use_llm_judge and comparison.get('llm_judge_match') is not None:
                                    # Use LLM Judge result
                                    is_match = comparison.get('llm_judge_match', False)
                                else:
                                    # Use rule-based result
                                    is_match = comparison.get('rule_based_match', False)
                            else:
                                # Fallback: rule-based comparison for old results
                                benchmark_answer = str(question.get('benchmark', {}).get('answer', '')).strip()
                                fw_answer = str(fw_result.get('answer', '')).strip()
                                
                                # Normalize for comparison
                                norm_benchmark = benchmark_answer.lower()
                                norm_framework = fw_answer.lower()
                                
                                # Exact match
                                exact_match = norm_benchmark == norm_framework
                                
                                # Contains match (framework answer contains benchmark)
                                contains_match = norm_benchmark in norm_framework
                                
                                # Numeric match (for numerical answers with tolerance)
                                numeric_match = False
                                try:
                                    bench_num = float(benchmark_answer)
                                    frame_num = float(fw_answer)
                                    # Allow 1% tolerance
                                    numeric_match = abs(bench_num - frame_num) / max(abs(bench_num), 1e-10) < 0.01
                                except (ValueError, TypeError):
                                    pass
                                
                                # Overall match
                                is_match = exact_match or contains_match or numeric_match
                            
                            if is_match:
                                framework_stats[fw_name]['correct'] += 1
                
                # Add records for each framework
                for fw_name, stats in framework_stats.items():
                    accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
                    records.append({
                        'dataset': file_info['dataset'],
                        'date': file_info['date'],
                        'timestamp': file_info['timestamp'],
                        'framework': fw_name,
                        'accuracy': accuracy,
                        'correct': stats['correct'],
                        'total': stats['total'],
                        'errors': stats['errors'],
                        'file': file_path
                    })
            else:
                # New format: dict with summary
                summary = result.get('summary', {})
                
                for framework, stats in summary.items():
                    if framework != 'total_questions':
                        records.append({
                            'dataset': file_info['dataset'],
                            'date': file_info['date'],
                            'timestamp': file_info['timestamp'],
                            'framework': framework,
                            'accuracy': stats.get('accuracy', 0),
                            'correct': stats.get('correct', 0),
                            'total': stats.get('total', 0),
                            'errors': stats.get('errors', 0),
                            'file': file_path
                        })
        except Exception as e:
            st.sidebar.error(f"Error loading {os.path.basename(file_path)}: {str(e)[:100]}")
    
    return pd.DataFrame(records)


def display_question_details(result: Dict[str, Any], question_idx: int):
    """Display detailed view of a single question with both evaluation methods."""
    # Handle both old (list) and new (dict with questions) formats
    if isinstance(result, list):
        questions = result
    elif isinstance(result, dict) and 'results' in result:
        # New format with metadata
        questions = result['results']
    else:
        questions = result.get('questions', [])
    
    if 0 <= question_idx < len(questions):
        q_data = questions[question_idx]
        
        # Get question text
        question_text = q_data.get('question', 'Unknown question')
        st.subheader(f"Question {question_idx + 1}: {question_text}")
        
        # Ground truth
        st.markdown("### 🎯 Ground Truth")
        col1, col2 = st.columns([1, 2])
        
        # Handle both old and new format for benchmark/ground truth
        if 'benchmark' in q_data:
            # Old format
            benchmark = q_data['benchmark']
            expected_answer = benchmark.get('answer', 'N/A')
            expected_reasoning = benchmark.get('reasoning', 'No reasoning')
        else:
            # New format
            expected_answer = q_data.get('expected_answer', 'N/A')
            expected_reasoning = q_data.get('expected_reasoning', 'No reasoning')
        
        with col1:
            st.metric("Answer", expected_answer)
        with col2:
            st.info(expected_reasoning)
        
        st.markdown("---")
        
        # Framework responses
        st.markdown("### 🤖 Framework Responses")
        
        # Get framework results - handle both formats
        if 'framework_results' in q_data:
            # Old format
            fw_results = q_data['framework_results']
        else:
            # New format
            fw_results = q_data.get('results', {})
        
        for fw_name, fw_result in fw_results.items():
            fw_answer = str(fw_result.get('answer', '')).strip()
            
            # Use pre-calculated comparison results
            comparison = fw_result.get('comparison', {})
            
            # Get both evaluation results
            rule_match = comparison.get('rule_based_match', False)
            llm_match = comparison.get('llm_judge_match', False)
            
            # Get LLM Judge confidence
            llm_judge = comparison.get('llm_judge', {})
            confidence = llm_judge.get('confidence', 0) if llm_judge else 0
            confidence_color = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.5 else "🔴"
            
            # Title shows both evaluations
            status_text = f"📊 {'✅' if rule_match else '❌'}  🤖 {'✅' if llm_match else '❌'} {confidence_color}"
            
            with st.expander(f"**{fw_name}** {status_text}", expanded=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("⚖️ **Evaluation Results:**")
                    
                    # Rule-based result
                    if rule_match:
                        st.markdown('📊 <span class="success-text">✅ CORRECT (Rule)</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('📊 <span class="error-text">❌ INCORRECT (Rule)</span>', unsafe_allow_html=True)
                    
                    # LLM Judge result
                    if llm_match:
                        st.markdown(f'🤖 <span class="success-text">✅ CORRECT (LLM {confidence:.0%})</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'🤖 <span class="error-text">❌ INCORRECT (LLM {confidence:.0%})</span>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    answer_display = fw_result.get('answer', 'N/A')
                    if not answer_display:
                        answer_display = "(No answer)"
                    st.metric("Answer", answer_display)
                
                with col2:
                    st.markdown("**Reasoning:**")
                    reasoning = fw_result.get('reasoning', 'No reasoning provided')
                    if not reasoning:
                        reasoning = "No reasoning provided"
                    st.write(reasoning)
                
                # Show error if present
                if fw_result.get('error'):
                    st.error(f"Error: {fw_result['error']}")
                
                # Show logs if available
                if fw_result.get('logs'):
                    with st.expander("📋 View Execution Logs"):
                        st.code(fw_result['logs'], language='text')
                        
                        # Download logs button
                        logs_text = fw_result['logs']
                        st.download_button(
                            label="📥 Download Logs",
                            data=logs_text,
                            file_name=f"{fw_name}_q{question_idx+1}_logs.txt",
                            mime="text/plain",
                            key=f"logs_{fw_name}_{question_idx}"
                        )
                
                # Show reproduction code if available
                if fw_result.get('reproduction_code'):
                    with st.expander("🔄 Reproduction Code"):
                        st.markdown(f"**Copy this code to reproduce the {fw_name} query:**")
                        st.code(fw_result['reproduction_code'], language='python')
                        
                        # Download reproduction code button
                        code_text = fw_result['reproduction_code']
                        st.download_button(
                            label="📥 Download Reproduction Code",
                            data=code_text,
                            file_name=f"reproduce_{fw_name.lower()}_q{question_idx+1}.py",
                            mime="text/x-python",
                            key=f"code_{fw_name}_{question_idx}"
                        )
                        st.caption("💡 Set OPENAI_API_KEY environment variable before running")
                
                # Show comparison details if available (includes LLM Judge)
                if fw_result.get('comparison'):
                    comparison = fw_result['comparison']
                    
                    with st.expander("⚖️ Evaluation Details"):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("**Rule-Based Evaluation:**")
                            st.write(f"Exact Match: {'✅' if comparison.get('exact_match') else '❌'}")
                            st.write(f"Contains Match: {'✅' if comparison.get('contains_match') else '❌'}")
                            st.write(f"Numeric Match: {'✅' if comparison.get('numeric_match') else '❌'}")
                            st.write(f"**Overall:** {'✅' if comparison.get('rule_based_match') else '❌'}")
                        
                        with col_b:
                            if comparison.get('llm_judge'):
                                llm_judge = comparison['llm_judge']
                                st.markdown("**🤖 LLM Judge Evaluation:**")
                                confidence = llm_judge.get('confidence', 0)
                                confidence_emoji = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.5 else "🔴"
                                st.write(f"Correct: {'✅' if llm_judge.get('is_correct') else '❌'}")
                                st.write(f"Confidence: {confidence_emoji} {confidence:.0%}")
                                st.caption(f"💭 {llm_judge.get('explanation', 'N/A')}")
                        
                        # Show LLM Judge log if available
                        if comparison.get('llm_judge_log'):
                            llm_log = comparison['llm_judge_log']
                            
                            st.markdown("---")
                            st.markdown("**🔬 LLM Judge Details:**")
                            
                            # Show prompt
                            with st.expander("📝 Prompt sent to LLM Judge"):
                                st.code(llm_log.get('prompt', 'N/A'), language='text')
                            
                            # Show response
                            with st.expander("💬 Response from LLM Judge"):
                                st.code(llm_log.get('response', 'N/A'), language='text')
                            
                            # Show reproduction code for LLM Judge
                            if llm_log.get('reproduction_code'):
                                with st.expander("🔄 LLM Judge Reproduction Code"):
                                    st.markdown("**Copy this code to reproduce the LLM Judge evaluation:**")
                                    st.code(llm_log['reproduction_code'], language='python')
                                    
                                    st.download_button(
                                        label="📥 Download LLM Judge Code",
                                        data=llm_log['reproduction_code'],
                                        file_name=f"reproduce_llm_judge_{fw_name.lower()}_q{question_idx+1}.py",
                                        mime="text/x-python",
                                        key=f"llm_judge_code_{fw_name}_{question_idx}"
                                    )


def main():
    # Header
    st.markdown('<p class="main-header">📊 DataFrame Q&A Benchmark Dashboard</p>', unsafe_allow_html=True)
    st.markdown("Compare PandasAI, Sketch, and LangChain performance across datasets")
    
    # Sidebar
    st.sidebar.header("🎛️ Filters & Options")
    
    # Load all results
    all_files = get_all_results_files()
    
    if not all_files:
        st.error("No result files found in the 'results/' directory.")
        st.info("Run benchmarks first: `python3 main.py --dataset iris --save-results`")
        return
    
    # Get aggregated data - will show both rule-based and LLM Judge results
    # Note: We now show BOTH evaluations side by side everywhere
    st.sidebar.markdown("---")
    st.sidebar.info("📊 **Showing both evaluations:**\n- Rule-based (exact/contains/numeric)\n- LLM Judge (GPT-4o-mini)")
    
    # Load both versions of aggregated data
    df_rule = aggregate_all_results(use_llm_judge=False)
    df_llm = aggregate_all_results(use_llm_judge=True)
    
    if df_rule.empty and df_llm.empty:
        st.error("No valid results found.")
        return
    
    # Use LLM Judge data as primary (for filters)
    df_all = df_llm if not df_llm.empty else df_rule
    
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filters")
    
    datasets = ['All'] + sorted(df_all['dataset'].unique().tolist())
    selected_dataset = st.sidebar.selectbox("Dataset", datasets)
    
    frameworks = ['All'] + sorted(df_all['framework'].unique().tolist())
    selected_framework = st.sidebar.selectbox("Framework", frameworks)
    
    # Apply filters to both dataframes
    df_rule_filtered = df_rule.copy()
    df_llm_filtered = df_llm.copy()
    
    if selected_dataset != 'All':
        df_rule_filtered = df_rule_filtered[df_rule_filtered['dataset'] == selected_dataset]
        df_llm_filtered = df_llm_filtered[df_llm_filtered['dataset'] == selected_dataset]
    if selected_framework != 'All':
        df_rule_filtered = df_rule_filtered[df_rule_filtered['framework'] == selected_framework]
        df_llm_filtered = df_llm_filtered[df_llm_filtered['framework'] == selected_framework]
    
    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    page = st.sidebar.radio(
        "Choose view:",
        ["📈 Overview", "🔍 Detailed Results", "📊 Compare Frameworks", "⏱️ Historical Trends", "🗂️ Raw Data"]
    )
    
    # Main content based on page selection - pass both dataframes
    if page == "📈 Overview":
        show_overview(df_rule_filtered, df_llm_filtered, df_rule, df_llm)
    
    elif page == "🔍 Detailed Results":
        show_detailed_results(all_files, selected_dataset, selected_framework)
    
    elif page == "📊 Compare Frameworks":
        show_framework_comparison(df_rule_filtered, df_llm_filtered)
    
    elif page == "⏱️ Historical Trends":
        show_historical_trends(df_rule, df_llm)
    
    elif page == "🗂️ Raw Data":
        show_raw_data(df_rule_filtered, df_llm_filtered)


def show_overview(df_rule_filtered: pd.DataFrame, df_llm_filtered: pd.DataFrame, 
                  df_rule_all: pd.DataFrame, df_llm_all: pd.DataFrame):
    """Display overview metrics with both rule-based and LLM Judge results.
    
    Args:
        df_rule_filtered: Filtered rule-based dataframe
        df_llm_filtered: Filtered LLM Judge dataframe
        df_rule_all: All rule-based results
        df_llm_all: All LLM Judge results
    """
    st.header("📈 Overview")
    
    # Create combined comparison table
    st.subheader("⚖️ Accuracy by Framework - Comparison")
    st.caption("📊 Rule-based vs 🤖 LLM Judge evaluation")
    
    # Get stats for both methods
    rule_stats = df_rule_all.groupby('framework')['accuracy'].agg(['mean', 'std', 'count']).reset_index()
    llm_stats = df_llm_all.groupby('framework')['accuracy'].agg(['mean', 'std', 'count']).reset_index()
    
    # Merge them
    combined = rule_stats.merge(llm_stats, on='framework', suffixes=('_rule', '_llm'))
    combined['Improvement'] = combined['mean_llm'] - combined['mean_rule']
    
    # Format for display
    display_df = pd.DataFrame({
        'Framework': combined['framework'],
        '📊 Rule-based': combined['mean_rule'].round(2),
        '🤖 LLM Judge': combined['mean_llm'].round(2),
        '🔺 Improvement': combined['Improvement'].round(2),
        'Runs': combined['count_llm']
    })
    
    st.dataframe(
        display_df.sort_values('🤖 LLM Judge', ascending=False),
        width="stretch",
        hide_index=True
    )
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_improvement = combined['Improvement'].mean()
        st.metric("⬆️ Avg Improvement", f"+{avg_improvement:.1f}%")
    
    with col2:
        total_datasets = df_llm_all['dataset'].nunique()
        st.metric("📋 Datasets", total_datasets)
    
    with col3:
        avg_llm_acc = combined['mean_llm'].mean()
        st.metric("🤖 LLM Avg", f"{avg_llm_acc:.1f}%")
    
    with col4:
        avg_rule_acc = combined['mean_rule'].mean()
        st.metric("📊 Rule Avg", f"{avg_rule_acc:.1f}%")
    
    st.markdown("---")
    
    # Accuracy comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Accuracy by Framework")
        
        # Prepare data for grouped bar chart
        rule_means = df_rule_all.groupby('framework')['accuracy'].mean().reset_index()
        rule_means['Evaluation'] = 'Rule-based'
        llm_means = df_llm_all.groupby('framework')['accuracy'].mean().reset_index()
        llm_means['Evaluation'] = 'LLM Judge'
        
        combined_chart_data = pd.concat([rule_means, llm_means])
        
        fig = px.bar(
            combined_chart_data,
            x='framework',
            y='accuracy',
            color='Evaluation',
            barmode='group',
            title='Mean Accuracy: Rule-based vs LLM Judge',
            labels={'accuracy': 'Accuracy (%)', 'framework': 'Framework'},
            color_discrete_map={'Rule-based': '#636EFA', 'LLM Judge': '#00CC96'}
        )
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.subheader("🔺 Improvement by Framework")
        
        # Calculate improvement for each framework
        improvement_data = combined[['framework', 'Improvement']].copy()
        
        fig = px.bar(
            improvement_data,
            x='framework',
            y='Improvement',
            title='LLM Judge Improvement over Rule-based',
            labels={'Improvement': 'Improvement (%)', 'framework': 'Framework'},
            color='Improvement',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")
    
    # Dataset performance
    st.markdown("---")
    st.subheader("📚 Performance by Dataset")
    
    # Prepare data with both evaluations
    rule_dataset = df_rule_all.groupby(['dataset', 'framework'])['accuracy'].mean().reset_index()
    rule_dataset['Evaluation'] = 'Rule-based'
    llm_dataset = df_llm_all.groupby(['dataset', 'framework'])['accuracy'].mean().reset_index()
    llm_dataset['Evaluation'] = 'LLM Judge'
    
    dataset_combined = pd.concat([rule_dataset, llm_dataset])
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Grouped by Framework", "📈 Grouped by Dataset"])
    
    with tab1:
        fig = px.bar(
            dataset_combined,
            x='dataset',
            y='accuracy',
            color='framework',
            facet_col='Evaluation',
            barmode='group',
            title='Accuracy by Dataset and Framework',
            labels={'accuracy': 'Accuracy (%)', 'dataset': 'Dataset'},
            height=400
        )
        st.plotly_chart(fig, width="stretch")
    
    with tab2:
        fig = px.bar(
            dataset_combined,
            x='framework',
            y='accuracy',
            color='Evaluation',
            facet_col='dataset',
            facet_col_wrap=3,
            barmode='group',
            title='Accuracy Comparison by Dataset',
            labels={'accuracy': 'Accuracy (%)', 'framework': 'Framework'},
            color_discrete_map={'Rule-based': '#636EFA', 'LLM Judge': '#00CC96'},
            height=600
        )
        st.plotly_chart(fig, width="stretch")


def show_detailed_results(all_files: List[str], selected_dataset: str, selected_framework: str):
    """Display detailed question-by-question results with both evaluation methods."""
    st.header("🔍 Detailed Results")
    
    # Filter files by dataset if specified
    if selected_dataset != 'All':
        filtered_files = [f for f in all_files if selected_dataset in os.path.basename(f)]
    else:
        filtered_files = all_files
    
    if not filtered_files:
        st.warning("No results found for the selected filters.")
        return
    
    # File selector
    file_options = {parse_result_filename(f)['date'] + " - " + parse_result_filename(f)['dataset']: f 
                   for f in filtered_files}
    
    selected_file_label = st.selectbox("Select a benchmark run:", list(file_options.keys()))
    selected_file = file_options[selected_file_label]
    
    # Load result
    result = load_results_from_file(selected_file)
    
    # Display metadata
    file_info = parse_result_filename(selected_file)
    st.info(f"**Dataset:** {file_info['dataset']} | **Date:** {file_info['date']}")
    
    # Download buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        # Download full results JSON
        result_json = json.dumps(result, indent=2)
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=result_json,
            file_name=f"{file_info['dataset']}_results_{file_info['timestamp']}.json",
            mime="application/json",
            help="Download complete benchmark results with all logs"
        )
    
    with col2:
        # Download dataset (if available in results)
        dataset_csv = None
        
        # Check for dataset in new format
        if isinstance(result, dict):
            dataset_csv = result.get('dataset_csv')
            if not dataset_csv and 'metadata' in result:
                # Might be nested
                dataset_csv = result.get('dataset_csv')
        
        if dataset_csv:
            st.download_button(
                label="📊 Download Dataset (CSV)",
                data=dataset_csv,
                file_name=f"{file_info['dataset']}_dataset.csv",
                mime="text/csv",
                help="Download the original dataset used in this benchmark"
            )
        else:
            st.button("📊 Dataset Not Available", disabled=True, help="Run benchmark with --save-results to include dataset")
    
    with col3:
        st.caption("Download complete results or dataset for offline analysis")
    
    st.markdown("---")
    
    # Summary metrics
    st.subheader("Summary Statistics")
    
    # Handle both old (list) and new (dict) formats
    if isinstance(result, list):
        # Old format - calculate summary
        questions = result
        framework_stats = {}
    elif isinstance(result, dict) and 'results' in result:
        # New format with metadata
        questions = result['results']
        framework_stats = {}
        
        # Calculate both rule-based and LLM Judge stats
        for question in questions:
            for fw_name, fw_result in question.get('framework_results', {}).items():
                if fw_name not in framework_stats:
                    framework_stats[fw_name] = {
                        'rule_correct': 0,
                        'llm_correct': 0,
                        'total': 0
                    }
                
                framework_stats[fw_name]['total'] += 1
                
                if not fw_result.get('error'):
                    comparison = fw_result.get('comparison', {})
                    
                    # Get rule-based result
                    if comparison.get('rule_based_match'):
                        framework_stats[fw_name]['rule_correct'] += 1
                    
                    # Get LLM Judge result
                    if comparison.get('llm_judge_match'):
                        framework_stats[fw_name]['llm_correct'] += 1
        
        # Display stats - both evaluations side by side
        if framework_stats:
            cols = st.columns(len(framework_stats))
            for idx, (fw_name, stats) in enumerate(framework_stats.items()):
                with cols[idx]:
                    total = stats['total']
                    rule_acc = (stats['rule_correct'] / total * 100) if total > 0 else 0
                    llm_acc = (stats['llm_correct'] / total * 100) if total > 0 else 0
                    
                    st.markdown(f"**{fw_name}**")
                    st.markdown(f"📊 **Rule-based:** {rule_acc:.1f}% ({stats['rule_correct']}/{total})")
                    st.markdown(f"🤖 **LLM Judge:** {llm_acc:.1f}% ({stats['llm_correct']}/{total})")
                    
                    # Show improvement
                    if llm_acc > rule_acc:
                        improvement = llm_acc - rule_acc
                        st.success(f"⬆️ +{improvement:.1f}% improvement")
                    elif llm_acc < rule_acc:
                        decline = rule_acc - llm_acc
                        st.error(f"⬇️ -{decline:.1f}% decline")
                    else:
                        st.info("➡️ Same result")
    else:
        # New format - use existing summary
        summary = result.get('summary', {})
        
        if summary:
            cols = st.columns(len([k for k in summary.keys() if k != 'total_questions']))
            
            for idx, (framework, stats) in enumerate(summary.items()):
                if framework != 'total_questions':
                    with cols[idx]:
                        accuracy = stats.get('accuracy', 0)
                        correct = stats.get('correct', 0)
                        total = stats.get('total', 0)
                        
                        st.metric(
                            framework,
                            f"{accuracy:.1f}%",
                            f"{correct}/{total} correct"
                        )
        
        questions = result.get('questions', [])
    
    st.markdown("---")
    
    # Question selector
    if questions:
        st.subheader(f"Questions ({len(questions)} total)")
        
        question_idx = st.selectbox(
            "Select a question to analyze:",
            range(len(questions)),
            format_func=lambda x: f"Q{x+1}: {questions[x].get('question', 'Unknown')[:80]}..."
        )
        
        display_question_details(result, question_idx)


def show_framework_comparison(df_rule: pd.DataFrame, df_llm: pd.DataFrame):
    """Display detailed framework comparison with both evaluation methods.
    
    Args:
        df_rule: Rule-based evaluation results
        df_llm: LLM Judge evaluation results
    """
    st.header("📊 Framework Comparison")
    
    if df_rule.empty or df_llm.empty:
        st.warning("No data available for comparison.")
        return
    
    # Overall comparison table with both evaluations
    st.subheader("⚖️ Overall Performance Comparison")
    st.caption("📊 Rule-based vs 🤖 LLM Judge evaluation")
    
    # Get stats for both methods
    rule_comp = df_rule.groupby('framework').agg({
        'accuracy': ['mean', 'std'],
        'correct': 'sum',
        'total': 'sum',
        'errors': 'sum'
    }).round(2)
    
    llm_comp = df_llm.groupby('framework').agg({
        'accuracy': ['mean', 'std'],
        'correct': 'sum',
        'total': 'sum',
        'errors': 'sum'
    }).round(2)
    
    # Create combined display
    combined_display = pd.DataFrame({
        'Framework': rule_comp.index,
        '📊 Rule Accuracy': rule_comp[('accuracy', 'mean')].values,
        '📊 Rule Std': rule_comp[('accuracy', 'std')].values,
        '🤖 LLM Accuracy': llm_comp[('accuracy', 'mean')].values,
        '🤖 LLM Std': llm_comp[('accuracy', 'std')].values,
        '🔺 Improvement': (llm_comp[('accuracy', 'mean')].values - rule_comp[('accuracy', 'mean')].values).round(2),
        'Total Questions': rule_comp[('total', 'sum')].values,
        'Errors': rule_comp[('errors', 'sum')].values
    })
    
    st.dataframe(combined_display.sort_values('🤖 LLM Accuracy', ascending=False), hide_index=True, width="stretch")
    
    st.markdown("---")
    
    # Side-by-side radar charts
    st.subheader("🕸️ Performance Radar Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("📊 Rule-based Evaluation")
        
        rule_metrics = df_rule.groupby('framework').agg({
            'accuracy': 'mean',
            'correct': lambda x: (x / df_rule.loc[x.index, 'total']).mean() * 100,
            'errors': lambda x: 100 - (x.sum() / len(x) * 10)
        }).reset_index()
        
        fig_rule = go.Figure()
        
        for framework in rule_metrics['framework'].unique():
            fw_data = rule_metrics[rule_metrics['framework'] == framework]
            
            fig_rule.add_trace(go.Scatterpolar(
                r=[fw_data['accuracy'].values[0], 
                   fw_data['correct'].values[0], 
                   fw_data['errors'].values[0]],
                theta=['Accuracy', 'Correctness', 'Reliability'],
                fill='toself',
                name=framework
            ))
        
        fig_rule.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_rule, width="stretch")
    
    with col2:
        st.caption("🤖 LLM Judge Evaluation")
        
        llm_metrics = df_llm.groupby('framework').agg({
            'accuracy': 'mean',
            'correct': lambda x: (x / df_llm.loc[x.index, 'total']).mean() * 100,
            'errors': lambda x: 100 - (x.sum() / len(x) * 10)
        }).reset_index()
        
        fig_llm = go.Figure()
        
        for framework in llm_metrics['framework'].unique():
            fw_data = llm_metrics[llm_metrics['framework'] == framework]
            
            fig_llm.add_trace(go.Scatterpolar(
                r=[fw_data['accuracy'].values[0], 
                   fw_data['correct'].values[0], 
                   fw_data['errors'].values[0]],
                theta=['Accuracy', 'Correctness', 'Reliability'],
                fill='toself',
                name=framework
            ))
        
        fig_llm.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_llm, width="stretch")
    
    st.markdown("---")
    
    # Win rate comparison
    st.subheader("🏆 Head-to-Head Win Rate")
    st.caption("Comparing best framework per dataset between evaluation methods")
    
    # Calculate wins per question for both methods
    datasets = df_llm['dataset'].unique()
    
    rule_wins = {fw: 0 for fw in df_rule['framework'].unique()}
    llm_wins = {fw: 0 for fw in df_llm['framework'].unique()}
    
    for dataset in datasets:
        # Rule-based wins
        rule_dataset_runs = df_rule[df_rule['dataset'] == dataset]
        if not rule_dataset_runs.empty:
            best_fw_rule = rule_dataset_runs.loc[rule_dataset_runs['accuracy'].idxmax(), 'framework']
            rule_wins[best_fw_rule] += 1
        
        # LLM Judge wins
        llm_dataset_runs = df_llm[df_llm['dataset'] == dataset]
        if not llm_dataset_runs.empty:
            best_fw_llm = llm_dataset_runs.loc[llm_dataset_runs['accuracy'].idxmax(), 'framework']
            llm_wins[best_fw_llm] += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("📊 Rule-based Wins")
        rule_win_df = pd.DataFrame({
            'Framework': list(rule_wins.keys()),
            'Wins': list(rule_wins.values())
        })
        
        fig_rule = px.pie(
            rule_win_df,
            values='Wins',
            names='Framework',
            hole=0.3
        )
        st.plotly_chart(fig_rule, width="stretch")
    
    with col2:
        st.caption("🤖 LLM Judge Wins")
        llm_win_df = pd.DataFrame({
            'Framework': list(llm_wins.keys()),
            'Wins': list(llm_wins.values())
        })
        
        fig_llm = px.pie(
            llm_win_df,
            values='Wins',
            names='Framework',
            hole=0.3
        )
        st.plotly_chart(fig_llm, width="stretch", key="llm_wins_pie")


def show_historical_trends(df_rule: pd.DataFrame, df_llm: pd.DataFrame):
    """Display accuracy trends over time for both evaluation methods.
    
    Args:
        df_rule: Rule-based evaluation results
        df_llm: LLM Judge evaluation results
    """
    st.header("⏱️ Historical Trends")
    
    if df_rule.empty or df_llm.empty:
        st.warning("No historical data available.")
        return
    
    # Convert timestamp to datetime for better plotting
    df_rule['datetime'] = pd.to_datetime(df_rule['timestamp'], format='%Y%m%d_%H%M%S', errors='coerce')
    df_rule = df_rule.sort_values('datetime')
    df_llm['datetime'] = pd.to_datetime(df_llm['timestamp'], format='%Y%m%d_%H%M%S', errors='coerce')
    df_llm = df_llm.sort_values('datetime')
    
    # Accuracy over time - comparison
    st.subheader("📈 Accuracy Trends Comparison")
    
    # Prepare combined data
    df_rule_plot = df_rule.copy()
    df_rule_plot['Evaluation'] = 'Rule-based'
    df_llm_plot = df_llm.copy()
    df_llm_plot['Evaluation'] = 'LLM Judge'
    
    df_combined = pd.concat([df_rule_plot, df_llm_plot])
    
    fig = px.line(
        df_combined,
        x='datetime',
        y='accuracy',
        color='framework',
        line_dash='Evaluation',
        hover_data=['dataset', 'Evaluation'],
        title='Framework Accuracy Over Time - Both Evaluations',
        labels={'datetime': 'Date', 'accuracy': 'Accuracy (%)'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, width="stretch", key="trends_combined_line")
    
    st.markdown("---")
    
    # Dataset-specific trends
    st.subheader("📊 Dataset-Specific Trends")
    
    selected_dataset = st.selectbox(
        "Select dataset for trend analysis:",
        df_llm['dataset'].unique()
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("📊 Rule-based")
        dataset_df_rule = df_rule[df_rule['dataset'] == selected_dataset]
        
        fig_rule = px.scatter(
            dataset_df_rule,
            x='datetime',
            y='accuracy',
            color='framework',
            size='total',
            hover_data=['correct', 'errors'],
            labels={'datetime': 'Date', 'accuracy': 'Accuracy (%)'}
        )
        st.plotly_chart(fig_rule, width="stretch", key="trends_dataset_rule_scatter")
    
    with col2:
        st.caption("🤖 LLM Judge")
        dataset_df_llm = df_llm[df_llm['dataset'] == selected_dataset]
        
        fig_llm = px.scatter(
            dataset_df_llm,
            x='datetime',
            y='accuracy',
            color='framework',
            size='total',
            hover_data=['correct', 'errors'],
            labels={'datetime': 'Date', 'accuracy': 'Accuracy (%)'}
        )
        st.plotly_chart(fig_llm, width="stretch", key="trends_dataset_llm_scatter")
    
    st.markdown("---")
    
    # Moving average comparison
    st.subheader("📊 7-Run Moving Average")
    
    # Calculate moving averages for both
    ma_rule_data = []
    for framework in df_rule['framework'].unique():
        fw_df = df_rule[df_rule['framework'] == framework].sort_values('datetime')
        fw_df['ma_accuracy'] = fw_df['accuracy'].rolling(window=min(7, len(fw_df)), min_periods=1).mean()
        fw_df['Evaluation'] = 'Rule-based'
        ma_rule_data.append(fw_df)
    
    ma_llm_data = []
    for framework in df_llm['framework'].unique():
        fw_df = df_llm[df_llm['framework'] == framework].sort_values('datetime')
        fw_df['ma_accuracy'] = fw_df['accuracy'].rolling(window=min(7, len(fw_df)), min_periods=1).mean()
        fw_df['Evaluation'] = 'LLM Judge'
        ma_llm_data.append(fw_df)
    
    ma_combined = pd.concat(ma_rule_data + ma_llm_data)
    
    fig = px.line(
        ma_combined,
        x='datetime',
        y='ma_accuracy',
        color='framework',
        line_dash='Evaluation',
        title='7-Run Moving Average - Both Evaluations',
        labels={'datetime': 'Date', 'ma_accuracy': 'Moving Avg Accuracy (%)'}
    )
    st.plotly_chart(fig, width="stretch", key="trends_moving_avg_line")


def show_raw_data(df_rule: pd.DataFrame, df_llm: pd.DataFrame):
    """Display raw data tables for both evaluation methods.
    
    Args:
        df_rule: Rule-based evaluation results
        df_llm: LLM Judge evaluation results
    """
    st.header("🗂️ Raw Data")
    
    if df_rule.empty or df_llm.empty:
        st.warning("No data available.")
        return
    
    # Export options
    st.subheader("📥 Export Options")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        csv_rule = df_rule.to_csv(index=False)
        st.download_button(
            label="📊 Rule CSV",
            data=csv_rule,
            file_name="benchmark_results_rule.csv",
            mime="text/csv"
        )
    
    with col2:
        csv_llm = df_llm.to_csv(index=False)
        st.download_button(
            label="🤖 LLM CSV",
            data=csv_llm,
            file_name="benchmark_results_llm.csv",
            mime="text/csv"
        )
    
    with col3:
        json_rule = df_rule.to_json(orient='records', indent=2)
        st.download_button(
            label="📊 Rule JSON",
            data=json_rule,
            file_name="benchmark_results_rule.json",
            mime="application/json"
        )
    
    with col4:
        json_llm = df_llm.to_json(orient='records', indent=2)
        st.download_button(
            label="🤖 LLM JSON",
            data=json_llm,
            file_name="benchmark_results_llm.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # Tabbed view for both datasets
    tab1, tab2, tab3 = st.tabs(["📊 Rule-based Data", "🤖 LLM Judge Data", "⚖️ Comparison"])
    
    with tab1:
        st.subheader("Rule-based Evaluation Data")
        
        columns_to_show = st.multiselect(
            "Select columns to display:",
            df_rule.columns.tolist(),
            default=['dataset', 'framework', 'accuracy', 'correct', 'total', 'date'],
            key='rule_columns'
        )
        
        if columns_to_show:
            st.dataframe(
                df_rule[columns_to_show].sort_values(['dataset', 'framework']),
                width="stretch",
                hide_index=True
            )
        
        st.subheader("Statistics")
        st.write(df_rule.describe())
    
    with tab2:
        st.subheader("LLM Judge Evaluation Data")
        
        columns_to_show = st.multiselect(
            "Select columns to display:",
            df_llm.columns.tolist(),
            default=['dataset', 'framework', 'accuracy', 'correct', 'total', 'date'],
            key='llm_columns'
        )
        
        if columns_to_show:
            st.dataframe(
                df_llm[columns_to_show].sort_values(['dataset', 'framework']),
                width="stretch",
                hide_index=True
            )
        
        st.subheader("Statistics")
        st.write(df_llm.describe())
    
    with tab3:
        st.subheader("Side-by-Side Comparison")
        
        # Merge key columns from both
        comparison_df = df_rule[['dataset', 'framework', 'accuracy', 'correct', 'total']].copy()
        comparison_df.columns = ['Dataset', 'Framework', 'Rule Accuracy', 'Rule Correct', 'Total']
        
        llm_subset = df_llm[['dataset', 'framework', 'accuracy', 'correct']].copy()
        llm_subset.columns = ['Dataset', 'Framework', 'LLM Accuracy', 'LLM Correct']
        
        merged = comparison_df.merge(llm_subset, on=['Dataset', 'Framework'])
        merged['Improvement'] = merged['LLM Accuracy'] - merged['Rule Accuracy']
        
        st.dataframe(
            merged.sort_values(['Dataset', 'Framework']),
            width="stretch",
            hide_index=True
        )


if __name__ == "__main__":
    main()
