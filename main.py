# -*- coding: utf-8 -*-
"""
@author: Ozaki
"""

import pygame
import sys
from front import Front
from back import Back
from window import Window
from vent import Vent

def main():
    pygame.init()
    screen = pygame.display.set_mode((1094,676))
    clock = pygame.time.Clock()
    
    lock_flag = [False, False]
    
    room_state = 0
    room_ctrl = [Front(screen, lock_flag),
                 Back(screen, lock_flag),
                 Window(screen, lock_flag),
                 Vent(screen, lock_flag)]
    
    while True:

        """ マウスカーソル位置 """
        x, y = pygame.mouse.get_pos()
        room_ctrl[room_state].pos_event(x, y)
        
        """ クリックイベント，キーイベント """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                room_ctrl[room_state].click_event(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    room_state = (room_state - 1) % 4
                elif event.key == pygame.K_RIGHT:
                    room_state = (room_state + 1) % 4
                elif event.key == pygame.K_a:
                    lock_flag[0] = not lock_flag[0]
                elif event.key == pygame.K_b:
                    lock_flag[1] = not lock_flag[1]

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        """ 処理 """
        room_ctrl[room_state].do()
        
        """ 描画 """
        room_ctrl[room_state].draw()
        pygame.display.update()
        
        clock.tick(30)
        
        
if __name__ == '__main__':
    main()
