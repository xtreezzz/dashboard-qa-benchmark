#!/usr/bin/env python3
"""
List all available benchmark datasets with details.
"""
import sys
sys.path.insert(0, 'src')

from benchmark_datasets import AVAILABLE_DATASETS
from tabulate import tabulate


def main():
    print("\n" + "="*80)
    print("AVAILABLE BENCHMARK DATASETS")
    print("="*80 + "\n")
    
    # Categories
    sklearn_datasets = ['iris', 'wine', 'diabetes', 'sales']
    synthetic_datasets = ['ecommerce', 'employees']
    external_datasets = ['titanic', 'happiness', 'supermarket', 'covid', 'stackoverflow']
    
    def print_category(category_name, dataset_list):
        print(f"\n{category_name}")
        print("-" * 80)
        
        table_data = []
        for name in dataset_list:
            if name in AVAILABLE_DATASETS:
                # Load dataset to get details
                benchmark = AVAILABLE_DATASETS[name]()
                df = benchmark.get_dataset()
                qa_pairs = benchmark.get_qa_pairs()
                
                table_data.append([
                    name,
                    benchmark.name,
                    len(df),
                    len(df.columns),
                    len(qa_pairs)
                ])
        
        print(tabulate(
            table_data,
            headers=['Dataset ID', 'Name', 'Rows', 'Columns', 'Questions'],
            tablefmt='grid'
        ))
    
    print_category("📊 Built-in Datasets (sklearn)", sklearn_datasets)
    print_category("🔧 Synthetic Datasets", synthetic_datasets)
    print_category("🌐 External Datasets (Popular Benchmarks)", external_datasets)
    
    print("\n" + "="*80)
    print(f"Total: {len(AVAILABLE_DATASETS)} datasets")
    print("="*80)
    
    print("\n💡 Usage Examples:")
    print("  python3 main.py --dataset iris")
    print("  python3 main.py --dataset titanic --save-results")
    print("  ./benchmark_external.sh  # Run all external datasets")
    
    print("\n📚 Documentation:")
    print("  EXTERNAL_DATASETS.md - Details on external datasets")
    print("  SYNTHETIC_DATASETS.md - Details on synthetic datasets")
    print("  README.md - General usage guide")
    print()


if __name__ == "__main__":
    main()
