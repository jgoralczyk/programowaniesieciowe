from pathlib import Path
if __name__ == "__main__":
    # with open("tescik.txt", "w") as f:
    #     f.write("Ciekawe czy wiedział\n")
    #     f.write("bo mi się wydaję\n")
    #     f.write("ze jednak nie\n")
        
    # with open("tescik.txt", "r") as f:
    #     for line in f:
    #         print(line.strip())
    
    def analyze_folder(path):
        folder = Path(path)
        print("obecny katalog roboczy:", folder)
        
        size = 0
        quantity = 0
        
        report_path = folder / "logs.txt"
        
        with open(report_path, "w") as log:
            for file in folder.glob("*.txt"):
                size += file.stat().st_size
                quantity += 1
                
            log.write(f"Folder: {folder}\n")
            log.write(f"Liczba plików .txt: {quantity}\n")
            log.write(f"Łączny rozmiar: {size} bajty\n")
        
        return report_path
        
    report = analyze_folder("test_folder_pathlib")
    print("Raport zapisano w:", report)
    print(report.read_text())
    
    