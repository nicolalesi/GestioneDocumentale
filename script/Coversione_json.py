import xmltodict
import json

# === CONFIGURAZIONE ===
# Percorso del file XML da convertire
xml_input_path = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO/vini.xml"  # ⬅️ Inserisci qui il percorso completo del tuo file XML

# Percorso per il file JSON di output
json_output_path = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO/vini_completo.json"  # ⬅️ Dove salvare il file JSON

# === FUNZIONE DI CONVERSIONE ===
def convert_xml_to_json(xml_path, output_path, regione=None):
    with open(xml_path, 'r', encoding='utf-8') as f:
        doc = xmltodict.parse(f.read())

    vini = doc["Vini"]["Vino"]  # Lista dei vini
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vini, f, indent=2, ensure_ascii=False)

    print(f"[✔] File JSON salvato in: {output_path}")


# === ESECUZIONE ===
convert_xml_to_json(xml_input_path, json_output_path)
