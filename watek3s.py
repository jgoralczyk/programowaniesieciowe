import os
import time
import threading

class FolderWatcher(threading.Thread):
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        if not os.path.isdir(folder_path):
            raise ValueError(f"podana sciezka nie jest folderem {folder_path}")
        self.last_state = {}
        self._stop_event = threading.Event()
    
    def run(self):
        print(f'Rozpoczynam monitorowanie folderu: {self.folder_path}')
        while not self._stop_event.is_set():
            self.scan_folder()
            time.sleep(3)
    
    def stop(self):
        self._stop_event.set()
        
    def scan_folder(self):
        current_state= {}
        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)
            if os.path.isfile(filepath):
                current_state[filename] = os.path.getmtime(filepath)
                if filename not in self.last_state:
                    print(f"[+] Dodano plik: {filename}")
                elif self.last_state[filename] != os.path.getmtime(filepath):
                    print(f"[~] Zmieniono plik: {filename}")
                    
        for old_file in list(self.last_state.keys()):
            if old_file not in current_state:
                print(f'[-] Usunieto plik: {old_file}')
        
        self.last_state = current_state
    
if __name__ == "__main__":
    folder_path = r"/Users/goral/Music"
    
    watcher = FolderWatcher(folder_path)
    watcher.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nZatrzymuje monitorowanie")
        watcher.stop()