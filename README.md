# Visualizador de Imagens com Filtros - Python + PySimpleGUI + OpenCV

## Introdução

Este projeto tem como objetivo a criação de um visualizador de imagens com capacidade de aplicar múltiplos filtros e transformações de maneira interativa. Desenvolvido em Python com as bibliotecas OpenCV, PySimpleGUI e PIL (Pillow), o sistema permite que o usuário carregue uma imagem do seu computador, visualize simultaneamente a versão original e a modificada, aplique diferentes efeitos visuais e, por fim, salve a imagem resultante em um novo arquivo.

A proposta une fundamentos de visão computacional com usabilidade prática, demonstrando como combinar interface gráfica e processamento de imagem para desenvolver aplicações acessíveis e completas.

## Demonstração em Vídeo

Você pode assistir à explicação completa do projeto neste vídeo: [🔗 Link para o vídeo no Google Drive](https://drive.google.com/file/d/1qH6gWZpbNj1uJq8aouTfVEy5GcxRA-Z_/view?usp=sharing)

## Funcionalidades

* Carregamento de imagens com suporte a formatos JPG, PNG e JPEG;
* Interface gráfica local responsiva, com rolagem e suporte a tela cheia;
* Exibição lado a lado da imagem original e da imagem modificada;
* Aplicação acumulativa de múltiplos filtros e transformações visuais;
* Salvamento da imagem final em novo arquivo escolhido pelo usuário;
* Tratamento de erros para arquivos inválidos ou ações inválidas.

## Filtros disponíveis

* Escala de Cinza
* Inversão de Cores
* Aumento de Contraste (CLAHE)
* Desfoque Gaussiano
* Nitidez (Filtro de realce)
* Detecção de Bordas (Canny)
* Sépia (tom retrô)
* Ajuste de Brilho (+/-)

## Transformações disponíveis

* Rotação (90 graus)
* Redimensionamento (50%)
* Espelhamento Horizontal
* Espelhamento Vertical

## Tecnologias Utilizadas

* **Python 3.8+**
* **OpenCV**: para processamento e manipulação de imagens
* **PySimpleGUI**: para construção da interface gráfica local
* **Pillow (PIL)**: para conversão de imagens e compatibilidade com GUI

## Tratamento de Erros

O sistema foi desenvolvido com foco em robustez, incluindo tratamento para os seguintes tipos de erro:

* **Carregamento de imagens inválidas**: se o usuário tentar abrir um arquivo corrompido ou em formato não suportado, uma mensagem de erro é exibida;
* **Tentativa de aplicar filtro sem imagem carregada**: impede ações sem contexto válido, garantindo estabilidade;
* **Erro na hora de salvar**: falhas ao salvar a imagem são capturadas e comunicadas claramente ao usuário, evitando encerramentos inesperados do programa;
* **Conversões de formatos**: o código trata diferenças entre imagens em escala de cinza, RGB e RGBA, evitando erros nas transformações.

## Como Executar

1. Certifique-se de ter Python 3 instalado;
2. Instale as dependências com o comando:

   ```bash
   pip install numpy opencv-python pillow PySimpleGUI 
   ```
3. Execute o script principal:

   ```bash
   python visualizador.py
   ```

## Conclusão

Este visualizador de imagens é uma aplicação didática que integra conhecimentos de interface gráfica, manipulação de imagens e controle de fluxo de eventos. Ele atende aos principais requisitos de usabilidade e modularidade, sendo uma ótima base para projetos maiores de edição ou análise visual. Além disso, serve como excelente exercício prático para quem deseja aprofundar suas habilidades com PySimpleGUI e OpenCV.
