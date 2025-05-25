import xmltodict
import json
import os

# === CONFIGURAZIONE ===
xml_input_path = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO/vini.xml"
output_dir = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO/Conversione/json_regioni/"

os.makedirs(output_dir, exist_ok=True)

def convert_xml_to_json_per_region(xml_path, output_dir):
    with open(xml_path, 'r', encoding='utf-8') as f:
        doc = xmltodict.parse(f.read())

    vini = doc["Vini"]["Vino"]
    regioni_map = {}

    # Organizza i vini per regione
    for vino in vini:
        regioni = vino["Luogo"]["Regione"]
        if isinstance(regioni, dict):
            regioni = [regioni]

        for regione in regioni:
            nome_regione = regione.get("@nome", "Sconosciuta")
            if nome_regione not in regioni_map:
                regioni_map[nome_regione] = []
            # Salviamo solo il vino, non il blocco regione (già incluso)
            regioni_map[nome_regione].append(vino)

    # Crea un JSON per ogni regione
    for nome_regione, vini_lista in regioni_map.items():
        filename = f"{nome_regione.replace(' ', '_')}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(vini_lista, f, indent=2, ensure_ascii=False)

        print(f"[✔] Creato: {filepath}")

# === ESECUZIONE ===
convert_xml_to_json_per_region(xml_input_path, output_dir)
