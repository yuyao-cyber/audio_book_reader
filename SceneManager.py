import pygame, sys 
# Setup pygame/window ---------------------------------------- #
from pygame.locals import *
pygame.init()
font = pygame.font.SysFont('FreeSans', 25, bold= True)
screen = pygame.display.set_mode((1920, 1080),pygame.RESIZABLE)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    screen.fill((255,255,255))
    draw_text('1. Choose Your Book', font, (0,0,0), screen, 735,300) 
    draw_text('2. Continue Reading', font, (0,0,0), screen, 735,340)
    draw_text('4. Help', font, (0,0,0), screen, 735,340) 
    pygame.display.update()