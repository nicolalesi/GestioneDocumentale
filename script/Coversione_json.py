import xmltodict
import json

# === CONFIGURAZIONE ===
# Percorso del file XML da convertire
xml_input_path = "../dati/vini.xml"  
# Percorso per il file JSON di output
json_output_path = "../dati/json/vini_completo.json"  

# === FUNZIONE DI CONVERSIONE ===
def convert_xml_to_json(xml_path, output_path, regione=None):
    with open(xml_path, 'r', encoding='utf-8') as f:
        doc = xmltodict.parse(f.read())

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)

    print(f"File JSON salvato in: {output_path}")


# === ESECUZIONE ===
convert_xml_to_json(xml_input_path, json_output_path)
