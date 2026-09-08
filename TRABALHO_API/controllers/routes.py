from flask import Blueprint, render_template, request
import requests


routes = Blueprint(
    "routes",
    __name__
)

TMDB_API_URL = "https://api.themoviedb.org/3"

TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjNmE4ZDNkMzQ4ODY2MjlmN2MyZTVmNzhmY2FlNjRmMyIsIm5iZiI6MTc4Njk3NDM5OS40MDgsInN1YiI6IjZhODMxMGJmMjAyMmExN2YyODk1N2ZkYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9Wn0MB3PK4pSJztH5oW_ip5LTzGUVvxMT2h9LgPqbLk"


def tmdb_headers():

    return {
        "Authorization": f"Bearer {TMDB_TOKEN}",
        "accept": "application/json"
    }


def converter_dorama(item):

    poster = item.get("poster_path")

    if poster:

        imagem = TMDB_IMAGE_URL + poster

    else:

        imagem = None


    paises = item.get(
        "origin_country",
        []
    )

    if paises:

        pais = paises[0]

    else:

        pais = "Não informado"


    data = item.get(
        "first_air_date",
        ""
    )

    if data:

        ano = data[:4]

    else:

        ano = "Não informado"


    return {

        "id": item.get("id"),

        "titulo": item.get(
            "name",
            "Sem título"
        ),

        "titulo_original": item.get(
            "original_name",
            "Não informado"
        ),

        "ano": ano,

        "pais": pais,

        "categoria": "Dorama",

        "genero": item.get(
            "genero",
            "Drama"
        ),

        "sinopse": item.get(
            "overview",
            "Sinopse não disponível."
        ),

        "imagem": imagem,

        "avaliacao": item.get(
            "vote_average",
            0
        ),

        "episodios": item.get(
            "number_of_episodes",
            None
        ),

        "status": item.get(
            "status",
            "Não informado"
        )

    }



@routes.route("/")
def index():

    return render_template(
        "index.html"
    )


@routes.route(
    "/api/doramas",
    methods=["GET"]
)
def api_listar_doramas():

    url = f"{TMDB_API_URL}/discover/tv"


    parametros = {

        "language": "pt-BR",

        "with_origin_country": "KR",

        "with_genres": "18",

        "sort_by": "popularity.desc",

        "page": 1

    }


    try:

        resposta = requests.get(

            url,

            headers=tmdb_headers(),

            params=parametros,

            timeout=15

        )

    except requests.exceptions.RequestException:

        return {

            "sucesso": False,

            "mensagem":
                "Não foi possível conectar à TMDB."

        }, 502


    if resposta.status_code != 200:

        return {

            "sucesso": False,

            "mensagem":
                "Erro ao consultar a TMDB.",

            "status":
                resposta.status_code

        }, 502


    dados = resposta.json()


    resultado = []


    for item in dados.get(
        "results",
        []
    ):

        resultado.append(
            converter_dorama(item)
        )


    return {

        "sucesso": True,

        "pagina": dados.get(
            "page"
        ),

        "total_resultados":
            dados.get(
                "total_results"
            ),

        "doramas": resultado

    }


@routes.route(
    "/api/doramas/<int:id>",
    methods=["GET"]
)
def api_dorama(id):

    url = f"{TMDB_API_URL}/tv/{id}"


    parametros = {

        "language": "pt-BR"

    }


    try:

        resposta = requests.get(

            url,

            headers=tmdb_headers(),

            params=parametros,

            timeout=15

        )

    except requests.exceptions.RequestException:

        return {

            "sucesso": False,

            "mensagem":
                "Não foi possível conectar à TMDB."

        }, 502


    if resposta.status_code == 404:

        return {

            "sucesso": False,

            "mensagem":
                "Dorama não encontrado."

        }, 404


    if resposta.status_code != 200:

        return {

            "sucesso": False,

            "mensagem":
                "Erro ao consultar a TMDB.",

            "status":
                resposta.status_code

        }, 502


    dados = resposta.json()


    resultado = converter_dorama(
        dados
    )


    generos = dados.get(
        "genres",
        []
    )


    resultado["genero"] = ", ".join(

        genero["name"]

        for genero in generos

    )


    resultado["numero_temporadas"] = dados.get(
        "number_of_seasons"
    )


    resultado["episodios"] = dados.get(
        "number_of_episodes"
    )


    resultado["status"] = dados.get(
        "status",
        "Não informado"
    )


    resultado["pais"] = ", ".join(

        dados.get(
            "origin_country",
            []
        )

    ) or "Não informado"


    return {

        "sucesso": True,

        "dorama": resultado

    }


