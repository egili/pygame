import pygame, random, sys
from pygame.locals import *

#import RPi.GPIO as gp
#import time

# gp.setmode(gp.BCM)
# gp.setup(18, gp.OUT, initial = gp.LOW)
# gp.setup(22, gp.OUT, initial = gp.LOW)

LARGURA = 600 # altura e largura da janela de jogo
ALTURA = 600

# define as cores que serao utilizadas nos textos e no fundo 
COR_BRANCA = (255, 255, 255)
COR_PRETA = (0, 0, 0)
COR_VERMELHA = (255, 0, 0)
COR_AMARELA = (255, 255, 0)
COR_LARANJA = (238, 173, 45)

ADICIONA_NOVO_CACTO_A_CADA = 15 # a cada 15 pontos vai adicionar um novo cacto

def ouvirTeclaASerPressionada():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # clicar no X de fechar a janela
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # esc fecha o jogo
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE: # tecla espaco pressionada
                    pygame.init()
                    return

# a funcao dinoColidiuComCacto recebe os parametros: 
# rectDinossaurinho: as coordenadas retangulares do personagem
# arrayCacto: o array com todos os cactos que estao na tela

def dinoColidiuComCacto(rectDinossaurinho, arrayCacto):
    for cacto in arrayCacto:
        if rectDinossaurinho.colliderect(cacto['cactoRect']): # colliderect: checa se os dois retangulos (rectDinossaurinho e cactoRect) se sobreporam
            return True
    return False

# a funcao escreveTexto recebe os parametros:
# texto: string a ser escrita em tela
# fonteTexto: fonte com a qual o texto sera escrito
# superficie: a superficie da janela do jogo
# eixoX: posicao do texto no eixo X da superficie
# eixoY: posicao do texto no eixo Y da superficie

def escreveTexto(texto, fonteTexto, superficie, eixoX, eixoY, corTexto):
    textoObj = fonteTexto.render(texto, 5, corTexto) # cria o textoObj, que renderiza o texto com tamanho 5 e com cor recebida via parametro
    rectTexto = textoObj.get_rect() # captura o rect (coordenadas retangulares) do textoObj
    rectTexto.topleft = (eixoX, eixoY) # a partir do canto superior esquerdo, define as posicoes do eixoX e eixoY
    superficie.blit(textoObj, rectTexto) # blit permite posicionar algo em cima de outra coisa, no caso, escrever o texto em cima da janela de jogo

# este trecho inicia o pygame e a janela com o jogo 
pygame.init() # inicia o pygame
mainClock = pygame.time.Clock() # define FPS
superficieJanelaJogo = pygame.display.set_mode((ALTURA, LARGURA)) # inicia a tela do jogo, definindo o tamanho
pygame.display.set_caption('20669 - 21088 - 21816') # define o texto a ser exibido na aba superior da tela de jogo

fonteTexto = pygame.font.SysFont("Futura", 30) # configura o tipo e o tamanho da fonte

# iniciando os assets
dinossaurinho = pygame.image.load('assets/images/dino.png') # pega a imagem do dinossauro e salva na variavel 
rectDinossaurinho = dinossaurinho.get_rect() # define o Rect (objeto que armazena coordenadas retangulares), area ocupada pela imagem do personagem
cacto = pygame.image.load('assets/images/cacto.png') # pega a imagem do cacto e salva na variavel

# mostra a tela de inicio
escreveTexto('20669 - 21088 - 21816', fonteTexto, superficieJanelaJogo, 175 , 250, COR_AMARELA)
escreveTexto('Cotuca/4° Semestre - 2022', fonteTexto, superficieJanelaJogo, 150, 300, COR_AMARELA)
pygame.display.update() # atualiza a tela
ouvirTeclaASerPressionada() # chama a funcao que aguarda o espaco ou esc ser pressionado

pontuacaoMaxima = 0 # no inicio do jogo a pontuacao sempre estara zerada

