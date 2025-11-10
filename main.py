#!/usr/bin/env python3
"""
Main script for benchmarking DataFrame Q&A frameworks.

Usage:
    python main.py --dataset iris --api-key YOUR_API_KEY
    python main.py --dataset sales --save-results
    python main.py --list-datasets
"""
import argparse
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from benchmark_datasets import get_benchmark_dataset, AVAILABLE_DATASETS
from framework_integrations import FrameworkManager
from evaluation import ResultFormatter


def main():
    # Load environment variables
    load_dotenv()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Benchmark DataFrame Q&A frameworks")
    parser.add_argument('--dataset', type=str, help=f"Dataset name: {list(AVAILABLE_DATASETS.keys())}")
    parser.add_argument('--api-key', type=str, help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument('--save-results', action='store_true', help="Save results to JSON file")
    parser.add_argument('--list-datasets', action='store_true', help="List available datasets")
    parser.add_argument('--output-dir', type=str, default='results', help="Output directory for results")
    
    args = parser.parse_args()
    
    # List datasets if requested
    if args.list_datasets:
        print("\nAvailable datasets:")
        for name in AVAILABLE_DATASETS.keys():
            print(f"  - {name}")
        return
    
    # Check if dataset is provided
    if not args.dataset:
        print("Error: --dataset is required (or use --list-datasets to see available datasets)")
        parser.print_help()
        return
    
    # Set API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\nWarning: No OpenAI API key provided. Set OPENAI_API_KEY environment variable or use --api-key")
        print("Frameworks will not work without an API key.\n")
    
    # Load dataset
    print(f"\n{'='*100}")
    print(f"Loading dataset: {args.dataset}")
    print(f"{'='*100}")
    
    try:
        benchmark_data = get_benchmark_dataset(args.dataset)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    df = benchmark_data.get_dataset()
    qa_pairs = benchmark_data.get_qa_pairs()
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Number of questions: {len(qa_pairs)}")
    print("\nDataset preview:")
    print(df.head())
    
    # Initialize frameworks
    print(f"\n{'='*100}")
    print("Initializing frameworks...")
    print(f"{'='*100}")
    
    manager = FrameworkManager(api_key)
    
    # Check availability
    availability = manager.get_availability_status()
    print("\nFramework availability:")
    for name, available in availability.items():
        status = "✓ Available" if available else "✗ Not available"
        print(f"  {name}: {status}")
    
    # Run benchmarks
    print(f"\n{'='*100}")
    print("Running benchmarks...")
    print(f"{'='*100}\n")
    
    all_results = []
    
    for idx, qa_pair in enumerate(qa_pairs, 1):
        question = qa_pair["question"]
        
        print(f"\nQuestion {idx}/{len(qa_pairs)}: {question}")
        print("-" * 80)
        
        # Query all frameworks
        framework_results = manager.query_all(df, question)
        
        # Store results
        result = {
            "question": question,
            "benchmark": qa_pair,
            "framework_results": framework_results
        }
        all_results.append(result)
        
        # Display comparison
        comparison_table = ResultFormatter.format_comparison_table(
            question, qa_pair, framework_results
        )
        print(comparison_table)
    
    # Display summary
    summary = ResultFormatter.format_summary(all_results)
    print(summary)
    
    # Save results if requested
    if args.save_results:
        ResultFormatter.save_results(all_results, args.dataset, args.output_dir, df)
    
    print("\nBenchmark complete!")


if __name__ == "__main__":
    main()
