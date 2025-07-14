# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re, math, logging, secrets, mimetypes, time
from info import *
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from plugins.start import decode, encode 
from datetime import datetime
from plugins.database import record_visit, get_count
from TechVJ.bot import multi_clients, work_loads, TechVJBot
from TechVJ.server.exceptions import FIleNotFound, InvalidHash
from TechVJ import StartTime, __version__
from TechVJ.util.custom_dl import ByteStreamer
from TechVJ.util.time_format import get_readable_time
from TechVJ.util.render_template import render_page
from TechVJ.util.file_properties import get_file_ids

routes = web.RouteTableDef()

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Warrior Units - Site and Bot is Live</title>
    <style>
        /* Basic reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body, html {
            height: 100%;
            font-family: 'Courier New', Courier, monospace;
            background: black;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        /* Main content container */
        .container {
            text-align: center;
            z-index: 1;
        }

        /* Animating text appearance */
        @keyframes glitch {
            0% {
                text-shadow: 2px 2px #00ff00, -2px -2px #00ff00;
            }
            20% {
                text-shadow: 2px -2px #ff00ff, -2px 2px #00ff00;
            }
            40% {
                text-shadow: -2px 2px #00ff00, 2px -2px #ff00ff;
            }
            60% {
                text-shadow: 2px 2px #ff00ff, -2px -2px #00ff00;
            }
            80% {
                text-shadow: -2px -2px #ff00ff, 2px 2px #00ff00;
            }
            100% {
                text-shadow: 2px 2px #00ff00, -2px -2px #00ff00;
            }
        }

        /* Styling for the welcome text */
        .team-spy {
            font-size: 3rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 5px;
            background: linear-gradient(90deg, #ff6a00, #ee0979, #8e44ad, #3498db, #f4d03f);
            background-size: 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.6);
            animation: glitch 1.5s infinite;
        }

        .bot-status {
            margin-top: 15px;
            font-size: 1.2rem;
            font-weight: 600;
            letter-spacing: 2px;
            color: #00ffab;
            text-shadow: 0 0 10px #00ffab, 0 0 20px #00ffab;
        }

        .actions {
            margin-top: 20px;
        }

        .btn {
            display: inline-block;
            padding: 12px 25px;
            font-size: 1rem;
            font-weight: 600;
            color: white;
            text-transform: uppercase;
            text-decoration: none;
            border-radius: 30px;
            background: linear-gradient(90deg, #6a11cb, #2575fc);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            background: linear-gradient(90deg, #2575fc, #6a11cb);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .team-spy {
                font-size: 2.5rem;
            }

            .bot-status {
                font-size: 1rem;
            }

            .btn {
                padding: 10px 20px;
                font-size: 0.9rem;
            }
        }

        @media (min-width: 1200px) {
            .team-spy {
                font-size: 4rem;
            }
        }
    </style>
</head>
<body>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1162417600616917"
     crossorigin="anonymous"></script>
<!-- Player Home 1 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-1162417600616917"
     data-ad-slot="6504990098"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    <!-- Main Content -->
    <div class="container">
        <div class="team-spy">Warrior Units Bots</div>
        <div class="bot-status">⚡ Site And Bot is Live ⚡</div>

        <div class="actions">
            <a href="https://t.me/WarriorUnitsBots" class="btn">Join Us</a>
            <a href="https://telegram.me/oo7jatji" class="btn">Contact Me</a>
        </div>
    </div>
</body>
</html>
"""

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text=html_content, content_type='text/html')

@routes.get(r"/{path}/{user_path}/{second}/{third}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        user_path = request.match_info["user_path"]
        sec = request.match_info["second"]
        th = request.match_info["third"]
        id = int(await decode(path))
        user_id = int(await decode(user_path))
        secid = int(await decode(sec))
        thid = int(await decode(th))
        return web.Response(text=await render_page(id, user_id, secid, thid), content_type='text/html')
    except Exception as e:
        return web.Response(text=html_content, content_type='text/html')
    return 

@routes.post('/click-counter')
async def handle_click(request):
    data = await request.json()  # Get the JSON body
    user_id = int(data.get('user_id'))  # Extract user_id from the request
    today = datetime.now().strftime('%Y-%m-%d')

    user_agent = request.headers.get('User-Agent')
    is_chrome = "Chrome" in user_agent or "Google Inc" in user_agent

    if is_chrome:
        visited_cookie = request.cookies.get('visited')
    else:
        return

    if visited_cookie == today:
        return
    else:
        response = web.Response(text="Hello, World!")
        response.set_cookie('visited', today, max_age=24*60*60)
        u = get_count(user_id)
        if u:
            c = int(u + 1)
            record_visit(user_id, c)
        else:
            c = int(1)
            record_visit(user_id, c)
        return response

@routes.get('/{short_link}', allow_head=True)
async def get_original(request: web.Request):
    short_link = request.match_info["short_link"]
    original = await decode(short_link)
    if original:
        link = f"{STREAM_URL}link?{original}"
        raise web.HTTPFound(link)  # Redirect to the constructed link 
    else:
        return web.Response(text=html_content, content_type='text/html')

@routes.get('/link', allow_head=True)
async def visits(request: web.Request):
    user = request.query.get('u')
    watch = request.query.get('w')
    second = request.query.get('s')
    third = request.query.get('t')
    data = await encode(watch)
    user_id = await encode(user)
    sec_id = await encode(second)
    th_id = await encode(third)
    link = f"{STREAM_URL}{data}/{user_id}/{sec_id}/{th_id}"
    raise web.HTTPFound(link)  # Redirect to the constructed link

@routes.get(r"/dl/{path:\S+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        match = re.search(r"^([a-zA-Z0-9_-]{6})(\d+)$", path)
        if match:
            secure_hash = match.group(1)
            id = int(match.group(2))
        else:
            id = int(re.search(r"(\d+)(?:\/\S+)?", path).group(1))
            secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))

class_cache = {}

async def media_streamer(request: web.Request, id: int, secure_hash: str):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(id)
    logging.debug("after calling get_file_properties")
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type = mimetypes.guess_type(file_id.file_name)
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
