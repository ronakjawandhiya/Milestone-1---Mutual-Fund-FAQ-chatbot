import schedule
import time
import subprocess
import sys
from datetime import datetime

def update_fund_data():
    """Function to update fund data by running both scrapers"""
    print(f"[{datetime.now()}] Starting daily fund data update...")
    
    try:
        # Run the final scraper to update Large Cap Fund data
        print(f"[{datetime.now()}] Updating ICICI Prudential Large Cap Fund data...")
        result1 = subprocess.run([sys.executable, 'final_scraper.py'], 
                               capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result1.returncode == 0:
            print(f"[{datetime.now()}] Large Cap Fund data update completed successfully!")
        else:
            print(f"[{datetime.now()}] Error during Large Cap Fund data update!")
            print(f"Error: {result1.stderr}")
            
        # Run the ELSS scraper to update ELSS Fund data
        print(f"[{datetime.now()}] Updating ICICI Prudential ELSS Tax Saver Fund data...")
        result2 = subprocess.run([sys.executable, 'elss_scraper.py'], 
                               capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result2.returncode == 0:
            print(f"[{datetime.now()}] ELSS Fund data update completed successfully!")
        else:
            print(f"[{datetime.now()}] Error during ELSS Fund data update!")
            print(f"Error: {result2.stderr}")
            
    except subprocess.TimeoutExpired:
        print(f"[{datetime.now()}] Fund data update timed out!")
    except Exception as e:
        print(f"[{datetime.now()}] Unexpected error during fund data update: {e}")

def run_scheduler():
    """Run the scheduler indefinitely"""
    # Schedule the update to run every day at 5:00 AM
    schedule.every().day.at("05:00").do(update_fund_data)
    
    print(f"[{datetime.now()}] Scheduler started. Waiting for scheduled tasks...")
    print("Fund data will be updated daily at 5:00 AM")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Also run an immediate update when the scheduler starts
    print(f"[{datetime.now()}] Running initial fund data update...")
    update_fund_data()
    
    # Start the scheduler
    run_scheduler()