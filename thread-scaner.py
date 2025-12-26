import os
import time
import threading
from pathlib import Path

def monitorowanie_folderu(sciezka):
    print(f"Monitorowanie folderu {sciezka}")
    poprzednie_pliki = set()
    
    try:
        while True:
            p = Path(sciezka)
            
            # czy folder istnieje
            if not p.is_dir():
                    print("ściezka do folderu nie istnieje")
                    break
            
            # pobieranie aktualnej listy plików
            try:
                aktualne_pliki = set(f.name for f in p.iterdir() if f.is_file())
            except OSError as e:
                print(f"Błąd odczytu folderu: {e}")
                time.sleep(3)
                continue
            
            
            #porównywanie stanu
            nowe_pliki = aktualne_pliki - poprzednie_pliki
            usuniete_pliki = poprzednie_pliki - aktualne_pliki
            
            if nowe_pliki:
                print(f"[Nowe Pliki]: {", ".join(nowe_pliki)}")
            if usuniete_pliki:
                print(f"[Usunięte Pliki]: {", ".join(usuniete_pliki)}")
            
            #aktualizacja stanu
            poprzednie_pliki = aktualne_pliki
            
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("Zatrzymano skaner")
        
FOLDER = "/Users/goral"

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)
    
monitor_thread = threading.Thread(target=monitorowanie_folderu, args=(FOLDER,), daemon=True)
monitor_thread.start()

print("Monitorowanie uruchomione w tle naciśnij CMD + C aby zakonczyc")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nZamykanie programu")
        
        
        