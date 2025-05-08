import PySimpleGUI as sg # Importa a biblioteca PySimpleGUI para criar interfaces gráficas
import cv2 # Importa a biblioteca OpenCV para manipulação de imagens
import numpy as np # Importa a biblioteca NumPy para operações numéricas
from PIL import Image # Importa a biblioteca PIL (Pillow) para manipulação de imagens
import io # Importa a biblioteca io para manipulação de fluxo de entrada/saída

# ---------------- Funções de Filtros ----------------

# Converte para escala de cinza ou reforça se já for cinza
def aplicar_escala_cinza(img):
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        return cv2.equalizeHist(img)

# Inverte as cores da imagem
def aplicar_inversao(img):
    return cv2.bitwise_not(img)

# Aplica CLAHE para melhorar o contraste
def aplicar_contraste(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

# Aplica desfoque gaussiano
def aplicar_desfoque(img):
    return cv2.GaussianBlur(img, (7, 7), 0)

# Realça nitidez da imagem
def aplicar_nitidez(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)

# Detecta bordas com algoritmo Canny
def aplicar_bordas(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(img, 50, 150)

# Rotaciona a imagem em um dado ângulo
def aplicar_rotacao(img, angulo):
    h, w = img.shape[:2]
    centro = (w // 2, h // 2)
    matriz = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    return cv2.warpAffine(img, matriz, (w, h))

# Redimensiona a imagem com base na escala
def aplicar_redimensionamento(img, escala):
    largura = int(img.shape[1] * escala)
    altura = int(img.shape[0] * escala)
    return cv2.resize(img, (largura, altura))

# Espelhamento horizontal
def aplicar_espelhamento_horizontal(img):
    return cv2.flip(img, 1)

# Espelhamento vertical
def aplicar_espelhamento_vertical(img):
    return cv2.flip(img, 0)

# Aplica efeito sépia (retrô)
def aplicar_sepia(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_sepia = np.array(img, dtype=np.float64)
    img_sepia = cv2.transform(img_sepia, np.matrix([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ]))
    img_sepia[np.where(img_sepia > 255)] = 255
    return np.array(img_sepia, dtype=np.uint8)

# Ajusta brilho positivo ou negativo
def aplicar_brilho(img, valor=30):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - abs(valor)
    if valor > 0:
        v[v > lim] = 255
        v[v <= lim] += valor
    else:
        v[v < abs(valor)] = 0
        v[v >= abs(valor)] -= abs(valor)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

# ---------------- Utilitários ----------------

# Converte PIL Image para bytes para exibir no PySimpleGUI
def ImageToData(im):
    with io.BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

# Converte imagem OpenCV para formato exibível no PySimpleGUI
def exibir_imagem(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imagem_pil = Image.fromarray(img)
    imagem_pil.thumbnail((400, 400))
    return ImageToData(imagem_pil)

# ---------------- Layout ----------------
layout = [
    [sg.Text("Visualizador de Imagens com Filtros", size=(40, 1), font=("Helvetica", 16))],
    [
        sg.Column([
            [sg.Text("Imagem Original", justification='center', size=(40,1), font=('Helvetica', 12))],
            [sg.Image(key='-ORIGINAL-')]
        ]),
        sg.Column([
            [sg.Text("Imagem Modificada", justification='center', size=(40,1), font=('Helvetica', 12))],
            [sg.Image(key='-MODIFICADA-')]
        ])
    ],
    [sg.Button("Carregar Imagem"), sg.Button("Salvar Imagem")],
    [sg.Button("Escala de Cinza"), sg.Button("Inversão de Cores"), sg.Button("Contraste"), sg.Button("Sépia")],
    [sg.Button("Desfoque"), sg.Button("Nitidez"), sg.Button("Detecção de Bordas"), sg.Button("Brilho +"), sg.Button("Brilho -")],
    [sg.Button("Rotacionar 90°"), sg.Button("Redimensionar 50%"), sg.Button("Espelhar H"), sg.Button("Espelhar V")],
    [sg.Button("Resetar"), sg.Button("Sair")]
]

# Janela com suporte a rolagem vertical, em tela cheia
janela = sg.Window(
    "Visualizador de Imagens",
    [[sg.Column(layout, scrollable=True, vertical_scroll_only=True, size=sg.Window.get_screen_size())]],
    location=(0, 0),
    resizable=True,
    finalize=True,
    no_titlebar=False,
    use_custom_titlebar=False
)

img_original = None
img_modificada = None

# ---------------- Lógica ----------------
while True:
    evento, _ = janela.read()
    if evento in (sg.WINDOW_CLOSED, "Sair"):
        break

    # Carrega imagem escolhida pelo usuário
    if evento == "Carregar Imagem":
        caminho = sg.popup_get_file("Escolha uma imagem", file_types=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            img_original = cv2.imread(caminho)
            if img_original is None:
                sg.popup_error("Erro ao carregar a imagem. Verifique o caminho e formato.")
                continue
            img_modificada = img_original.copy()
            janela["-ORIGINAL-"].update(data=exibir_imagem(img_original))
            janela["-MODIFICADA-"].update(data=exibir_imagem(img_modificada))

    # Aplicação de filtros e transformações
    if img_modificada is not None:
        if evento == "Escala de Cinza":
            img_modificada = aplicar_escala_cinza(img_modificada)
        elif evento == "Inversão de Cores":
            img_modificada = aplicar_inversao(img_modificada)
        elif evento == "Contraste":
            img_modificada = aplicar_contraste(img_modificada)
        elif evento == "Sépia":
            img_modificada = aplicar_sepia(img_modificada)
        elif evento == "Desfoque":
            img_modificada = aplicar_desfoque(img_modificada)
        elif evento == "Nitidez":
            img_modificada = aplicar_nitidez(img_modificada)
        elif evento == "Detecção de Bordas":
            img_modificada = aplicar_bordas(img_modificada)
        elif evento == "Brilho +":
            img_modificada = aplicar_brilho(img_modificada, valor=30)
        elif evento == "Brilho -":
            img_modificada = aplicar_brilho(img_modificada, valor=-30)
        elif evento == "Rotacionar 90°":
            img_modificada = aplicar_rotacao(img_modificada, 90)
        elif evento == "Redimensionar 50%":
            img_modificada = aplicar_redimensionamento(img_modificada, 0.5)
        elif evento == "Espelhar H":
            img_modificada = aplicar_espelhamento_horizontal(img_modificada)
        elif evento == "Espelhar V":
            img_modificada = aplicar_espelhamento_vertical(img_modificada)
        elif evento == "Resetar":
            img_modificada = img_original.copy()

        # Atualiza imagem modificada exibida
        janela["-MODIFICADA-"].update(data=exibir_imagem(img_modificada))

    # Salva imagem modificada escolhendo local
    if evento == "Salvar Imagem" and img_modificada is not None:
        caminho = sg.popup_get_file("Salvar imagem como", save_as=True, file_types=[("PNG", "*.png")])
        if caminho:
            try:
                if len(img_modificada.shape) == 2:
                    cv2.imwrite(caminho, img_modificada)
                else:
                    cv2.imwrite(caminho, cv2.cvtColor(img_modificada, cv2.COLOR_RGB2BGR))
                sg.popup("Imagem salva com sucesso!")
            except:
                sg.popup_error("Erro ao salvar a imagem.")

janela.close()