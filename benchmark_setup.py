import subprocess
import time

def setup_databases():
    # Start ClickHouse and MySQL using Docker Compose
    docker_compose = """
version: '3.7'
services:
  clickhouse:
    image: clickhouse/clickhouse-server:latest
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./data/clickhouse:/var/lib/clickhouse
      
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: benchmark
    ports:
      - "3306:3306"
    volumes:
      - ./data/mysql:/var/lib/mysql
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    
    # Start containers
    subprocess.run(['docker-compose', 'up', '-d'])
    time.sleep(30)  # Wait for databases to start

if __name__ == "__main__":
    setup_databases()