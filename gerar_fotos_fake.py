from PIL import Image, ImageDraw
import os
from pathlib import Path

# Criar pasta para armazenar as fotos fake
fotos_dir = Path('app/static/fotos_fake')
fotos_dir.mkdir(parents=True, exist_ok=True)

def gerar_foto_fake(nome_arquivo, sexo='F'):
    """Gera uma foto fake simples (desenho) de uma criança."""

    # Criar imagem branca 200x200
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)

    # Cores baseadas no sexo
    cor_pele = '#FFD4A3' if sexo == 'F' else '#E5B89E'
    cor_cabelo = '#D4A574' if sexo == 'F' else '#8B4513'
    cor_olhos = '#4A90E2'

    # Desenhar cabeça (círculo)
    draw.ellipse([50, 30, 150, 130], fill=cor_pele, outline='black', width=2)

    # Desenhar cabelo
    if sexo == 'F':
        draw.ellipse([40, 20, 160, 110], fill=cor_cabelo, outline=None)
    else:
        draw.ellipse([50, 20, 150, 100], fill=cor_cabelo, outline=None)

    # Desenhar olhos
    draw.ellipse([75, 60, 85, 70], fill=cor_olhos, outline='black', width=1)
    draw.ellipse([115, 60, 125, 70], fill=cor_olhos, outline='black', width=1)

    # Desenhar boca (simples)
    draw.arc([80, 75, 120, 95], 0, 180, fill='black', width=2)

    # Desenhar corpo (retângulo)
    draw.rectangle([70, 130, 130, 180], fill='#FF6B6B', outline='black', width=2)

    # Salvar imagem
    caminho = fotos_dir / nome_arquivo
    img.save(caminho)
    return str(caminho)

# Gerar 100 fotos fake
sexos = ['F'] * 50 + ['M'] * 50
for i in range(100):
    sexo = sexos[i]
    nome = f'crianca_{i+1:03d}.png'
    caminho = gerar_foto_fake(nome, sexo)
    if (i + 1) % 10 == 0:
        print(f'✓ {i+1}/100 fotos criadas...')

print(f'\n✓ Total: 100 fotos fake geradas em {fotos_dir}/')
