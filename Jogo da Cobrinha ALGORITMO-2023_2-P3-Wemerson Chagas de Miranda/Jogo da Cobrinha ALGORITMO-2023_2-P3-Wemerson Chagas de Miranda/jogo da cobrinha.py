import pygame
from pygame.locals import * #contem todas funcoes e constante da biblioteca locals
from sys import exit #quando clicar fechar janela ela é chamda para fechar
from random import randint #sorteia valores dentro do intervalo das variaveis comida
from pygame import mixer
pygame.init() #iniciando o jogo


#parametros jogo
largura, altura = 660, 480 #660 em x e 480 em y
relogio = pygame.time.Clock()#quanto maior a quantidade de fraimes mais rapido o jogo roda
fim_jogo = False


#parametros de cores em RGB
#preta = (0, 0, 0)
#branca = (255, 255, 255)
#vermelha = (255, 0, 0)
#verde = (0, 255, 0)


#parametros musica
pygame.mixer.music.set_volume(0.2)
fundo_musica = mixer.music.load('Snake Baron.mp3')
mixer.music.play(-1)
musica_colidir = pygame.mixer.Sound('smw_coin.wav')


# Parâmetros da cobra
#dividimos por 2 a largura e altura,  pois vai aparcer no meio da tela
x_cobrinha = largura // 2
y_cobrinha = altura // 2
comprimento_inicial = 2
pontuacao = 0
lista_cobra = []


# Parâmetros da comida
#com a funçao RANDOM aciona outros valores(numeros aleatorios no intervalo de 30 e 480 no x)
#usamos um valor em x e em y
x_comida = randint(30, 480)
y_comida = randint(50, 400)


# Controlando a velocidade dos botões
velocidade_cobra = 10
x_velocidade = velocidade_cobra
y_velocidade = 0
velocidade_atual = velocidade_cobra


#tela de inico
game_over = False
inicio = True
iniciar_jogo = False


#tela padrão, com as suas dimensões
tela = pygame.display.set_mode((largura, altura))#a funcão setmode recebe na a largura e altura como dimensoes da tela
pygame.display.set_caption('Jogo da cobrinha')#a funçao set_caption nos permite colocar na nome na janela(titulo do jogo)


#uma funçao para inicio do jogo
def iniciar_jogo():
    global inicio
    inicio = False


#aqui vamos usar as letras do teclado para a movimentação, velocidade da cobra, que são(para cima:UP, para baixo:DOWN, para esquerda:LEFT e para direita:Right)
#usamos a função KEYDOWN
#quanto mais para baixo em eixo y maior serão os valores e logo, usamos -velocidade
def controle_velocidade(tecla, x_velocidade, y_velocidade):
    if tecla == K_LEFT and x_velocidade == 0:           #se a cobra não está se movendo horizontalmente (velocidade horizontal é zero)
        x_velocidade = -velocidade_cobra
        y_velocidade = 0                                #para a cobrar anda so na horizontal
    elif tecla == K_RIGHT and x_velocidade == 0:
        x_velocidade = velocidade_cobra
        y_velocidade = 0
    elif tecla == K_UP and y_velocidade == 0:
        x_velocidade = 0
        y_velocidade = -velocidade_cobra
    elif tecla == K_DOWN and y_velocidade == 0:
        x_velocidade = 0
        y_velocidade = velocidade_cobra

    return x_velocidade, y_velocidade


def tela_inicio():
    tela.fill((0,0,0))
    tela.fill((0, 255, 0))
    fonte3 = pygame.font.SysFont('Helvetica', 25)
    mensagem_inicio = 'Pressione ESPAÇO para iniciar'
    texto_inicio = fonte3.render(mensagem_inicio, True, (0, 0, 0))
    ret_texto_inicio = texto_inicio.get_rect()
    ret_texto_inicio.center = (largura // 2, altura // 2)
    tela.blit(texto_inicio, ret_texto_inicio)
    pygame.display.update()


#função para reinicio do jogo assim que o player tocar na propria cobra.
#usei a funçao GLOBAL do pygame para que essas variaveis sejam globais e passem a existir no jogo todo, deixando de ser varialvis locais, porque caso ocontrario, assim que a cobra tocar nela
# mesma o jogo para.
def restart_no_jogo():
    global pontuacao, comprimento_inicial, x_cobrinha, y_cobrinha, lista_cobra, lista_head, x_comida, y_comida, fim_jogo, x_velocidade, y_velocidade, velocidade_atual
    pontuacao = 0
    comprimento_inicial = 4
    x_cobrinha = largura / 2
    y_cobrinha = altura / 2
    lista_cobra = []
    lista_head = []
    x_comida = randint(30, 480)
    y_comida = randint(50, 400)
    fim_jogo = False
    velocidade_cobra = 10
    x_velocidade = velocidade_cobra
    y_velocidade = 0
    velocidade_atual = velocidade_cobra
    

#aqui vai aparecer a quantidade de pontos para o usuario assim que a cobra comer a comida
#a função blit desenha o que esta em texto, e o seu conteudo estara posicionado no canto superior esquedo em X e Y
#fonte.render cria uma superficie a ser exibido, definindo a cor do texto
def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont('Helvetica', 25)
    texto = fonte.render(f'Pontos: {pontuacao}', True, (255,0,0))
    tela.blit(texto, (10, 10))


#essa funçao desenha o corpo da cobra baseada nos valores armazenados na lista
#pega cada elemento da lista_cobra e desenha
def comprimento_cobra(lista_cobra):
    for XeY in lista_cobra:# as variaveis XeY representam uma [x,y], XeY[0] = x e [1]=y
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))


