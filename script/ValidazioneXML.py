from lxml import etree

DIR_PATH = "./Validazione/"


DTD_FILENAME = "../DTD_ViniXML"
XML_FILENAME = "../vini_ITA_Singolare.xml"

dtd_filename = DIR_PATH + DTD_FILENAME
xml_filename = DIR_PATH + XML_FILENAME

dtd_file = open(dtd_filename, 'r')
xml_file = open(xml_filename, 'r')

# Nota: assumiamo che il file XML
#       in input sia ben formato
#
# Nota 2: in questo caso il documento XML
#         è stato caricato da file ma può
#         essere generato anche da una stringa o programmaticamente
xml_root = etree.parse(xml_filename)


try:
    # Carica DTD se sintatticamente corretto
    # oppure solleva un'eccezione
    dtd = etree.DTD(dtd_file)

    # Valida rispetto al DTD e restituisce un booleano
    if dtd.validate(xml_root):
        print("Valid XML!")
    else:
        # Recupera l'errore di validazione dai log
        validation_error = dtd.error_log.filter_from_errors()[0]
        print("XML not valid!\n", validation_error)
except:
  print("DTD non corretto")