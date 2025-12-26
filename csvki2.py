import csv
from pathlib import Path

# path = Path("people.csv")

# with path.open("r") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)
        
# with path.open("r") as f1:
#     reader = csv.DictReader(f1)
#     for row in reader:
#         print(f"{row['name']} ma {row['age']} lat i mieszkwa w {row['city']}")
        
        
def filter_people(csv_path, min_age):
    
    path1 = Path(csv_path)
    path2 = Path("filtered.csv")
    
    with path1.open("r") as f_in, path2.open("w", newline="") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if int(row["age"]) >= min_age:
                writer.writerow(row)

filter_people("people.csv", 25)