import requests
import subprocess
import time
import os

def setup_clickhouse_table():
    """Set up ClickHouse table using Python requests"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS web_logs (
        timestamp DateTime,
        user_id Int32,
        ip_address String,
        url String,
        status_code Int16,
        response_time_ms Int32
    ) ENGINE = MergeTree()
    ORDER BY timestamp
    """
    
    try:
        response = requests.post('http://localhost:8123/', data=create_table_query)
        if response.status_code == 200:
            print("✅ ClickHouse table created successfully!")
        else:
            print(f"❌ Error creating table: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

def setup_mysql_table():
    """Set up MySQL table"""
    try:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS web_logs (
            timestamp DATETIME,
            user_id INT,
            ip_address VARCHAR(15),
            url VARCHAR(255),
            status_code SMALLINT,
            response_time_ms INT,
            INDEX(timestamp),
            INDEX(user_id)
        )
        """
        
        # Using mysql command line
        cmd = [
            'mysql', '-h', 'localhost', '-P', '3306', '-u', 'root', '-ppassword', 
            'benchmark', '-e', create_table_sql
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL table created successfully!")
        else:
            print(f"❌ Error creating MySQL table: {result.stderr}")
            
    except Exception as e:
        print(f"❌ MySQL setup error: {e}")

def load_data_to_clickhouse():
    """Load CSV data into ClickHouse"""
    try:
        # Use clickhouse-client to load data
        cmd = [
            'docker', 'exec', 'clickhouse_project-clickhouse-1', 
            'clickhouse-client', 
            '--query', 'INSERT INTO web_logs FORMAT CSV',
            '--input_format_allow_errors_num', '10'
        ]
        
        with open('web_logs.csv', 'r') as f:
            # Skip header
            next(f)
            result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Data loaded into ClickHouse successfully!")
        else:
            print(f"❌ Error loading data to ClickHouse: {result.stderr}")
            
    except Exception as e:
        print(f"❌ ClickHouse data load error: {e}")

def load_data_to_mysql():
    """Load CSV data into MySQL"""
    try:
        # First, get the full path to the CSV file and fix backslashes
        csv_path = os.path.abspath('web_logs.csv')
        # Replace backslashes with forward slashes for MySQL
        mysql_csv_path = csv_path.replace("\\", "/")
        
        load_sql = f"""
        LOAD DATA LOCAL INFILE '{mysql_csv_path}' 
        INTO TABLE web_logs 
        FIELDS TERMINATED BY ',' 
        OPTIONALLY ENCLOSED BY '\\"' 
        LINES TERMINATED BY '\\n' 
        IGNORE 1 ROWS
        """
        
        cmd = [
            'mysql', '-h', 'localhost', '-P', '3306', '-u', 'root', '-ppassword', 
            'benchmark', '-e', load_sql
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Data loaded into MySQL successfully!")
        else:
            print(f"❌ Error loading data to MySQL: {result.stderr}")
            
    except Exception as e:
        print(f"❌ MySQL data load error: {e}")

def check_database_connections():
    """Check if databases are accessible"""
    print("🔍 Checking database connections...")
    
    # Check ClickHouse
    try:
        response = requests.get('http://localhost:8123/ping')
        if response.status_code == 200:
            print("✅ ClickHouse is running")
        else:
            print("❌ ClickHouse is not accessible")
    except:
        print("❌ ClickHouse connection failed")
    
    # Check MySQL
    try:
        cmd = ['mysql', '-h', 'localhost', '-P', '3306', '-u', 'root', '-ppassword', '-e', 'SELECT 1']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL is running")
        else:
            print("❌ MySQL is not accessible")
    except:
        print("❌ MySQL connection failed")

if __name__ == "__main__":
    print("🚀 Starting database setup...")
    
    # Check connections first
    check_database_connections()
    
    print("\n📊 Setting up database tables...")
    
    # Wait for databases to be ready
    time.sleep(3)
    
    setup_clickhouse_table()
    setup_mysql_table()
    
    print("\n📥 Loading data into databases...")
    
    # Check if data file exists
    if not os.path.exists('web_logs.csv'):
        print("❌ web_logs.csv not found. Please run data_generator.py first.")
        exit(1)
    
    load_data_to_clickhouse()
    load_data_to_mysql()
    
    print("\n🎉 Database setup completed!")
    print("\nNext steps:")
    print("1. Run: python query_runner.py")
    print("2. Then run: python results_analyzer.py")