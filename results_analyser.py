import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

class ResultsAnalyzer:
    def __init__(self, results_file='benchmark_results.csv'):
        self.results = pd.read_csv(results_file)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_summary_report(self):
        """Generate a comprehensive performance summary"""
        print("=" * 60)
        print("CLICKHOUSE vs MYSQL PERFORMANCE BENCHMARK REPORT")
        print("=" * 60)
        
        avg_speedup = self.results['speedup'].mean()
        max_speedup = self.results['speedup'].max()
        min_speedup = self.results['speedup'].min()
        
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print(f"   Average Speedup: {avg_speedup:.1f}x")
        print(f"   Maximum Speedup: {max_speedup:.1f}x")
        print(f"   Minimum Speedup: {min_speedup:.1f}x")
        
        # Find best and worst performing queries
        best_query = self.results.loc[self.results['speedup'].idxmax()]
        worst_query = self.results.loc[self.results['speedup'].idxmin()]
        
        print(f"\n🚀 BEST PERFORMING QUERY: {best_query['query']}")
        print(f"   ClickHouse: {best_query['clickhouse_time']:.3f}s")
        print(f"   MySQL: {best_query['mysql_time']:.3f}s")
        print(f"   Speedup: {best_query['speedup']:.1f}x")
        
        print(f"\n🐌 SLOWEST PERFORMING QUERY: {worst_query['query']}")
        print(f"   ClickHouse: {worst_query['clickhouse_time']:.3f}s")
        print(f"   MySQL: {worst_query['mysql_time']:.3f}s")
        print(f"   Speedup: {worst_query['speedup']:.1f}x")
        
        return {
            'timestamp': self.timestamp,
            'average_speedup': avg_speedup,
            'max_speedup': max_speedup,
            'min_speedup': min_speedup,
            'best_query': best_query['query'],
            'worst_query': worst_query['query'],
            'total_queries': len(self.results)
        }
    
    def create_performance_chart(self):
        """Create visualization of benchmark results"""
        plt.figure(figsize=(12, 8))
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['font.size'] = 12
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Query execution time comparison
        queries = self.results['query']
        ch_times = self.results['clickhouse_time']
        mysql_times = self.results['mysql_time']
        
        x = range(len(queries))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], ch_times, width, label='ClickHouse', color='#FF6B00', alpha=0.8)
        ax1.bar([i + width/2 for i in x], mysql_times, width, label='MySQL', color='#007ACC', alpha=0.8)
        
        ax1.set_xlabel('Queries')
        ax1.set_ylabel('Execution Time (seconds)')
        ax1.set_title('Query Execution Time: ClickHouse vs MySQL')
        ax1.set_xticks(x)
        ax1.set_xticklabels(queries, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, (ch, mysql) in enumerate(zip(ch_times, mysql_times)):
            ax1.text(i - width/2, ch + 0.01, f'{ch:.2f}s', ha='center', va='bottom', fontsize=9)
            ax1.text(i + width/2, mysql + 0.01, f'{mysql:.2f}s', ha='center', va='bottom', fontsize=9)
        
        # Plot 2: Speedup factor
        speedups = self.results['speedup']
        colors = ['green' if x > 1 else 'red' for x in speedups]
        
        bars = ax2.bar(queries, speedups, color=colors, alpha=0.7)
        ax2.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Break-even (1x)')
        ax2.set_xlabel('Queries')
        ax2.set_ylabel('Speedup Factor (MySQL Time / ClickHouse Time)')
        ax2.set_title('Performance Speedup: ClickHouse vs MySQL')
        ax2.set_xticklabels(queries, rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on speedup bars
        for bar, speedup in zip(bars, speedups):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{speedup:.1f}x', ha='center', va='bottom', fontsize=10,
                    fontweight='bold' if speedup > 5 else 'normal')
        
        plt.tight_layout()
        plt.savefig(f'benchmark_results_{self.timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_detailed_breakdown(self):
        """Generate detailed analysis for each query type"""
        print("\n" + "=" * 50)
        print("DETAILED QUERY BREAKDOWN")
        print("=" * 50)
        
        for _, row in self.results.iterrows():
            print(f"\n📋 Query: {row['query']}")
            print(f"   ⏱️  ClickHouse: {row['clickhouse_time']:.3f} seconds")
            print(f"   ⏱️  MySQL: {row['mysql_time']:.3f} seconds")
            print(f"   🚀 Speedup: {row['speedup']:.1f}x faster")
            
            # Performance interpretation
            if row['speedup'] > 10:
                print("   💡 INSIGHT: Excellent for analytical workloads")
            elif row['speedup'] > 5:
                print("   💡 INSIGHT: Very good performance gain")
            elif row['speedup'] > 2:
                print("   💡 INSIGHT: Moderate improvement")
            else:
                print("   💡 INSIGHT: Minimal advantage for this query type")
    
    def generate_technical_insights(self):
        """Provide technical insights about the results"""
        print("\n" + "=" * 50)
        print("TECHNICAL INSIGHTS")
        print("=" + 50)
        
        # Analyze which query types benefit most
        aggregation_queries = self.results[self.results['query'].str.contains('count|avg|sum', case=False)]
        grouping_queries = self.results[self.results['query'].str.contains('group|top', case=False)]
        
        if len(aggregation_queries) > 0:
            avg_agg_speedup = aggregation_queries['speedup'].mean()
            print(f"\n📈 Aggregation Queries (COUNT, AVG, SUM):")
            print(f"   Average speedup: {avg_agg_speedup:.1f}x")
            print("   Why: ClickHouse's columnar storage excels at scanning and aggregating large datasets")
        
        if len(grouping_queries) > 0:
            avg_group_speedup = grouping_queries['speedup'].mean()
            print(f"\n🔍 GROUP BY Queries:")
            print(f"   Average speedup: {avg_group_speedup:.1f}x")
            print("   Why: ClickHouse's vectorized execution handles grouping operations efficiently")
        
        # General insights
        print(f"\n🎯 KEY TAKEAWAYS:")
        print("   • ClickHouse dominates analytical workloads with large datasets")
        print("   • Best for: aggregations, filtering, time-series analysis")
        print("   • Consider: MySQL may still be better for transactional workloads")
        print("   • Optimal use case: Real-time analytics on large datasets")
    
    def save_comprehensive_report(self, summary):
        """Save all results to files"""
        # Save JSON report
        report_data = {
            'summary': summary,
            'detailed_results': self.results.to_dict('records'),
            'benchmark_metadata': {
                'dataset_size': '10+ million rows',
                'query_types': list(self.results['query']),
                'test_date': self.timestamp
            }
        }
        
        with open(f'benchmark_report_{self.timestamp}.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Save formatted CSV
        self.results.to_csv(f'detailed_results_{self.timestamp}.csv', index=False)
        
        print(f"\n💾 Reports saved:")
        print(f"   📄 benchmark_report_{self.timestamp}.json")
        print(f"   📊 detailed_results_{self.timestamp}.csv")
        print(f"   🖼️  benchmark_results_{self.timestamp}.png")

def main():
    """Main execution function"""
    try:
        analyzer = ResultsAnalyzer()
        
        print("🔍 Analyzing benchmark results...")
        
        # Generate all reports
        summary = analyzer.generate_summary_report()
        analyzer.generate_detailed_breakdown()
        analyzer.generate_technical_insights()
        
        # Create visualizations
        print("\n📊 Generating charts...")
        analyzer.create_performance_chart()
        
        # Save comprehensive report
        analyzer.save_comprehensive_report(summary)
        
        print("\n✅ Analysis completed successfully!")
        
    except FileNotFoundError:
        print("❌ Error: benchmark_results.csv not found.")
        print("   Please run query_runner.py first to generate benchmark data.")
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()