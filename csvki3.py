import csv
from pathlib import Path
import pandas as pd


def filter_people(csv_path, min_age, descending = False):
    path1 = Path(csv_path)
    path2 = Path("filtered.csv")
    
    with path1.open("r") as f_in:
        reader = csv.DictReader(f_in)
        data = [row for row in reader if int(row["age"]) >= min_age]
        
    data.sort(key=lambda row: int(row["age"]), reverse=descending)
    
    with path2.open("w") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=["name",'age','city'])
        writer.writeheader()
        writer.writerows(data)
        
filter_people("people.csv", 23, descending=True)

def filter_people_pandas(csv_path, min_age):
    
    df = pd.read_csv(csv_path)
    
    filtered = df[df["age"] >= min_age]
    
    filtered.to_csv("filtered.csv", index = False)
    
    return filtered

if __name__ == "__main__":
    result = filter_people_pandas("people.csv", 25)
    print(result)