import time
import random

quotes = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Do what you can, with what you have, where you are.",
    "Life is 10% what happens to us and 90% how we react to it."
]

file_path = "/data/quotes.txt"

while True:
    with open(file_path, "a") as f:
        f.write(random.choice(quotes) + "\n")
    print("Wrote a new quote to the shared file.", flush=True)
    time.sleep(10)
