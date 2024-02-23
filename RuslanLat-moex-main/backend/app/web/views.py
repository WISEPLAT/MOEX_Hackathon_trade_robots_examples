from aiohttp.web import Response


async def index(request):
    return Response(
        text="""<h1>GO.ALGO</h1> 
        <p>Cервис по построению торговых решений на основе данных AlgoPack</p> 
        <a href='/docs'>Документация GO.ALGO API</a>""",
        content_type="text/html",
    )