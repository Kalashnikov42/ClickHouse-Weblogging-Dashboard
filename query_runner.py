import time
import clickhouse_connect
import mysql.connector
import pandas as pd

class Benchmark:
    def __init__(self):
        self.ch_client = clickhouse_connect.get_client(
            host='localhost', port=8123
        )
        self.mysql_conn = mysql.connector.connect(
            host='localhost', user='root', password='password', database='benchmark'
        )
    
    def run_clickhouse_query(self, query):
        start = time.time()
        result = self.ch_client.query(query)
        end = time.time()
        return end - start, result.row_count
    
    def run_mysql_query(self, query):
        start = time.time()
        cursor = self.mysql_conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        end = time.time()
        return end - start, len(result)
    
    def benchmark_queries(self):
        queries = {
            'count_total': "SELECT COUNT(*) FROM web_logs",
            'count_by_status': "SELECT status_code, COUNT(*) FROM web_logs GROUP BY status_code",
            'avg_response_time': "SELECT AVG(response_time_ms) FROM web_logs",
            'top_urls': "SELECT url, COUNT(*) as cnt FROM web_logs GROUP BY url ORDER BY cnt DESC LIMIT 10",
            'hourly_traffic': """
                SELECT toHour(timestamp) as hour, COUNT(*) as requests 
                FROM web_logs 
                GROUP BY hour ORDER BY hour
            """
        }
        
        results = []
        
        for query_name, query in queries.items():
            # ClickHouse
            ch_time, ch_rows = self.run_clickhouse_query(query)
            
            # MySQL (adapt query if needed)
            mysql_time, mysql_rows = self.run_mysql_query(query)
            
            results.append({
                'query': query_name,
                'clickhouse_time': ch_time,
                'mysql_time': mysql_time,
                'speedup': mysql_time / ch_time,
                'rows_returned': ch_rows
            })
            
            print(f"{query_name}: ClickHouse: {ch_time:.2f}s, MySQL: {mysql_time:.2f}s, Speedup: {mysql_time/ch_time:.1f}x")
        
        return pd.DataFrame(results)

if __name__ == "__main__":
    benchmark = Benchmark()
    results = benchmark.benchmark_queries()
    results.to_csv('benchmark_results.csv', index=False)