@routes.route(
    "/api/doramas/pesquisar",
    methods=["GET"]
)
def api_pesquisar():

    termo = request.args.get(
        "q",
        ""
    ).strip()


    if not termo:

        return {

            "sucesso": False,

            "mensagem":
                "Digite um termo para pesquisar."

        }, 400


    url = f"{TMDB_API_URL}/search/tv"


    parametros = {

        "query": termo,

        "language": "pt-BR",

        "page": 1,

        "include_adult": False

    }


    try:

        resposta = requests.get(

            url,

            headers=tmdb_headers(),

            params=parametros,

            timeout=15

        )

    except requests.exceptions.RequestException:

        return {

            "sucesso": False,

            "mensagem":
                "Não foi possível conectar à TMDB."

        }, 502


    if resposta.status_code != 200:

        return {

            "sucesso": False,

            "mensagem":
                "Erro ao pesquisar na TMDB.",

            "status":
                resposta.status_code

        }, 502


    dados = resposta.json()


    resultado = []


    for item in dados.get(
        "results",
        []
    ):

        if "KR" in item.get(
            "origin_country",
            []
        ):

            resultado.append(
                converter_dorama(item)
            )


    return {

        "sucesso": True,

        "termo": termo,

        "quantidade":
            len(resultado),

        "doramas":
            resultado

    }



@routes.route("/doramas")
def doramas():

    url = f"{TMDB_API_URL}/discover/tv"


    parametros = {

        "language": "pt-BR",

        "with_origin_country": "KR",

        "with_genres": "18",

        "sort_by": "popularity.desc",

        "page": 1

    }


    try:

        resposta = requests.get(

            url,

            headers=tmdb_headers(),

            params=parametros,

            timeout=15

        )

    except requests.exceptions.RequestException:

        return render_template(

            "doramas.html",

            doramas=[],

            erro=
                "Não foi possível conectar à TMDB."

        )


    if resposta.status_code != 200:

        return render_template(

            "doramas.html",

            doramas=[],

            erro=
                "Não foi possível carregar os doramas da TMDB."

        )


    dados = resposta.json()


    lista = []


    for item in dados.get(
        "results",
        []
    ):

        lista.append(
            converter_dorama(item)
        )


    return render_template(

        "doramas.html",

        doramas=lista

    )


@routes.route("/pesquisar")
def pesquisar():

    termo = request.args.get(
        "q",
        ""
    ).strip()


    if not termo:

        return render_template(

            "doramas.html",

            doramas=[],

            erro=
                "Digite o nome de um dorama."

        )


    url = f"{TMDB_API_URL}/search/tv"


    parametros = {

        "query": termo,

        "language": "pt-BR",

        "page": 1,

        "include_adult": False

    }


    try:

        resposta = requests.get(

            url,

            headers=tmdb_headers(),

            params=parametros,

            timeout=15

        )

    except requests.exceptions.RequestException:

        return render_template(

            "doramas.html",

            doramas=[],

            pesquisa=termo,

            erro=
                "Não foi possível conectar à TMDB."

        )


    if resposta.status_code != 200:

        return render_template(

            "doramas.html",

            doramas=[],

            pesquisa=termo,

            erro=
                "Erro ao pesquisar na TMDB."

        )


    dados = resposta.json()


    lista = []


    for item in dados.get(
        "results",
        []
    ):

        if "KR" in item.get(
            "origin_country",
            []
        ):

            lista.append(
                converter_dorama(item)
            )


    return render_template(

        "doramas.html",

        doramas=lista,

        pesquisa=termo

    )


@routes.route(
    "/dorama/<int:id>"
)
def dorama_info(id):

    url = f"{TMDB_API_URL}/tv/{id}"


    parametros = {

        "language": "pt-BR"

    }


    try:

        resposta = requests.get(

            url,

            headers=tmdb_headers(),

            params=parametros,

            timeout=15

        )

    except requests.exceptions.RequestException:

        return render_template(

            "doramainfo.html",

            dorama=None,

            erro=
                "Não foi possível conectar à TMDB."

        )


    if resposta.status_code == 404:

        return render_template(

            "doramainfo.html",

            dorama=None,

            erro=
                "Dorama não encontrado."

        )


    if resposta.status_code != 200:

        return render_template(

            "doramainfo.html",

            dorama=None,

            erro=
                "Erro ao consultar a TMDB."

        )


    dados = resposta.json()


    dorama = converter_dorama(
        dados
    )


    generos = dados.get(
        "genres",
        []
    )


    dorama["genero"] = ", ".join(

        genero["name"]

        for genero in generos

    )


    dorama["numero_temporadas"] = dados.get(
        "number_of_seasons"
    )


    dorama["episodios"] = dados.get(
        "number_of_episodes"
    )


    dorama["status"] = dados.get(
        "status",
        "Não informado"
    )


    dorama["pais"] = ", ".join(

        dados.get(
            "origin_country",
            []
        )

    ) or "Não informado"


    return render_template(

        "doramainfo.html",

        dorama=dorama

    )


@routes.route("/api-doramas")
def api_doramas():

    resposta = api_listar_doramas()


    if isinstance(
        resposta,
        tuple
    ):

        dados = resposta[0]

    else:

        dados = resposta


    return render_template(

        "apidoramas.html",

        doramas=dados.get(
            "doramas",
            []
        )

    )