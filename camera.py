#raspberrypi.org/forums/viewtopic.php?t=84388
import os
import pygame, sys

from pygame.locals import *
import pygame.camera

width = 300
height = 300

#initialize pygame
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0", (width,height))
cam.start()

#setup window
windowSurfaceObj = pygame.display.set_mode((width, height), 1, 16)
pygame.display.set_caption('Camera')

def getnewWebcam():
    #take a picture
    image = cam.get_image()
    cam.stop()

    #display the picture
    catSurfaceObj = image
    windowSurfaceObj.blit(catSurfaceObj, (0,0))
    pygame.display.update()

    #save picture
    pygame.image.save(windowSurfaceObj, 'picture.png')
