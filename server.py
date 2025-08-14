from flask import Flask, Response

ARQUIVO_M3U = "lista.m3u"

# Palavras-chave para filtrar canais
CANAIS_PERMITIDOS = [
    'RECORDTV SP [FHD]',
    'GLOBO',
    'SBT'
]

app = Flask(__name__)

def filtrar_m3u():
    try:
        with open(ARQUIVO_M3U, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()

        nova_lista = []
        adicionar = False

        for linha in linhas:
            if linha.startswith("#EXTINF"):
                adicionar = any(canal.lower() in linha.lower() for canal in CANAIS_PERMITIDOS)
            if adicionar:
                nova_lista.append(linha)

        return "".join(nova_lista)
    except FileNotFoundError:
        return "# Arquivo M3U não encontrado"

@app.route("/lista.m3u")
def get_lista():
    conteudo = filtrar_m3u()
    return Response(conteudo, mimetype="application/vnd.apple.mpegurl")

@app.route("/")
def home():
    return "Servidor M3U Online! Acesse /lista.m3u"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
