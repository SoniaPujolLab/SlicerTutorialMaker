# Slicer Tutorial Maker

O Slicer Tutorial Maker é uma extensão para o 3D Slicer para agilizar a criação de tutoriais do 3D Slicer em vários idiomas. As seções abaixo fornecem um guia do usuário para a ferramenta.

[English Documentation](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README.md)
[Documentación en español](https://github.com/SoniaPujolLab/SlicerTutorialMaker/blob/main/README_esp.md)

## Instalação (Usando o Gerenciador de Extensões)
- Instale a versão [3D Slicer 5.10.0](https://download.slicer.org/) ou a [versão estável mais recente disponível](https://download.slicer.org/)
- Vá para o "Extension Manager" (Gerenciador de Extensões) e procure por "TutorialMaker".
![TutorialMakenAnnotation](https://github.com/user-attachments/assets/a6060e33-34bd-444c-a230-293c580962ca)
- Clique para reiniciar e carregar a extensão
![image](https://github.com/user-attachments/assets/5b035504-fcc3-42e5-9ae3-2d45615daea7)
- Prossiga para [**Como usar o Tutorial Maker**](#como-usar-o-tutorial-maker)

## Instalação (Manualmente)
Siga estas etapas se quiser obter a versão mais recente da extensão antes da compilação de pré-visualização (que ocorre pela manhã ~9 EST).
### Recomendamos fortemente desabilitar o Modo Desenvolvedor, pois ele usa recursos que estão atualmente em desenvolvimento e podem quebrar durante o uso da extensão.

- Instale a versão estável mais recente do [3D Slicer Stable Release](https://download.slicer.org/) ou a versão de pré-visualização [3D Slicer Preview Release](https://download.slicer.org/)
- Abra o [repositório do Tutorial Maker no GitHub](https://github.com/SlicerLatinAmerica/TutorialMaker)
- Clique no botão verde 'Code' e selecione a opção 'Download ZIP' conforme exibido na imagem abaixo para baixar o arquivo 'TutorialMaker.zip' no seu computador
- Descompacte o arquivo 'TutorialMaker.zip' para acessar o diretório 'TutorialMaker-main'
- **Usuários Windows** :
  1. Inicie o 3D Slicer
  2. Arraste e solte a pasta `TutorialMaker` para a janela do aplicativo Slicer
  3. Uma primeira janela pop-up, 'Select a reader' (Selecionar um leitor), aparece. Selecione 'Add Python scripted modules to the application' (Adicionar módulos de script Python ao aplicativo) e clique em OK.
  4. Uma segunda janela pop-up aparece para carregar o módulo Tutorial Maker. Clique em 'Yes' (Sim).
![TutorialMakerInstall](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/17ffda20-ee58-4e52-91c8-755655725d83)

- **Usuários MacOs**:
   1. Inicie o 3D Slicer
   2. Selecione 'Edit' (Editar) no menu principal
   3. Selecione 'Application settings' (Configurações do aplicativo).
   4. Uma janela 'Parameters' (Parâmetros) aparece: selecione 'Modules' (Módulos) no painel esquerdo
   5. Selecione o arquivo 'TutoriaMaker.py.'
   6. Arraste e solte o arquivo `TutorialMaker.py` localizado no subdiretório 'TutorialMaker-main/TutorialMaker/' no campo 'Additional module paths' (Caminhos adicionais de módulos) e clique em OK para reiniciar o Slicer
![TutorialMakerInstallMac](https://github.com/SlicerLatinAmerica/TutorialMaker/assets/28208639/1aad7764-0eb6-4f2e-8a5e-ba46c3cf373d)


## Como usar o Tutorial Maker

- Selecione o módulo 'Tutorial Maker' da categoria 'Utilities' (Utilitários) na lista de módulos no Slicer
![image](https://github.com/user-attachments/assets/61f70e02-fd7c-4f0b-b2ec-b190021eaf5d)

> [!IMPORTANT]
> Antes de iniciar este tutorial, alterne o Slicer para o modo Tela Cheia e defina o tamanho da fonte para 14pt para garantir que as capturas de tela sejam fáceis de ler.

- Selecione `FourMinuteTutorial`
![image](https://github.com/user-attachments/assets/33bb0de0-24e6-4edc-b807-69f593443dce)

- Clique em `Capture screenshots` (Capturar capturas de tela) e siga as instruções para fechar a cena e fechar o console Python
![image](https://github.com/user-attachments/assets/1eac96d9-150f-416c-ba40-18730ef02ccd)

- Após capturar o tutorial, clique em `Edit annotations` (Editar anotações).
![image](https://github.com/user-attachments/assets/e2d1f02c-e8d6-4620-ade8-cc8dd2d30e30)

## Ferramenta de Anotação

- As capturas de tela aparecerão à esquerda
![image](https://github.com/user-attachments/assets/dcabfa14-8454-4458-a32a-a2040d03ef10)

- Cada captura de tela inclui uma seção de título (seta verde) e uma seção de Comentários (seta vermelha)
![image](https://github.com/user-attachments/assets/de1a97a9-a5e4-4cbd-8c8b-208a9b9e0ebe)

- Selecione uma das quatro ferramentas de anotação
![image](https://github.com/user-attachments/assets/3b345eb6-5ac3-46c8-a87f-b2bd935173a9)

- Após selecionar uma ferramenta, especifique o estilo
![image](https://github.com/user-attachments/assets/62acbbba-c118-40f9-9a34-97674c64d121)

- Em seguida, clique no elemento que receberá a anotação e comece a digitar
![image](https://github.com/user-attachments/assets/32a7de11-6dc8-4bcc-a78c-5aacc1e83087)

- Após criar todas as anotações, clique em Save file (Salvar arquivo)
![image](https://github.com/user-attachments/assets/983da69f-78ae-4812-afa2-7d30eeec687f)

As Capturas de Tela com Anotações são salvas agora na pasta do Módulo em Outputs, dentro da pasta de instalação da extensão.

- Clique em `Generate output` (Gerar saída) para gerar os arquivos MD e HTML.
![image](https://github.com/user-attachments/assets/6422a4fa-bcac-4634-8c1c-c03b20d55aee)

- Você receberá uma mensagem avisando sobre a geração
![image](https://github.com/user-attachments/assets/4f0dd1cc-6d5f-44c6-8d9b-5579145aaa04)

- A extensão abrirá a pasta contendo as capturas de tela anotadas, e também o HTML e MD
![image](https://github.com/user-attachments/assets/3e1b91bd-0d9f-42f6-8e47-e27ceeba72d4)

![image](https://github.com/user-attachments/assets/a7201cae-30b6-4ddd-8e4f-cd60079ba9a7)

Você também pode alterar o layout do anotador, arrastando os menus.
![dg](https://github.com/user-attachments/assets/b4269d5d-7c37-43f1-9e2e-f90d8aacb730)

É possível alterar o título e as descrições do slide
![dg2](https://github.com/user-attachments/assets/a0264344-6c3d-403d-ae49-db8b30507623)

## Modo Desenvolvedor
- Se você habilitou o modo desenvolvedor (Edit > Application Settings > Developer > Enable developer mode) no Slicer, você pode notar opções adicionais dentro da extensão. Estas representam recursos experimentais e processos instáveis atualmente em teste
![image](https://github.com/user-attachments/assets/ce9478fa-e195-4cc8-b2ef-f90b3d4c9ed1)

- O recurso Fetch From GitHub permite que os usuários baixem tutoriais diretamente de uma lista curada de repositórios externos. Atualmente, este recurso está desabilitado para evitar problemas relacionados aos limites de taxa da API do GitHub.
- .Tutorial Creation Tools: Esses recursos auxiliam no desenvolvimento de novos tutoriais, permitindo gravar nomes e caminhos de widgets automaticamente.

## Escrevendo tutoriais
- Para orientações sobre o desenvolvimento de seus próprios tutoriais, siga o modelo e exemplos hospedados no SlicerTestRepository (https://github.com/SoniaPujolLab/SlicerTestTutorial).
