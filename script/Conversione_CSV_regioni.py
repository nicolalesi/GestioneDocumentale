import xmltodict
import csv
import os

# === CONFIGURAZIONE ===
xml_input_path = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO/vini.xml"
output_dir = "/Users/robertozanoni/Downloads/LM_ANNO 2/SEMESTRE 2/Elaborazione Testi e Gestione Documentale/PROGETTO/Conversione/csv_regioni/"

os.makedirs(output_dir, exist_ok=True)

def convert_xml_to_csv_per_region(xml_path, output_dir):
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
            regioni_map[nome_regione].append((vino, regione))

    # Crea un CSV per ogni regione
    for nome_regione, entries in regioni_map.items():
        filename = f"{nome_regione.replace(' ', '_')}.csv"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Nome", "Tipologia", "Denominazione", "Descrizione",
                "Valore minimo", "Valore massimo", "Materia prima",
                "Regione", "Province", "Città"
            ])

            for vino, regione in entries:
                nome = vino.get("@nome", "")
                tipologia = vino.get("Tipologia", "")
                denominazione = vino.get("Denominazione", "")
                descrizione = vino.get("Descrizione", "")
                valore_min = vino.get("ValoreMinimo", "")
                valore_max = vino.get("ValoreMassimo", "")
                materia = vino.get("MateriaPrima", "")

                province = []
                citta = []

                province_raw = regione.get("Provincia", [])
                if isinstance(province_raw, dict):
                    province_raw = [province_raw]
                elif isinstance(province_raw, str):
                    province_raw = [{"@nome": province_raw}]

                for prov in province_raw:
                    if isinstance(prov, dict):
                        province.append(prov.get("@nome", ""))
                        citta_raw = prov.get("Città", [])
                        if isinstance(citta_raw, dict):
                            citta_raw = [citta_raw]
                        elif isinstance(citta_raw, str):
                            citta_raw = [{"@nome": citta_raw}]
                        for city in citta_raw:
                            if isinstance(city, dict):
                                citta.append(city.get("@nome", ""))
                            else:
                                citta.append(str(city))
                    else:
                        province.append(str(prov))

                writer.writerow([
                    nome, tipologia, denominazione, descrizione,
                    valore_min, valore_max, materia,
                    nome_regione,
                    ", ".join(province),
                    ", ".join(citta)
                ])

        print(f"[✔] Creato: {filepath}")

# === ESECUZIONE ===
convert_xml_to_csv_per_region(xml_input_path, output_dir)
