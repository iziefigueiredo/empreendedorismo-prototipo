from PIL import Image, ImageDraw
import random
from pathlib import Path

fotos_dir = Path('app/static/fotos_fake')
fotos_dir.mkdir(parents=True, exist_ok=True)

def gerar_foto_crianca(nome_arquivo, sexo='F'):
    """Gera um desenho melhor de uma criança."""

    img = Image.new('RGB', (250, 250), color='#F5F5F5')
    draw = ImageDraw.Draw(img)

    # Cores
    cores_pele = ['#FFD1B3', '#E8B8A0', '#D4A574', '#C19A6B']
    cores_cabelo = ['#8B6914', '#654321', '#5C4033', '#3E2723'] if sexo == 'M' else ['#8B6914', '#D4A574', '#A0826D', '#8B4513']

    cor_pele = random.choice(cores_pele)
    cor_cabelo = random.choice(cores_cabelo)

    # Desenhar cabeça (círculo maior)
    draw.ellipse([50, 30, 200, 180], fill=cor_pele, outline='#999', width=2)

    # Desenhar cabelo
    if sexo == 'F':
        # Cabelo comprido em volta da cabeça
        draw.ellipse([40, 20, 210, 160], fill=cor_cabelo, outline=None)
        # Alguns detalhes de cabelo
        draw.arc([45, 25, 205, 155], 0, 180, fill='#5C4033', width=2)
    else:
        # Cabelo curto
        draw.ellipse([50, 25, 200, 135], fill=cor_cabelo, outline=None)

    # Desenhar olhos (maiores e com mais detalhes)
    # Olho esquerdo
    draw.ellipse([80, 80, 110, 110], fill='white', outline='#333', width=1)
    draw.ellipse([85, 88, 105, 102], fill='#4A90E2', outline='#333', width=1)
    draw.ellipse([88, 91, 100, 99], fill='black', outline=None)
    draw.ellipse([91, 94, 95, 97], fill='white', outline=None)  # brilho

    # Olho direito
    draw.ellipse([140, 80, 170, 110], fill='white', outline='#333', width=1)
    draw.ellipse([145, 88, 165, 102], fill='#4A90E2', outline='#333', width=1)
    draw.ellipse([148, 91, 160, 99], fill='black', outline=None)
    draw.ellipse([151, 94, 155, 97], fill='white', outline=None)  # brilho

    # Sobrancelhas
    draw.line([75, 75, 105, 70], fill='#333', width=2)
    draw.line([145, 70, 175, 75], fill='#333', width=2)

    # Nariz (simples)
    draw.line([125, 90, 125, 120], fill='#999', width=2)
    draw.line([120, 118, 130, 118], fill='#999', width=1)

    # Boca (sorriso)
    draw.arc([100, 120, 150, 145], 0, 180, fill='#E74C3C', width=3)

    # Orelhas
    draw.ellipse([40, 90, 55, 125], fill=cor_pele, outline='#999', width=1)
    draw.ellipse([195, 90, 210, 125], fill=cor_pele, outline='#999', width=1)

    # Pescoço
    draw.rectangle([110, 175, 140, 200], fill=cor_pele, outline=None)

    # Corpo (camiseta)
    cor_roupa = random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
    draw.rectangle([60, 200, 190, 240], fill=cor_roupa, outline='#333', width=2)

    # Braços (simples)
    draw.rectangle([40, 205, 60, 230], fill=cor_pele, outline='#999', width=1)
    draw.rectangle([190, 205, 210, 230], fill=cor_pele, outline='#999', width=1)

    # Salvar
    caminho = fotos_dir / nome_arquivo
    img.save(caminho)
    return str(caminho)

# Gerar 100 fotos
sexos = ['F'] * 50 + ['M'] * 50
for i in range(100):
    sexo = sexos[i]
    nome = f'crianca_{i+1:03d}.png'
    gerar_foto_crianca(nome, sexo)
    if (i + 1) % 10 == 0:
        print(f'✓ {i+1}/100 fotos geradas...')

print(f'\n✓ 100 desenhos melhorados criados!')
