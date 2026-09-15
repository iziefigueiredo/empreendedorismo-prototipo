from PIL import Image, ImageDraw
import random
from pathlib import Path

fotos_dir = Path('app/static/fotos_fake')
fotos_dir.mkdir(parents=True, exist_ok=True)

def gerar_foto_crianca(nome_arquivo, sexo='F'):
    """Gera um desenho melhorado de uma criança."""

    img = Image.new('RGB', (300, 300), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Paleta de cores realista
    peles = ['#F5D5B8', '#E8C4A0', '#D4A574', '#C19A6B', '#B8956A']
    cabelos_f = ['#D4A574', '#8B6F47', '#A0826D', '#8B7355', '#6B4423']
    cabelos_m = ['#8B6F47', '#654321', '#5C4033', '#4A3728', '#3E2723']
    roupas = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#FF9FF3', '#54A0FF']

    cor_pele = random.choice(peles)
    cor_cabelo = random.choice(cabelos_f if sexo == 'F' else cabelos_m)
    cor_roupa = random.choice(roupas)

    # Fundo com gradiente suave (simulado com retângulos)
    for i in range(300):
        cor_gradiente = max(0, min(255, int(255 - (i * 0.15))))
        cor_b = max(0, min(255, cor_gradiente + 20))
        cor = (cor_gradiente, cor_gradiente, cor_b)
        draw.line([(0, i), (300, i)], fill=cor)

    # Cabeça - círculo maior e melhor proporcionado
    cabeça_bbox = [80, 40, 220, 170]
    draw.ellipse(cabeça_bbox, fill=cor_pele, outline='#D4C5B9', width=2)

    # Cabelo - desenho melhor
    if sexo == 'F':
        # Cabelo comprido com mais volume
        draw.ellipse([75, 30, 225, 160], fill=cor_cabelo, outline=None)
        # Detalhes de cabelo
        draw.arc([70, 25, 230, 165], 0, 180, fill='#8B7355', width=2)
        draw.arc([75, 35, 225, 150], 180, 360, fill=cor_cabelo, width=2)
    else:
        # Cabelo curto
        draw.ellipse([80, 35, 220, 140], fill=cor_cabelo, outline=None)
        # Textura de cabelo
        for x in range(90, 210, 15):
            draw.line([(x, 50), (x, 130)], fill='#5C4033', width=1)

    # Olhos - desenho mais realista
    # Branco dos olhos
    draw.ellipse([105, 90, 135, 115], fill='white', outline='#333', width=2)
    draw.ellipse([165, 90, 195, 115], fill='white', outline='#333', width=2)

    # Íris
    draw.ellipse([110, 95, 130, 110], fill='#4A90E2', outline='#333', width=1)
    draw.ellipse([170, 95, 190, 110], fill='#4A90E2', outline='#333', width=1)

    # Pupila
    draw.ellipse([115, 100, 125, 108], fill='black', outline=None)
    draw.ellipse([175, 100, 185, 108], fill='black', outline=None)

    # Brilho nos olhos
    draw.ellipse([118, 102, 123, 106], fill='white', outline=None)
    draw.ellipse([178, 102, 183, 106], fill='white', outline=None)

    # Sobrancelhas
    draw.arc([100, 85, 140, 100], 0, 180, fill='#5C4033', width=3)
    draw.arc([160, 85, 200, 100], 0, 180, fill='#5C4033', width=3)

    # Nariz
    draw.line([150, 100, 150, 130], fill='#D4A574', width=2)
    draw.line([145, 128, 155, 128], fill='#D4A574', width=2)

    # Boca - sorriso
    draw.arc([125, 130, 175, 155], 0, 180, fill='#E74C3C', width=3)

    # Orelhas
    draw.ellipse([60, 95, 80, 130], fill=cor_pele, outline='#D4C5B9', width=2)
    draw.ellipse([220, 95, 240, 130], fill=cor_pele, outline='#D4C5B9', width=2)

    # Pescoço
    draw.rectangle([130, 165, 170, 185], fill=cor_pele, outline=None)

    # Corpo - camiseta
    draw.rectangle([70, 185, 230, 260], fill=cor_roupa, outline='#333', width=2)

    # Detalhes da camiseta (gola redonda)
    draw.arc([135, 180, 165, 200], 180, 360, fill=cor_roupa, width=2)

    # Botão/detalhe central
    draw.ellipse([143, 210, 157, 225], fill='#FFF', outline='#999', width=1)

    # Braços
    draw.rectangle([40, 190, 70, 225], fill=cor_pele, outline='#D4C5B9', width=1)
    draw.rectangle([230, 190, 260, 225], fill=cor_pele, outline='#D4C5B9', width=1)

    # Mãos
    draw.ellipse([35, 220, 75, 245], fill=cor_pele, outline='#D4C5B9', width=1)
    draw.ellipse([225, 220, 265, 245], fill=cor_pele, outline='#D4C5B9', width=1)

    # Salvar
    caminho = fotos_dir / nome_arquivo
    img.save(caminho)
    return str(caminho)

# Gerar 100 fotos melhoradas
sexos = ['F'] * 50 + ['M'] * 50
for i in range(100):
    sexo = sexos[i]
    nome = f'crianca_{i+1:03d}.png'
    gerar_foto_crianca(nome, sexo)
    if (i + 1) % 10 == 0:
        print(f'✓ {i+1}/100 fotos geradas...')

print(f'\n✓ 100 desenhos profissionais criados!')
