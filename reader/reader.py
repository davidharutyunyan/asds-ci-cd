import time

file_path = "/data/quotes.txt"

while True:
    try:
        with open(file_path, "r") as f:
            print("Quotes in the shared file:", flush=True)
            print(f.read(), flush=True)
    except FileNotFoundError:
        print("Shared file not found. Waiting for writer to create it...", flush=True)
    time.sleep(5)
