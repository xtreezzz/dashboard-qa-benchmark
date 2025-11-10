#!/usr/bin/env python3
"""
View logs from benchmark results.

Usage:
    python view_logs.py results/iris_results_20251108_214147.json
    python view_logs.py results/sales_results_20251108_214522.json --question 0
    python view_logs.py results/iris_results_20251108_214147.json --framework PandasAI
"""
import json
import argparse
import sys


def print_separator(title="", char="="):
    """Print a separator line."""
    if title:
        print(f"\n{char*10} {title} {char*10}")
    else:
        print(char*80)


def view_logs(filepath, question_idx=None, framework_name=None):
    """View logs from benchmark results."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {filepath}")
        return
    
    print(f"\n📊 Benchmark Results: {filepath}")
    print(f"Total Questions: {len(data)}")
    
    # Filter questions if specified
    questions_to_show = [question_idx] if question_idx is not None else range(len(data))
    
    for idx in questions_to_show:
        if idx >= len(data):
            print(f"\nError: Question index {idx} out of range (max: {len(data)-1})")
            continue
            
        q_data = data[idx]
        
        print_separator(f"Question {idx+1}/{len(data)}")
        print(f"\n❓ {q_data['question']}")
        print(f"✅ Benchmark Answer: {q_data['benchmark']['answer']}")
        print(f"   Reasoning: {q_data['benchmark']['reasoning']}")
        
        # Show framework results
        frameworks = [framework_name] if framework_name else q_data['framework_results'].keys()
        
        for fw_name in frameworks:
            if fw_name not in q_data['framework_results']:
                print(f"\nError: Framework '{fw_name}' not found")
                continue
                
            fw_result = q_data['framework_results'][fw_name]
            
            print_separator(fw_name, char="-")
            
            # Show answer
            if fw_result.get('error'):
                print(f"❌ Error: {fw_result['error']}")
            else:
                answer = fw_result['answer']
                print(f"💡 Answer: {answer}")
                print(f"📝 Reasoning: {fw_result['reasoning']}")
            
            # Show logs
            logs = fw_result.get('logs', '')
            if logs:
                print(f"\n📋 Execution Logs:")
                print("-" * 80)
                print(logs)
                print("-" * 80)
            else:
                print("\n📋 No logs available")
    
    print_separator()


def main():
    parser = argparse.ArgumentParser(
        description="View logs from benchmark results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View all questions
  python view_logs.py results/iris_results_20251108_214147.json
  
  # View specific question
  python view_logs.py results/sales_results_20251108_214522.json --question 0
  
  # View specific framework
  python view_logs.py results/iris_results_20251108_214147.json --framework LangChain
  
  # View specific question and framework
  python view_logs.py results/sales_results_20251108_214522.json -q 1 -f PandasAI
        """
    )
    
    parser.add_argument('filepath', help='Path to JSON results file')
    parser.add_argument('-q', '--question', type=int, help='Question index to view (0-based)')
    parser.add_argument('-f', '--framework', choices=['PandasAI', 'Sketch', 'LangChain'],
                       help='Framework to view logs for')
    
    args = parser.parse_args()
    
    view_logs(args.filepath, args.question, args.framework)


if __name__ == "__main__":
    main()
