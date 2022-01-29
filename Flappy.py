import pygame
import os
import random
import sys

HEIGHT_SCREEN = 800
WIDTH_SCREEN = 500

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
IMAGE_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "background.png")))
IMAGES_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird_up.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird_mid.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird_donw.png"))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 20)


class Bird:
    IMGS = IMAGES_BIRD
    #Animações da rotação
    ROTATION_MAX = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[1]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
    #Calcular o deslocamento
        self.time += 1
        deslocamento = 1.5 % (self.time**2) + self.speed + self.time

    #Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
    
        self.y += deslocamento

        #Angulo do pássaro
        if deslocamento < 0 or self.y < (self.y + 50):
            if self.angulo < self.ROTATION_MAX:
                self.angulo = self.ROTATION_MAX
        else:
            if self.angulo > - 90:
                self.angulo -= self.ROTATION_SPEED

    # Definir imagem
    def drawn(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.ANIMATION_TIME:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.ANIMATION_TIME*2:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.ANIMATION_TIME*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.ANIMATION_TIME*4 +1:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = 0

    #Se o pássaro cair não bater a asa

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.ANIMATION_TIME * 2

    #Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        rect = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Pipe:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_top =  0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGE_PIPE, False, True)
        self.CANO_BASE = IMAGE_PIPE
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_top = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_top))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))
    
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        top_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_top = (self.x - passaro.x, self.pos_top - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(top_mask, distancia_top)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Base:
    VELOCIDADE = 5
    LARGURA = IMAGE_BASE.get_width()
    IMAGEM = IMAGE_BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA


    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGE_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.drawn(tela)
    for cano in canos:
        cano.desenhar(tela)
    

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (100, 100, 100))
    tela.blit(texto, (WIDTH_SCREEN -20 - texto.get_width(), 20))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    pygame.init()
    passaros = [Bird(240, 350)]
    chao = Base(730)
    canos = [Pipe(700)]
    tela = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 30)
    


    while rodando:        

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()
            elif evento.type == SCREEN_UPDATE:
                        #Mover as coisas
                for passaro in passaros:
                    passaro.move()
                chao.mover()

                adicionar_cano = False
                remover_canos = []
                for cano in canos:
                    for i, passaro in enumerate(passaros):
                        if cano.colidir(passaro):
                            passaro.pop(i)
                        if not cano.passou and passaro.x > cano.x:
                            cano.passou = True
                            adicionar_cano = True
                    cano.mover()
                    if cano.x + cano.CANO_TOPO.get_width() < 0:
                        remover_canos.append(cano)


                if adicionar_cano:
                    pontos += 1
                    canos.append(Pipe(700))
                for cano in remover_canos:
                    canos.remove(cano)

                for i, passaro in enumerate(passaros):
                    if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y <0:
                        passaros.pop(i)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaros[0].jump()
                
                if evento.key == pygame.K_w:
                    passaros[1].jump()

        

        desenhar_tela(tela, passaros, canos, chao, pontos)
        pygame.display.update()
        relogio.tick(120)
if __name__ == "__main__":
    main()