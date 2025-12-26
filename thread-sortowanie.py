import os
import shutil
import time
import threading
from pathlib import Path


# Konfiguracja
FOLDER_ZRODLOWY = "./testowy_folder"
FOLDER_DOCELOWY_BAZA = "./posortowane"
MAPOWANIE_ROZSZERZEN = {
    "dokumenty": [".txt", ".doc", ".csv", ".pdf"],
    "obrazy": [".png", ".jpg", ".bmp"],
}
FOLDER_ROZNE = "rozne"

def sortuj_pliki():
    print("Sortowanie plików rozpoczęte...")
    
    for folder in list(MAPOWANIE_ROZSZERZEN.keys()) + [FOLDER_ROZNE]:
        os.makedirs(Path(FOLDER_DOCELOWY_BAZA) / folder, exist_ok= True)
        
    p_zrodlo = Path(FOLDER_ZRODLOWY)
    
    try:
        while True:
            for plik in p_zrodlo.iterdir():
                if not plik.is_file():
                    continue # Ignoruj podfoldery
                
                docelowy_podfolder = FOLDER_ROZNE
                
                for folder_doc, rozszerzenia in MAPOWANIE_ROZSZERZEN.items():
                    if plik.suffix.lower() in rozszerzenia:
                        docelowy_podfolder = folder_doc
                        break
                    
                sciezka_docelowa = Path(FOLDER_DOCELOWY_BAZA) / docelowy_podfolder / plik.name
                try:
                    
                    shutil.move((str(plik)), str(sciezka_docelowa))
                    print(f"Przeniesiono: {plik.name} -> {docelowy_podfolder}")
                except Exception as e:
                    print(f"Błąd przy przenoszeniu {plik.name}: {e}")
                    
            time.sleep(10)
    except KeyboardInterrupt:
        print("zatrzymano program")
        
sorter_thread = threading.Thread(target=sortuj_pliki, daemon= True)
sorter_thread.start()

print(f"Sorter plików uruchomiony. Monitoruje {FOLDER_ZRODLOWY}...")
print("Wrzuć pliki do tego folderu. Zostaną posortowane co 10 sekund.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nZatrzymanie programu")