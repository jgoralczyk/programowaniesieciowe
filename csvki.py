import csv
from pathlib import Path

data = [
    ["name", "age", "city"],
    ["Alice", 25, "Krakow"],
    ["Bob", 30, "Warsaw"],
    ["Charlie", 22, "Gdansk"],
]

path = Path("people.csv")

with path.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
    
print("Utworzono plik: ", path)