#loop principal do jogo 
#aqui com o usor de for detectamos se algum evento ocorreu
#aqui a cada interação do loop infinito a tela esta sendo prrecnida com  cor preta
while True:
    relogio.tick(velocidade_atual)
    #relogio.tick(8)
    tela.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
            #função que foi definida no inicio com sys import exit
        elif event.type == KEYDOWN:
            x_velocidade, y_velocidade = controle_velocidade(event.key, x_velocidade, y_velocidade)
        if event.type == KEYDOWN:
            if inicio and event.key == K_SPACE:
                iniciar_jogo()
    

    if inicio:
        tela_inicio()
    else:
           

    #aqui vai parar de se mover nas diagonais
        x_cobrinha += x_velocidade
        y_cobrinha += y_velocidade

   

        tamanho_cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobrinha, y_cobrinha, 20, 20))#retangulo que representa a cor verde da cobra, 330 em x e 240 em y e 20 de largura e 20 de altura
        tamanho_comida = pygame.draw.rect(tela, (255, 0, 0), (x_comida, y_comida, 20, 20))#retangulo que representa a cor vermelha da comida


    #Toda vez que o o retangulo verde(cobra) colidir com o retangulo vermelho(comida) assume outras
    #posiçoes e outros valores
    #usamos o colliderect para detecçao em uma sequencia.
        if tamanho_cobra.colliderect(tamanho_comida):
            x_comida = randint(30, 480)
            y_comida = randint(50, 400)
            pontuacao += 1
            comprimento_inicial += 1
            velocidade_atual += 1#toda vez que a cobra colide com a comida ela aumenta de velocidade, conforme aumenta de tamanho
            musica_colidir.play()

    #Assim como a cobra vai crescendo a lista cresce e a funçao usa essa lista e acresecenta
    #ela começa com a pos[x0, y0], [x1,y0] e assim por diante
        lista_head = []#armazena os valores de x e y da cabeça da cobra
        lista_head.append(x_cobrinha)#aqui armazena os valores de x
        lista_head.append(y_cobrinha)#aqui armazena os valores de y
        lista_cobra.append(lista_head)


    #aqui acontece que assim que a cobra tocar nela mesma morrer!
    #se existir mais de uma lista igual a lista cabeça dentro da lista lagarta, significa que a cobra encostou nela mesma
    #criei outro loop, se a cobra tocar nela mesma clicar com botão do mouse para voltar ao jogo, assim a mensagem aparece na tela.
        if lista_cobra.count(lista_head) > 1:
            fonte2 = pygame.font.SysFont('Helvetica', 15, True, True)
            mensagem = 'Você morreu! Clique no botão esquerdo do mouse para jogar novamente'
            texto_formatado = fonte2.render(mensagem, True, (0,0,0))
            ret_texto = texto_formatado.get_rect()
            fim_jogo = True
            while fim_jogo:
                tela.fill((0,255,0))
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            restart_no_jogo()
                            
                ret_texto.center = (largura//2, altura//2) 
                tela.blit(texto_formatado, ret_texto)
                pygame.display.update()


    #Aqui acontece o caso de que, se a cobra tocar na for para cima ela surge do lado oposto e assim o caso contrario, acontece tambem assim que passas do limite de tela direito aparece do lado esquerdo 
        '''if x_cobrinha > largura:
            x_cobrinha = 0
        if x_cobrinha < 0:
            x_cobrinha = largura
        if y_cobrinha < 0:
            y_cobrinha = altura
        if y_cobrinha > altura:
            y_cobrinha = 0'''  
        if x_cobrinha > largura or x_cobrinha < 0 or y_cobrinha < 0 or y_cobrinha > altura:
            restart_no_jogo()
           

    #esse if faz com que a cobra pare de crescer infinitamente
    #usamos o recurso Del para excluirmos o primeiro elemento
        if len(lista_cobra) > comprimento_inicial:
            del lista_cobra[0]
        

        comprimento_cobra(lista_cobra)


        desenhar_pontuacao(pontuacao)
    

   
#a cada interação do loop principal ela atualiza a tela do jogo 
# por exemplo o se nao existir o jogo roda e depois trava/buga  
    pygame.display.update()


    