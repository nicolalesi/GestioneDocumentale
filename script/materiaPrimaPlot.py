import os
import re
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from lxml import etree

# Imposta font base più grande
plt.rcParams.update({'font.size': 10})

# Carica XML
with open("../dati/vini.xml", "rb") as f:
    root = etree.fromstring(f.read())

# Percorsi output
output_dir_generale = "../img/Grafici"
output_dir_regionali = os.path.join(output_dir_generale, "Regionali")
os.makedirs(output_dir_generale, exist_ok=True)
os.makedirs(output_dir_regionali, exist_ok=True)

# Pattern per catturare elementi tra apici
pattern = r"'(.*?)'"
parole_chiave_generiche = ("Altre", "Vitigni", "Uve", "Varietà")

# Conteggio globale per materie prime generiche
materie_prime_generiche = []

# Conteggio per regione (senza filtraggio)
conteggio_per_regione = defaultdict(list)

for vino in root:
    try:
        materia_prima = vino.find("MateriaPrima").text
        if not materia_prima:
            continue

        # Estrazione per grafico generale
        estratti = re.findall(pattern, materia_prima)
        for item in estratti:
            if item.strip().startswith(parole_chiave_generiche):
                materie_prime_generiche.append(item.strip())

        # Regione
        regione = vino.find("Luogo")[0].get("nome")
        conteggio_per_regione[regione].append(materia_prima.strip())

    except Exception as e:
        print(f"Errore su vino: {e}")
        continue

# ========== GRAFICO GENERALE ========== #
conteggio_globale = Counter(materie_prime_generiche)
sigle = {nome: f"{i+1}" for i, nome in enumerate(conteggio_globale.keys())}
etichette = [sigle[nome] for nome in conteggio_globale.keys()]

fig, ax = plt.subplots(figsize=(14, 10))
ax.bar(etichette, conteggio_globale.values(), color="teal")
ax.set_xlabel("Sigle delle materie prime", fontsize=12)
ax.set_ylabel("Numero di occorrenze", fontsize=12)
ax.set_title("Distribuzione globale delle materie prime generiche nei vini", fontsize=14)
ax.set_xticks(range(len(etichette)))
ax.set_xticklabels(etichette, rotation=45, ha="right", fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(output_dir_generale, "generale.png"))
plt.close()

# Salva legenda come immagine separata
fig_leg, ax_leg = plt.subplots(figsize=(10, len(sigle) * 0.3))
ax_leg.axis("off")
legenda_text = "\n".join([f"{sigla}: {nome}" for nome, sigla in sigle.items()])
ax_leg.text(0, 1, legenda_text, fontsize=10, va='top')
plt.tight_layout()
plt.savefig(os.path.join(output_dir_generale, "generale_legenda.png"))
plt.close()


# ========== GRAFICI REGIONALI ========== #
for regione, lista_materie in conteggio_per_regione.items():
    conteggio = Counter(lista_materie)
    sigle_regionali = {nome: f"{i+1}" for i, nome in enumerate(conteggio.keys())}
    etichette = [sigle_regionali[nome] for nome in conteggio.keys()]

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.bar(etichette, conteggio.values(), color="darkred")
    ax.set_xlabel("Sigle delle materie prime", fontsize=12)
    ax.set_ylabel("Numero di occorrenze", fontsize=12)
    ax.set_title(f"Distribuzione materie prime - {regione}", fontsize=14)
    ax.set_xticks(range(len(etichette)))
    ax.set_xticklabels(etichette, rotation=45, ha="right", fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir_regionali, f"{regione}.png"))
    plt.close()

    # Salva legenda regionale
    fig_leg, ax_leg = plt.subplots(figsize=(10, len(sigle_regionali) * 0.3))
    ax_leg.axis("off")
    legenda = "\n".join([f"{sigla}: {nome}" for nome, sigla in sigle_regionali.items()])
    ax_leg.text(0, 1, legenda, fontsize=10, va='top')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir_regionali, f"{regione}_legenda.png"))
    plt.close()

