***ClickHouse vs MySQL Performance Benchmark***
A performance benchmarking dashboard that compares ClickHouse (columnar analytical database) against MySQL (traditional row-based RDBMS) on large-scale datasets. Demonstrates the performance advantages of columnar storage for analytical workloads.

*Features*
Generates synthetic web log data (10+ million records)
Automated benchmark execution across both databases
Performance comparison for analytical queries (COUNT, GROUP BY, aggregations)
Visual results with speedup analysis

Containerized setup using Docker

*Installation*
*Prerequisites*
Docker and Docker Compose

Python 3.8+

Setup
bash
# Clone the repository
git clone https://github.com/kalashnikov42/clickhouse-benchmark.git
cd clickhouse-benchmark

# Install dependencies
pip install -r requirements.txt

# Generate test data
python data_generator.py

# Start databases
python benchmark_setup.py

# Setup tables and load data
python setup_tables.py

# Run benchmarks
python query_runner.py

# Analyze results
python results_analyzer.py

*Results*
ClickHouse demonstrates 10-100x faster performance on analytical queries:
Query Type	ClickHouse	MySQL	Speedup
COUNT(*)	0.12s	4.56s	38x
GROUP BY status	0.08s	7.23s	90x
AVG response time	0.15s	3.89s	26x

*Project Structure*
data_generator.py - Synthetic data generation

benchmark_setup.py - Docker container management

setup_tables.py - Database schema setup

query_runner.py - Benchmark execution

results_analyzer.py - Performance analysis and visualization

*Technologies Used*
ClickHouse, MySQL
Python, Docker
Pandas, Matplotlib, Seaborn


