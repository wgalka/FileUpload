import re
import shutil
from datetime import datetime
import os

import aiofiles
import uvicorn

from utils import convert_size, read_settings, resource_path, saved, danger
from fastapi import FastAPI, Request, UploadFile
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import xml.etree.ElementTree as ET

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=resource_path("templates"))


@app.get("/myip")
async def myip(request: Request):
    return request.client.host

@app.get("/")
async def index(request: Request):
    print(request.__dict__)
    return templates.TemplateResponse("index.html", {"request": request, "abc": "abc"})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/fileupload")
async def upload_file(file: UploadFile, request: Request):
    now = datetime.now()
    minutes = now.hour * 60 + now.minute

    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    mb_size = int(size / 1048576)
    file.file.seek(0, 0)
    path = "upload/" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "/"
    try:
        os.mkdir(path)
    except:
        pass

    filetypes, filename, filesize_limit, startstop = read_settings()
    print(filename, file.filename, bool(re.match(filename, file.filename)))
    ok_filename = bool(re.match(filename, file.filename))
    ok_size = mb_size <= filesize_limit
    ok_date = ((startstop[0] <= minutes) and (minutes <= startstop[1]))
    ok_type = file.content_type in filetypes
    ok_saved = False

    print(ok_date, startstop[0], minutes, startstop[1], now.hour, (startstop[0] <= minutes), (minutes <= startstop[1]))

    if ok_type and ok_date and ok_filename and ok_size:
        newpath = path + request.client.host + "/"
        if os.path.isdir(newpath):
            pass
        elif request.client.host == "":
            newpath = path + "unknown/"
            os.mkdir(newpath)
        else:
            os.mkdir(newpath)

        # TODO Jeśli ktoś przesyła drugi raz ten sam plik chcemy zachować tą kopię
        full_path = newpath + file.filename
        if os.path.isfile(full_path):
            time = now.strftime("__%H_%M_%S")
            full_path += time


        async with aiofiles.open(full_path, 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
        ok_saved = True

    return templates.TemplateResponse("upload.html",
                                      {'request': request, "ok_saved": danger(ok_saved), "saved": saved(ok_saved),
                                       "filename": file.filename, "ok_filename": danger(ok_filename),
                                       "filesize_limit": convert_size(size), "file_limit": filesize_limit, "ok_size": danger(ok_size),
                                       "uploadtime": now.strftime("%H:%M"), "ok_date": danger(ok_date),
                                       "filetype": file.content_type, "ok_type": danger(ok_type)})
    # return {"host": request.client.host}


if __name__ == "__main__":
    if not os.path.exists("settings.xml"):
        f = open("settings.xml", "+w", encoding="utf-8")
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n\
<settings>\n\
\t<!--  Akceptowane formaty plików, może być kilka  -->\n\
\t<filetype>application/x-zip-compressed</filetype>\n\
\t<!-- Rozmiar pliku wyrażony w mb -->\n\
\t<filesize>10</filesize>\n\
\t<starthour>21:00</starthour>\n\
\t<stophour>24:00</stophour>\n\
\t<!--  wyrażenie regularne do sprawdzenia poprawności nazwy pliku  -->\n\
\t<nameregex>[a-z]{2}[a-z]{2}[0-9]{6}</nameregex>\n\
</settings>')
        f.close()

    config = uvicorn.Config(app, host='0.0.0.0', port=8000, log_level="info")
    server = uvicorn.Server(config)
    print("http://localhost:8000/myip")
    server.run()
