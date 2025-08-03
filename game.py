# -*- coding: utf-8 -*-
import time
import pygame
import os
import json
import random
# import libRec.libLibras as R
import asyncio
import sys
from pygame.locals import *
#from sqlalchemy import false

blue = (0, 0, 0)


class Block(pygame.sprite.Sprite):
    def __init__(self, color=blue, width=40, height=40):
        super(Block, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.org_image = pygame.Surface((width, height))
        self.org_image.fill(color)
        self.rect = self.image.get_rect()
        self.name = ""

    def set_size(self, width, height):
        self.image = pygame.transform.scale(self.org_image, (int(width), int(height)))

    def set_name(self, name):
        self.name = name

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_name(self):
        return self.name

    def set_image(self, filename=None):
        if (filename != None):
            self.org_image = pygame.image.load(filename)
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()


# definindo cores
def game():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 165, 223)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE_LINE = (2, 120, 161)

    # iniciando jogo
    pygame.init()
    with open('data.json',encoding='utf-8') as json_file:
        data = json.load(json_file)
        #random.shuffle(data)
        objs = data
    print(len(objs))

    with open('data2.json',encoding='utf-8') as json_file2:
        data2 = json.load(json_file2)
        random.shuffle(data2)
        objs2 = data2
    print(len(objs2))

    screen = pygame.display.set_mode((1720, 800))  # criando uma janela com largura e altura

    # carregando fonte
    font = pygame.font.SysFont(None, 80)
    pygame.display.set_caption('Oque É?')  # caption é a borda com o nome do jogo
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
    fullscreen = False
    fundo = pygame.image.load('imgs/cenario/cenario5.png')

    block_group = pygame.sprite.Group()
    a_block = Block()
    for i in range(0, len(objs)):
        block_group = pygame.sprite.Group()
        obj = data[i]["objeto"]
        print(obj)
        img = data[i]["img"]
        qtd = data[i]["quantidade"]
        texto = ""
        maos = []
        SwImgs = []
        p = 60
        l = 0
        random.shuffle(objs2)
        screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        x = 20
        for i in range(0, len(objs2)):
            a_block = Block()
            a_block.set_image(os.path.join('imgs/mao', objs2[i]["img"]))
            a_block.set_size(50, 80)
            a_block.set_position(100, 100)
            a_block.rect.x = x
            a_block.rect.y = (620)
            a_block.set_name(objs2[i]["letra"])
            block_group.add(a_block)
            x += 66
            # print(objs2[i]["img"])
            # print(block_group)
        # preenchendo o fundo com azul

        while True:
            w, h = pygame.display.get_surface().get_size()
            correcaoW = w / 1280
            correcaoH = h / 720
            x = 15
            nletras = 1
            posletras = 535
            for a_block in block_group:
                a_block.set_size(50 * correcaoW, 80 * correcaoH)
                a_block.set_position(100, 100)
                a_block.rect.x = x * correcaoW
                a_block.rect.y = (posletras * correcaoH)
                nletras += 1
                if (nletras == 23):
                    posletras += 90
                    x = 15
                else:
                    x += 55
                pass

            fundoR = pygame.transform.scale(fundo, (int(w), int(h)))

            screen.blit(fundoR, (0, 0))

            block_group.draw(screen)

            image = pygame.image.load(os.path.join('imgs/objs', img))
            # image = pygame.transform.scale(image, (420, 495))
            # screen.blit(image, (1210, 140))
            image = pygame.transform.scale(image, (int(300 * correcaoW), int(390 * correcaoH)))
            screen.blit(image, (w * 0.71, h * 0.14))
            p = 105 * correcaoW
            for mao in maos:
                print(p)
                #tamanho do bloco das maos impressas
                mao = pygame.transform.scale(mao, (int(60 * correcaoW), int(70 * correcaoH)))
                screen.blit(mao, (p, h * 0.34))
                #distancia entre as maos
                p = p + (60 * correcaoW)
                pass

            p = 105 * correcaoW
            for Sw in SwImgs:
                Sw = pygame.transform.scale(Sw, (int(30 * correcaoW), int(30 * correcaoH)))
                screen.blit(Sw, (p, h * 0.46))
                p = p + (55 * correcaoW)
                pass
            # definindo o texto
            espaco = ""
            tamanho = len(texto)
            espaco = texto

            for x in range(0, qtd - tamanho):
                espaco = espaco + "_ "

            text = font.render(espaco, True, WHITE)
            # copiando o texto para a superficie
            screen.blit(text, [w * 0.13, h * 0.20])

            # atualizando a tela+++++++++++++++++++++++
            pygame.display.flip()

            if tamanho == qtd:
                time.sleep(2)
                break

            for event in pygame.event.get():
                x += 1
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return 0
                if event.type == pygame.KEYDOWN:

                    if event.unicode == obj[l]:
                        l += 1
                        nomeImagem = event.unicode + ".png"
                        print(nomeImagem)
                        letraImg = pygame.image.load(os.path.join('imgs/mao', nomeImagem))
                        SwImg = pygame.image.load(os.path.join('imgs/SignWriting', nomeImagem))
                        maos.append(letraImg)
                        SwImgs.append(SwImg)
                        texto += event.unicode

                    print(event.unicode)

                if event.type == pygame.MOUSEBUTTONUP:
                    for bloco in block_group.sprites():
                        if bloco.rect.collidepoint(event.pos):
                            mouse_pos = pygame.mouse.get_pos()
                            bloco.set_position(mouse_pos[0], mouse_pos[1])
                            letra_mouse = bloco.get_name()
                            if letra_mouse == obj[l]:
                                l += 1
                                nomeImagem = letra_mouse + ".png"
                                print(nomeImagem)
                                letraImg = pygame.image.load(os.path.join('imgs/mao', nomeImagem))
                                SwImg = pygame.image.load(os.path.join('imgs/SignWriting', nomeImagem))
                                maos.append(letraImg)
                                SwImgs.append(SwImg)
                                texto += letra_mouse

            time.sleep(0.4)
            pygame.display.update()
    pygame.quit()


game()
