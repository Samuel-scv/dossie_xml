# converter.py - converte um arquivo XML (NETCONF) para JSON ou YAML
import sys

import formatos

if len(sys.argv) != 3:
    print("Uso: python converter.py <entrada> <saida>")
    sys.exit(1)

origem, destino = sys.argv[1], sys.argv[2]

dados = formatos.ler(origem)
if not dados:
    # falhar cedo e alto, em vez de gravar um arquivo vazio em silencio
    raise ValueError(f"Nada foi lido de {origem}")
formatos.gravar(dados, destino)

raiz = next(iter(dados))
print(f"Conversao concluida: {origem} -> {destino} (elemento raiz: {raiz}).")