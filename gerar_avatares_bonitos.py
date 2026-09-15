from PIL import Image, ImageDraw
import random
from pathlib import Path

fotos_dir = Path('app/static/fotos_fake')
fotos_dir.mkdir(parents=True, exist_ok=True)

def gerar_avatar(nome_arquivo, sexo='F'):
    """Gera avatares bonitos estilo ilustrado."""

    img = Image.new('RGB', (256, 256), color='#F5F7FA')
    draw = ImageDraw.Draw(img)

    # Cores disponíveis
    peles = ['#FDBCB4', '#F0AD69', '#D99E7E', '#EDBAA6', '#F4C4AE']
    cabelos_f = ['#8B5A3C', '#C19A6B', '#D4AF37', '#A0826D', '#654321']
    cabelos_m = ['#654321', '#5C4033', '#3E2723', '#8B6F47', '#6B4423']
    olhos = ['#4A90E2', '#8B7355', '#654321', '#3E8E7E', '#8B4513']
    roupas = ['#FF6B9D', '#C44569', '#4ECDC4', '#44AF69', '#F7DC6F', '#BB8FCE', '#85C1E2']

    cor_pele = random.choice(peles)
    cor_cabelo = random.choice(cabelos_f if sexo == 'F' else cabelos_m)
    cor_olho = random.choice(olhos)
    cor_roupa = random.choice(roupas)

    # Cabeça - grande e limpa
    draw.ellipse([60, 30, 196, 155], fill=cor_pele, outline='#E8C4A0', width=1)

    # Cabelo
    if sexo == 'F':
        # Cabelo comprido
        draw.ellipse([50, 20, 206, 140], fill=cor_cabelo, outline=None)
        # Franja
        draw.polygon([(70, 50), (100, 40), (130, 45), (160, 50), (180, 60), (190, 80), (50, 80)], fill=cor_cabelo)
    else:
        # Cabelo curto/moderno
        draw.ellipse([60, 25, 196, 130], fill=cor_cabelo, outline=None)

    # Rosto em formato mais suave
    draw.ellipse([70, 50, 186, 150], fill=cor_pele, outline=None)

    # Olhos - simples e bonitos
    # Esquerdo
    draw.ellipse([95, 85, 115, 100], fill='white', outline='#DDD', width=1)
    draw.ellipse([98, 88, 112, 98], fill=cor_olho, outline=None)
    draw.ellipse([105, 92, 110, 96], fill='black', outline=None)
    draw.ellipse([107, 91, 109, 93], fill='white', outline=None)

    # Direito
    draw.ellipse([141, 85, 161, 100], fill='white', outline='#DDD', width=1)
    draw.ellipse([144, 88, 158, 98], fill=cor_olho, outline=None)
    draw.ellipse([151, 92, 156, 96], fill='black', outline=None)
    draw.ellipse([153, 91, 155, 93], fill='white', outline=None)

    # Sobrancelhas suaves
    draw.arc([93, 80, 118, 90], 0, 180, fill=cor_cabelo, width=2)
    draw.arc([138, 80, 163, 90], 0, 180, fill=cor_cabelo, width=2)

    # Nariz simples (2 pontos)
    draw.ellipse([125, 105, 131, 115], fill=cor_pele, outline='#E8C4A0', width=1)

    # Boca sorridente
    draw.arc([110, 115, 146, 135], 0, 180, fill='#E75480', width=3)

    # Bochechas rosadas
    draw.ellipse([75, 105, 90, 120], fill='#FFB6C1', outline=None)
    draw.ellipse([166, 105, 181, 120], fill='#FFB6C1', outline=None)

    # Pescoço
    draw.rectangle([115, 145, 141, 160], fill=cor_pele, outline=None)

    # Corpo - Camiseta
    draw.rectangle([50, 160, 206, 240], fill=cor_roupa, outline='#999', width=2)

    # Gola
    draw.ellipse([105, 155, 151, 175], fill=cor_roupa, outline='#999', width=1)

    # Braços
    draw.ellipse([35, 170, 55, 220], fill=cor_pele, outline='#E8C4A0', width=1)
    draw.ellipse([201, 170, 221, 220], fill=cor_pele, outline='#E8C4A0', width=1)

    # Detalhes na camiseta
    if random.random() > 0.5:
        # Bolsinho
        draw.rectangle([110, 185, 146, 205], fill='#FFF', outline='#999', width=1)

    # Salvar
    caminho = fotos_dir / nome_arquivo
    img.save(caminho)
    return str(caminho)

# Gerar 100 avatares
sexos = ['F'] * 50 + ['M'] * 50
for i in range(100):
    sexo = sexos[i]
    nome = f'crianca_{i+1:03d}.png'
    gerar_avatar(nome, sexo)
    if (i + 1) % 10 == 0:
        print(f'✓ {i+1}/100 avatares gerados...')

print(f'\n✓ 100 avatares bonitos criados!')
