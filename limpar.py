import sys
from xml.dom import minidom

entrada, saida = sys.argv[1], sys.argv[2]
bruto = open(entrada, encoding="utf-8").read()
xml = bruto.split("]]>]]>")[0]
bonito = minidom.parseString(xml.encode("utf-8")).toprettyxml(indent="  ")
linhas = [l for l in bonito.splitlines() if l.strip()]
open(saida, "w", encoding="utf-8").write("\n".join(linhas) + "\n")
print(saida, ":", len(linhas), "linhas")