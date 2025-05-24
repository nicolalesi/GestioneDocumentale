import os
import re
import time
from lxml import etree
from icrawler.builtin import BingImageCrawler
import hashlib

def nome_file_hash(nome, max_len=100):
    # Pulisci il nome (es. sostituisci spazi con underscore)
    nome_pulito = nome.strip().replace(" ", "_")

    # Calcola hash md5 (stringa esadecimale)
    hash_md5 = hashlib.md5(nome.encode('utf-8')).hexdigest()

    # Combina hash con una parte del nome pulito (ad esempio primi 10 caratteri)
    prefix = nome_pulito[:10]

    # Componi nome file finale
    filename = f"{prefix}__{hash_md5}.jpg"

    # Taglia se troppo lungo (in realtà non serve, è abbastanza corto)
    return filename[:max_len]


# === CONFIG ===
xml_file = "../dati/vini.xml"
output_dir = "../img/immagini_vini/"
immagini_per_vino = 1
delay = 1  # secondi tra i download

# === CREA CARTELLA DESTINAZIONE ===
os.makedirs(output_dir, exist_ok=True)

# === PARSA IL FILE XML E PRENDI I NOMI ===
tree = etree.parse(xml_file)
root = tree.getroot()
nomi_vini = [vino.attrib["nome"] for vino in root.findall(".//Vino") if "nome" in vino.attrib]

# === PULISCI IL NOME FILE (max 100 caratteri) ===
def pulisci_nome(nome, max_len=100):
    base = re.sub(r"[^\w\-_.()]", "_", nome.strip().replace(" ", "_"))
    return base[:max_len]

# === SCARICA IMMAGINI E RINOMINA ===
for i, nome in enumerate(nomi_vini):
    query = nome + " bottiglia vino"
    nome_file = nome_file_hash(nome)
    path_file = os.path.join(output_dir, nome_file)

    print(f"\n🔍 {i+1}/{len(nomi_vini)} Cerco immagine per: {nome}")

    crawler = BingImageCrawler(storage={"root_dir": output_dir})
    crawler.crawl(keyword=query, max_num=1, file_idx_offset=i)

    # Cerca immagine appena scaricata
    immagini = sorted(
        [f for f in os.listdir(output_dir) if f.endswith(".jpg")],
        key=lambda f: os.path.getctime(os.path.join(output_dir, f)),
        reverse=True
    )

    # Rinomina se scaricato qualcosa di nuovo
    file_scaricato = next((f for f in immagini if f != nome_file), None)

    if file_scaricato:
        try:
            os.rename(os.path.join(output_dir, file_scaricato), path_file)
            print(f"✅ Salvata immagine: {nome_file}")
        except Exception as e:
            print(f"❌ Errore nel rinominare immagine: {e}")
    else:
        print("⚠️ Nessuna immagine trovata")

    time.sleep(delay)

print("\n✅ Download completato.")
