from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse
from utils import *

import aiofiles
import uuid
app = FastAPI()


# ● /image: Uma requisição POST que recebe um multipart/form-data com uma imagem bitmap e retorna a
# identificação única do arquivo armazenado em um diretório temporário do servidor;
@app.post('/image')
async def post_image(file: UploadFile = File(...)):
    img = await file.read()
    name = uuid.uuid4().hex
    async with aiofiles.open(f"images/{name}.bmp", "wb") as f:
        await f.write(img)
    return {"uuid": name}


# ● /image: Uma requisição GET que recebe na query a identificação da
# imagem pós processada a ser acessada e retorna o arquivo para download;
@app.get('/image/{uuid}')
async def get_image(uuid: str):
    file_location = f"images/{uuid}.bmp"

    return FileResponse(file_location, media_type="application/octet-stream")


# ● /encode: Uma requisição POST que recebe um application/json com a identificação da imagem (gerada
# após o upload para o servidor), aplica um algoritmo de Esteganografia (será descrito melhor abaixo)
# retornando um JSON informando a identificação da imagem do novo arquivo gerado;
@app.post('/encode')
async def post_encode(_uuid: str, msg: str):
    image = f"images/{_uuid}.bmp"

    with open(image, 'rb') as file:
        bmp = file.read()

    offset = bmp[10]

    bmp_array = bytearray(bmp)

    msg = msg + '.'
    bits = []
    for i in range(len(msg)):
        for j in range(7, -1, -1):
            bits.append(nth_bit_present(bytearray(msg, 'utf-8')[i], j))

    if (len(bits) >= len(bmp_array) + offset):
        return {"uu"}

    for i in range(len(bits)):
        bmp_array[i + offset] = set_lsb(bmp_array[i + offset], bits[i])

    name = uuid.uuid4().hex
    async with aiofiles.open(f"images/{name}.bmp", "wb") as f:
        await f.write(bmp_array)

    return {"uuid": name}


# ● /decode: Uma requisição GET que recebe na query a identificação do arquivo de imagem a ser
# decodificada e retorna a mensagem escondida na imagem;
@app.get('/decode')
async def get_decode(_uuid: str):

    image = f"images/{_uuid}.bmp"

    with open(image, 'rb') as bmp_file:
        bmp = bmp_file.read()

    offset = bmp[10]

    bits = []
    for i in range(offset, len(bmp)):
        bits.append(nth_bit_present(bmp[i], 0))

    out_bytes = []
    for i in range(0, len(bits), 8):
        if (len(bits) - i > 8):
            out_bytes.append(bits_to_byte(bits[i:i+8]))

    out = []
    for b in out_bytes:
        if chr(b) == ".":
            break
        out.append(chr(b))


    return {"msg": ''.join(out)}