while True:

    # configura o inicio do jogo

    chuvaDeCactos = [] # a tela comeca sem nenhum cacto

    pontuacao = 0 # a pontuacao comeca zerada
    
    rectDinossaurinho.topleft = (200, 550) # posição inicial do personagem na tela nos eixos x e y

    # as linhas seguintes definem que o dino comeca parado
    moverParaEsquerda = False
    moverParaDireita = False
    moverParaCima = False
    moverParaBaixo = False 

    parouJogo = False # false enquanto o jogo nao acabar

    contagemCactosAdicionadosEmTela = 0 # zero cactos em tela

    while True: # o loop roda enquanto o jogo esta acontecendo
        pontuacao += 1 # aumenta a pontuacao

        for event in pygame.event.get():
            if event.type == QUIT: # clicar no X de fechar a janela
                pygame.quit()
                sys.exit()

            if event.type == KEYUP: # quando a tecla sobe, apos ser pressionada
                if event.key == K_ESCAPE: # esc fecha o jogo
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEMOTION: # capturar movimentos do mouse
                rectDinossaurinho.move_ip(event.pos[0] - rectDinossaurinho.centerx, event.pos[1] - rectDinossaurinho.centery) # se o mouse se mover, move o personagem junto com o cursor

        # este trecho adiciona novos cactos em tela
        if not parouJogo:
            contagemCactosAdicionadosEmTela += 1 # enquanto o jogo estiver em andamento, adiciona novo cacto a contagem
        if contagemCactosAdicionadosEmTela == ADICIONA_NOVO_CACTO_A_CADA:
            contagemCactosAdicionadosEmTela = 0
            tamanhoCacto = random.randint(30, 60) # gera um numero aleatorio entre 30 e 60 que vai ser o tamanho do cacto
            
            # novoCacto = dicionario com as chaves:
            # cactoRect: a area retangular ocupada pelo cacto, varia de acordo com o tamanho do cacto (que é um numero aleatorio entre 30 e 60)
            # velocidadeQueda: valor numerico entre 1 e 8 gerado aleatoriamente
            # superficieTela: transform.scale utilizado para que o cacto se redimensione para a resolucao

            novoCacto = {'cactoRect': pygame.Rect(random.randint(0, LARGURA - tamanhoCacto), 0 - tamanhoCacto, tamanhoCacto, tamanhoCacto),
                        'velocidadeQueda': random.randint(1, 8), # define que a velocidade da queda do cacto sera entre 1 e 8, sendo aleatorio para cada novo cacto plotado em tela
                        'superficieTela': pygame.transform.scale(cacto, (tamanhoCacto, tamanhoCacto)),
                        }

            chuvaDeCactos.append(novoCacto) # inclui o novoCacto no array de cactos
        
        pygame.mouse.set_pos(rectDinossaurinho.centerx, rectDinossaurinho.centery) # faz com que o cursor do mouse acompanhe a pposicao do dino na tela

        # este trecho faz com que os cactos descam pela tela, caindo
        for cactos in chuvaDeCactos:
            if not parouJogo:
                cactos['cactoRect'].move_ip(0, cactos['velocidadeQueda']) # move_ip: move o retangulo 

        # remover da tela os cactos que chegarem a borda inferior
        for cactos in chuvaDeCactos[:]:
            if cactos['cactoRect'].top > ALTURA:
                chuvaDeCactos.remove(cactos)

        superficieJanelaJogo.fill(COR_BRANCA) # desenhar na tela a janela de jogo, pintando o fundo de preto

        #  mostra a pontuacao atual e a maxima
        escreveTexto('Pontos: %s' % (pontuacao), fonteTexto, superficieJanelaJogo, 450 , 0, COR_LARANJA) # posicao 450 no eixo x e 0 no eixo y
        escreveTexto('Máximo: %s' % (pontuacaoMaxima), fonteTexto, superficieJanelaJogo, 450, 40, COR_VERMELHA) # posicao 450 no eixo x e 40 no eixo y 

        superficieJanelaJogo.blit(dinossaurinho, rectDinossaurinho) # define e desenha o retangulo do personagem

        for cactos in chuvaDeCactos: # desenhar na tela cada cacto
            superficieJanelaJogo.blit(cactos['superficieTela'], cactos['cactoRect']) # funcao blit permite colocar uma imagem em cima de outra, no caso, o cacto por cima da janela de jogo

        pygame.display.update() # atualiza a tela

        # verifica a colisao entre o personagem e algum cacto
        if dinoColidiuComCacto(rectDinossaurinho, chuvaDeCactos):
            if pontuacao > pontuacaoMaxima:
                pontuacaoMaxima = pontuacao # definindo uma nova pontuacao maxima
                parouJogo = True

                # acende dois leds quando o jogo finalizar
                #gp.output(18, gp.HIGH)
                #gp.output(22, gp.HIGH)
                #time.sleep(1)
                #gp.output(18, gp.LOW)
                #gp.output(22, gp.HIGH)

            break

        mainClock.tick(40) # seta o fps 

    # para o jogo e mostra a tela de fim de jogo

    escreveTexto('Fim de Jogo', fonteTexto, superficieJanelaJogo, 200, 200, COR_VERMELHA) # posicao: 200 no eixo x e 200 no eixo y 
    escreveTexto('Aperte Espaço para jogar novamente', fonteTexto, superficieJanelaJogo, 120, 250, COR_LARANJA) # posicao: 120 no eixo x e 250 no eixo y 
    escreveTexto(' ou Esc para sair', fonteTexto, superficieJanelaJogo, 200, 300, COR_LARANJA) # posicao: 200 no eixo x e 300 no eixo y 

    pygame.display.update() # atualiza a tela
    ouvirTeclaASerPressionada() # chama a funcao que aguarda o espaco ou esc ser pressionado