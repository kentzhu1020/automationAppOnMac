# coding: utf-8
import time
import sys
from Quartz.CoreGraphics import *

def mouseEvent(type,posx,posy):
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)


def mousemove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy)

def mouseclickdn(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy)

def mouseclickup(posx,posy):
    mouseEvent(kCGEventLeftMouseUp, posx,posy)

def mousedrag(posx,posy):
    mouseEvent(kCGEventLeftMouseDragged, posx,posy)







   



