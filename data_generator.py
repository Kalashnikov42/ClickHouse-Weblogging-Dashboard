import csv
import random
from datetime import datetime, timedelta

def simple_data_generator(num_rows=10000):
    """Simpler data generator without Faker"""
    print(f"Generating {num_rows} simple log entries...")
    
    with open('web_logs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'user_id', 'ip_address', 'url', 'status_code', 'response_time_ms'])
        
        start_date = datetime(2023, 1, 1)
        
        for i in range(num_rows):
            # Simple timestamp generation
            days_offset = random.randint(0, 365)
            hours_offset = random.randint(0, 23)
            timestamp = start_date + timedelta(days=days_offset, hours=hours_offset)
            
            user_id = random.randint(1, 1000)
            ip_address = f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"
            url = random.choice(['/home', '/products', '/about', '/contact', '/api/data'])
            status_code = random.choice([200, 200, 200, 404, 500])
            response_time = random.randint(50, 1000)
            
            writer.writerow([
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                user_id, 
                ip_address, 
                url, 
                status_code, 
                response_time
            ])
    
    print(f"✅ Generated {num_rows} rows in web_logs.csv")

if __name__ == "__main__":
    simple_data_generator(10000)