import time
from core.agent import run_agent

def start_worker():
    while True:
        print("Checking emails...")
        run_agent()
        # EVERY 120 SEC
        time.sleep(120)

if __name__ == "__main__":
    start_worker()