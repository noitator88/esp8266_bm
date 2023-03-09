import uasyncio as asyncio
from nanoweb import Nanoweb, send_file

WWW_DIR = './www/'

async def api_status(request):
    """API status endpoint"""
    await request.write("HTTP/1.1 200 OK\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    await request.write('{"status": "running"}')

naw = Nanoweb()

# Declare route directly with decorator
@naw.route("/ping")
def ping(request):
    await request.write("HTTP/1.1 200 OK\r\n\r\n")
    await request.write("pong")

async def index(request):
    await request.write(b"HTTP/1.1 200 Ok\r\n\r\n")

    await send_file(
        request,
        './%s/index.html' % WWW_DIR,
    )

# Declare route from a dict
naw.routes = {
    '/': index,
    '/api/status': api_status,
}

loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()