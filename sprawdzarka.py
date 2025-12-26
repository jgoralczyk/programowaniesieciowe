import os
import shutil
from pathlib import Path




# zrodlo = Path(FOLDER)

# for plik in zrodlo.iterdir():
    
FOLDER = "/Users/goral"
def zlistuj_plicki(folderino: str):
    zrodlo = Path(folderino)
    
    for plik in zrodlo.iterdir():
        if not plik.is_dir():
            yield plik
            print("spermiara")
            continue
    
for element in zlistuj_plicki(FOLDER):
    print(f"Znaleziono: {element}")
