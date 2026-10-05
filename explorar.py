import xml.etree.ElementTree as ET

raiz = ET.parse("rpc-reply.xml").getroot()
print(raiz.tag)
print(raiz.attrib)
for filho in raiz:
    print("  ", filho.tag, filho.attrib)