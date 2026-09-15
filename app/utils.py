import os
import io
import re
import unicodedata
import cloudinary
import cloudinary.uploader
from PIL import Image, ImageOps
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def slugify(texto):
    """Transforma 'João da Silva' em 'joao-da-silva'."""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    texto = re.sub(r'[^\w\s-]', '', texto).strip().lower()
    return re.sub(r'[-\s]+', '-', texto)

def comprimir_e_enviar(arquivo, pasta='osgade', nome_arquivo=None):
    """Comprime a imagem e envia para o Cloudinary. Retorna a URL."""

    if os.getenv('CLOUDINARY_API_KEY') in (None, '', 'local'):
        return None

    img = Image.open(arquivo)
    img = ImageOps.exif_transpose(img)  # corrige fotos "deitadas" tiradas com celular

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    max_px = 1200
    if max(img.size) > max_px:
        img.thumbnail((max_px, max_px), Image.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=75, optimize=True)
    buffer.seek(0)

    opcoes = {'folder': pasta, 'resource_type': 'image'}
    if nome_arquivo:
        opcoes['public_id'] = slugify(nome_arquivo)
        opcoes['overwrite'] = True

    resultado = cloudinary.uploader.upload(buffer, **opcoes)

    return resultado['secure_url']

import urllib.request

def girar_imagem_cloudinary(url):
    """Baixa a imagem, gira 90° de verdade (nos pixels) e reenvia pro Cloudinary, no mesmo lugar."""
    try:
        with urllib.request.urlopen(url) as resposta:
            dados = resposta.read()
    except Exception:
        return None

    img = Image.open(io.BytesIO(dados))
    img = img.rotate(-90, expand=True)

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85, optimize=True)
    buffer.seek(0)

    # extrai o "nome" do arquivo no Cloudinary a partir do link
    caminho = url.split('/upload/')[1]
    caminho = caminho.split('/', 1)[1]  # remove a versão (ex: v1234567)
    public_id = caminho.rsplit('.', 1)[0]  # remove a extensão (.jpg)

    resultado = cloudinary.uploader.upload(
        buffer, public_id=public_id, overwrite=True, resource_type='image'
    )
    return resultado['secure_url']