import json
import xml.etree.ElementTree as ET
import yaml


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def gravar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def ler_yaml(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)


def gravar_yaml(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        yaml.dump(dados, arquivo, allow_unicode=True, sort_keys=False)


def sem_namespace(tag):
    # DECISAO 1: o ElementTree entrega "{namespace}nome"; ficamos só com "nome".
    return tag.split("}")[-1]


def elemento_para_dado(elemento):
    """Converte um elemento XML (e tudo que há dentro dele) em dicionário/valor."""
    filhos = list(elemento)
    texto = (elemento.text or "").strip()

    # DECISAO 2: atributos viram chaves com prefixo "@" (JSON/YAML não têm atributos).
    atributos = {"@" + sem_namespace(k): v for k, v in elemento.attrib.items()}

    # Elemento só com texto (ou vazio): devolve o texto.
    # DECISAO 3: elemento vazio vira None (null); número continua texto ("10").
    if not filhos:
        valor = texto if texto else None
        if atributos:
            if valor is not None:
                atributos["#text"] = valor
            return atributos
        return valor

    # Elemento com filhos: dicionário, chamando a função de novo para cada filho.
    resultado = dict(atributos)
    for filho in filhos:
        nome = sem_namespace(filho.tag)
        dado = elemento_para_dado(filho)
        # DECISAO 4: nomes repetidos viram lista (senão o segundo sobrescreveria o primeiro).
        if nome in resultado:
            if not isinstance(resultado[nome], list):
                resultado[nome] = [resultado[nome]]
            resultado[nome].append(dado)
        else:
            resultado[nome] = dado
    return resultado


def ler_xml(caminho):
    raiz = ET.parse(caminho).getroot()
    return {sem_namespace(raiz.tag): elemento_para_dado(raiz)}


def ler(caminho):
    """Lê o arquivo escolhendo o leitor pelo sufixo."""
    if caminho.endswith(".json"):
        return ler_json(caminho)
    if caminho.endswith((".yaml", ".yml")):
        return ler_yaml(caminho)
    if caminho.endswith(".xml"):
        return ler_xml(caminho)
    raise ValueError(f"Formato nao reconhecido: {caminho}")


def gravar(dados, caminho):
    if caminho.endswith(".json"):
        return gravar_json(dados, caminho)
    if caminho.endswith((".yaml", ".yml")):
        return gravar_yaml(dados, caminho)
    raise ValueError(f"Gravacao nao suportada para: {caminho}")