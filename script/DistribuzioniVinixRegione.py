import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Carica XML
tree = ET.parse('../dati/vini.xml')
root = tree.getroot()

#distribuzioni vini per regione
# Conta i vini per regione (Regione è attributo di <Regione> dentro <Luogo>)
conteggio_regioni = {}
for vino in root.findall('Vino'):
    luogo = vino.find('Luogo')
    if luogo is not None:
        regione_tag = luogo.find('Regione')
        if regione_tag is not None:
            regione = regione_tag.get('nome', 'Sconosciuta')  # prende l'attributo 'nome'
        else:
            regione = 'Sconosciuta'
    else:
        regione = 'Sconosciuta'

    conteggio_regioni[regione] = conteggio_regioni.get(regione, 0) + 1

# Dati per il grafico
regioni = list(conteggio_regioni.keys())
quantita = list(conteggio_regioni.values())

# Crea il grafico
plt.figure(figsize=(12, 6))
plt.bar(regioni, quantita, color='#8B0000')
plt.xticks(rotation=45, ha='right')
plt.title('Numero di vini per regione')
plt.xlabel('Regione')
plt.ylabel('Numero di vini')

# Imposta scalini sull'asse Y ogni 5 unità
max_val = max(quantita)
plt.yticks(range(0, max_val + 6, 5))  # +6 per includere l'ultimo step

plt.tight_layout()

# Percorso dove salvare il grafico
percorso_output = '/Users/robertozanoni/Desktop/GestioneDocumentale/Grafici'
os.makedirs(percorso_output, exist_ok=True)

# Salva il file
output_file = os.path.join(percorso_output, 'grafico_vini_per_regione.png')
plt.savefig(output_file)
print(f"Grafico salvato in: {output_file}")
###########################

# Classificazione ISTAT delle regioni italiane
nord = ['Piemonte', 'Valle d\'Aosta', 'Lombardia', 'Trentino-Alto Adige', 'Veneto', 'Friuli-Venezia Giulia', 'Liguria', 'Emilia-Romagna']
centro = ['Toscana', 'Umbria', 'Marche', 'Lazio']
sud = ['Abruzzo', 'Molise', 'Campania', 'Puglia', 'Basilicata', 'Calabria', 'Sicilia', 'Sardegna']

# Conteggi per macroarea
conteggio_zone = {'Nord': 0, 'Centro': 0, 'Sud': 0, 'Sconosciuta': 0}

for regione, count in conteggio_regioni.items():
    if regione in nord:
        conteggio_zone['Nord'] += count
    elif regione in centro:
        conteggio_zone['Centro'] += count
    elif regione in sud:
        conteggio_zone['Sud'] += count
    else:
        conteggio_zone['Sconosciuta'] += count

# Rimuovi 'Sconosciuta' se ha valore 0
if conteggio_zone['Sconosciuta'] == 0:
    del conteggio_zone['Sconosciuta']

# Dati per il grafico a torta
labels = list(conteggio_zone.keys())
valori = list(conteggio_zone.values())
colori = ['#C08090', '#AF6900', '#D9B382', '#F5EBDACC']  # puoi personalizzare

# Crea grafico a torta
plt.figure(figsize=(7, 7))
plt.pie(valori, labels=labels, autopct='%1.1f%%', startangle=90, colors=colori)
plt.title('Distribuzione percentuale dei vini per zona ISTAT')
plt.tight_layout()

# Salva il grafico
output_pie = os.path.join(percorso_output, 'grafico_vini_per_zona.png')
plt.savefig(output_pie)
print(f"Grafico a torta salvato in: {output_pie}")
