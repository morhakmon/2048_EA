#!/usr/bin/python
#
# py2048: Python version of the famous 2048 Game with animated graphics
# Copyright 2016 Andrea Vucetich
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import pickle

import pygame
from random import choice, randint
from sys import exit
from copy import deepcopy
from pygame.locals import *
import random
# Variable Declaration Section

FPS = 30
WINDOWWIDTH = 375
WINDOWHEIGHT = 667
ANIMATION_FRAMES = 17
#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_SELECT = (204, 0, 204)
GREY1 = (224, 224, 224)
GREY2 = (160, 160, 160)
SET_1 = {2: (255, 51, 255),
         4: (204, 0, 204),
         8: (102, 0, 102),
         16: (153, 51, 255),
         32: (102, 0, 204),
         64: (51, 0, 102),
         128: (51, 51, 255),
         256: (0, 0, 204),
         512: (0, 0, 102),
         1024: (51, 153, 255),
         2048: (0, 102, 204),
         4096: (0, 51, 102),
         8192: (51, 255, 255),
         16384: (0, 204, 204)}
SET_2 = {2: (51, 255, 255),
         4: (0, 204, 204),
         8: (0, 102, 102),
         16: (51, 255, 153),
         32: (0, 204, 102),
         64: (0, 102, 51),
         128: (51, 255, 51),
         256: (0, 204, 0),
         512: (0, 102, 0),
         1024: (153, 255, 51),
         2048: (102, 204, 0),
         4096: (51, 102, 0),
         8192: (255, 153, 51),
         16384: (204, 102, 0)}
SET_3 = {2: (255, 153, 51),
         4: (204, 102, 0),
         8: (102, 51, 0),
         16: (255, 51, 51),
         32: (204, 0, 0),
         64: (102, 0, 0),
         128: (255, 51, 153),
         256: (204, 0, 102),
         512: (102, 0, 51),
         1024: (255, 51, 255),
         2048: (204, 0, 204),
         4096: (102, 0, 102),
         8192: (153, 51, 255),
         16384: (102, 0, 204)}


with open('example_agent.pickle', 'rb') as handle:
    AGENT = pickle.load(handle)

FAIL_MOVE = False

def terminate():
    pygame.quit()
    exit()


def drawTitle():
    TitleFont = pygame.font.Font('freesansbold.ttf', 75)
    TitleObj = TitleFont.render('py2048', 1, BLACK)
    TitleRect = TitleObj.get_rect()
    TitleRect.center = (WINDOWWIDTH / 2, 65)
    DISPLAYSURF.blit(TitleObj, TitleRect)


def drawBorderSquare():
    OuterSquare = pygame.Rect(0, 0, 357, 357)
    OuterSquare.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 20)
    pygame.draw.rect(DISPLAYSURF, BLACK, OuterSquare)
    InnerSquare = pygame.Rect(0, 0, 351, 351)
    InnerSquare.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 20)
    pygame.draw.rect(DISPLAYSURF, WHITE, InnerSquare)


def main():
    global FPSCLOCK, BASICFONT, DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048 Game')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    StartScreen()


def StartScreen():
    EntryFont = pygame.font.Font('freesansbold.ttf', 55)
    Entries = ['Start', 'Quit']
    Entry_Selected = 0

    while True:

        DISPLAYSURF.fill(WHITE)

        for event in pygame.event.get():  # Managing Inputs
            # Managing Quit Input
            if event.type == QUIT:
                terminate()
            # Managing Keydown Input
            elif event.type == KEYDOWN:
                if (event.key == K_UP or event.key == K_w) and Entry_Selected > 0:
                    Entry_Selected = Entry_Selected - 1
                elif (event.key == K_DOWN or event.key == K_s) and Entry_Selected < len(Entries) - 1:
                    Entry_Selected = Entry_Selected + 1
                elif event.key == K_ESCAPE:
                    terminate()
                # Managing Return
                elif event.key == K_RETURN:
                    if Entries[Entry_Selected] == 'Start':
                        RunGame()
                        pass
                    elif Entries[Entry_Selected] == 'Quit':
                        terminate()

        drawTitle()
        drawBorderSquare()

        # Drawing Menu Entries
        for i in range(len(Entries)):
            if i == Entry_Selected:
                ENTRY_COLOR = COLOR_SELECT
            else:
                ENTRY_COLOR = BLACK

            Entry_Obj = EntryFont.render(Entries[i], 1, ENTRY_COLOR)
            Entry_Rect = Entry_Obj.get_rect()
            Entry_Rect.center = (WINDOWWIDTH / 2, 250 + 100 * i)
            DISPLAYSURF.blit(Entry_Obj, Entry_Rect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def RunGame():
    global FAIL_MOVE
    TILE_COLOR = SET_1
    game_state = [[0 for x in range(4)] for y in range(4)]
    game_state_premove = [[0 for x in range(4)] for y in range(4)]
    movements = []  # Each value will be (row_start, col_start, row_finish, col_finish, Number_on_tile, isSumming?_flag)
    showing_up_tiles = []  # Each value will be (row, col, number)
    game_dynamics = {'status': 'dynamic', 'i': 11}  # This are the starting values properly set
    game_score = 0
    OUTER_SQ1_COLOR = BLACK
    OUTER_SQ2_COLOR = BLACK
    OUTER_SQ3_COLOR = BLACK

    # Create The Array with the computed centers coordinates of each Tile in the main square
    centers_coordinates = [[(0, 0) for x in range(4)] for y in range(4)]
    for row in range(4):
        for col in range(4):
            centers_coordinates[row][col] = [12 + 45 + (84 + 3) * col, 178 + 45 + (84 + 3) * row]

    # ---Declaring RUNGAME functions---
    def drawGame_State(game_state_passed):
        for row in range(4):
            for col in range(4):
                if game_state_passed[row][col] != 0:
                    drawTile(row, col, game_state_passed[row][col])

    def drawTile(row, col, number):
        TileBackRect = pygame.Rect(0, 0, 84, 84)
        TileBackRect.center = centers_coordinates[row][col]
        pygame.draw.rect(DISPLAYSURF, TILE_COLOR[number], TileBackRect)  # Draw The Background of the tile

        font_size = 50
        if number >= 1024:
            font_size = 30
        TileFont = pygame.font.Font('freesansbold.ttf', font_size)
        TileObj = TileFont.render(str(number), 1, WHITE)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row][col]
        DISPLAYSURF.blit(TileObj, TileRect)  # Draw The Number over the tile

    def showupTile(row, col, number, movement_i):
        TileBackRect = pygame.Rect(0, 0, 49, 49)  # Draw The Background of the tile
        TileBackRect.center = centers_coordinates[row][col]

        font_size = 50
        if number >= 1024:
            font_size = 30
        TileFont = pygame.font.Font('freesansbold.ttf', font_size)  # Draw The Number over the tile
        TileObj = TileFont.render(str(number), 1, WHITE)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row][col]

        if (movement_i > 5):
            movement_i = 5

        TileBackRect = TileBackRect.inflate(7 * movement_i, 7 * movement_i)
        TileBackRect.center = centers_coordinates[row][col]

        pygame.draw.rect(DISPLAYSURF, TILE_COLOR[number], TileBackRect)  # Redraw the showing up rect
        DISPLAYSURF.blit(TileObj, TileRect)  # Redraw the number

    def drawMovingTile(grid_param, movement_i):
        row_s, col_s, row_f, col_f, number, flag = grid_param
        TileBackRect = pygame.Rect(0, 0, 84, 84)  # Draw The Background of the tile
        TileBackRect.center = centers_coordinates[row_s][col_s]

        font_size = 50
        if number >= 1024:
            font_size = 30
        TileFont = pygame.font.Font('freesansbold.ttf', font_size)  # Draw The Number over the tile
        TileObj = TileFont.render(str(number), 1, WHITE)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row_f][col_f]

        if (row_f < row_s):  # MovementTowardsUp
            distance = centers_coordinates[row_s][col_s][1] - centers_coordinates[row_f][col_f][1]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0],
                                   centers_coordinates[row_s][col_s][1] - step * movement_i]
            TileRect.center = [centers_coordinates[row_s][col_s][0],
                               centers_coordinates[row_s][col_s][1] - step * movement_i]
        if (row_f > row_s):  # MovementTowardsDown
            distance = centers_coordinates[row_f][col_f][1] - centers_coordinates[row_s][col_s][1]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0],
                                   centers_coordinates[row_s][col_s][1] + step * movement_i]
            TileRect.center = [centers_coordinates[row_s][col_s][0],
                               centers_coordinates[row_s][col_s][1] + step * movement_i]
        if (col_f < col_s):  # MovementTowardsLeft
            distance = centers_coordinates[row_s][col_s][0] - centers_coordinates[row_f][col_f][0]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0] - step * movement_i,
                                   centers_coordinates[row_s][col_s][1]]
            TileRect.center = [centers_coordinates[row_s][col_s][0] - step * movement_i,
                               centers_coordinates[row_s][col_s][1]]
        if (col_f > col_s):  # MovementTowardsRight
            distance = centers_coordinates[row_f][col_f][0] - centers_coordinates[row_s][col_s][0]
            step = distance / 10
            TileBackRect.center = [centers_coordinates[row_s][col_s][0] + step * movement_i,
                                   centers_coordinates[row_s][col_s][1]]
            TileRect.center = [centers_coordinates[row_s][col_s][0] + step * movement_i,
                               centers_coordinates[row_s][col_s][1]]

        pygame.draw.rect(DISPLAYSURF, TILE_COLOR[number], TileBackRect)  # Redraw the moving rect
        DISPLAYSURF.blit(TileObj, TileRect)  # Redraw the moving number

    def summingTile(row, col, number, movement_i):
        TileBackRect = pygame.Rect(0, 0, 74, 74)  # Draw The Background of the tile
        TileBackRect.center = centers_coordinates[row][col]

        font_size = 50
        if number >= 1024:
            font_size = 30
        TileFont = pygame.font.Font('freesansbold.ttf', font_size)  # Draw The Number over the tile
        TileObj = TileFont.render(str(number), 1, WHITE)
        TileRect = TileObj.get_rect()
        TileRect.center = centers_coordinates[row][col]

        if movement_i == 5:
            movement_i = 3
        if (movement_i > 5):
            movement_i = 2

        TileBackRect = TileBackRect.inflate(5 * movement_i, 5 * movement_i)
        TileBackRect.center = centers_coordinates[row][col]

        pygame.draw.rect(DISPLAYSURF, TILE_COLOR[number], TileBackRect)  # Redraw the showing up rect
        DISPLAYSURF.blit(TileObj, TileRect)  # Redraw the number

    def MovementTowardsLeft():
        for row in range(4):
            for col in range(1, 4):
                if (game_state[row][col] != 0) and (game_state[row][col - 1] == 0):
                    tmp_n_var = game_state[row][col]
                    shift_index = 1
                    while (col - shift_index >= 0) and (game_state[row][col - shift_index] == 0):
                        game_state[row][col - shift_index] = game_state[row][col - shift_index + 1]
                        game_state[row][col - shift_index + 1] = 0
                        shift_index += 1
                    movements.append((row, col, row, col - shift_index + 1, tmp_n_var, 0))

    def SumTowardsLeft():
        score_increase = 0
        for row in range(4):
            for col in range(1, 4):
                if (game_state[row][col] != 0) and (game_state[row][col - 1] == game_state[row][col]):
                    tmp_n_var = game_state[row][col]
                    game_state[row][col - 1] = game_state[row][col - 1] * 2
                    game_state[row][col] = 0
                    movements.append((row, col, row, col - 1, tmp_n_var, 1))
                    score_increase += tmp_n_var * 2
        return score_increase

    def MovementTowardsRight():
        for row in range(4):
            for col in range(2, -1, -1):
                if (game_state[row][col] != 0) and (game_state[row][col + 1] == 0):
                    tmp_n_var = game_state[row][col]
                    shift_index = 1
                    while (col + shift_index <= 3) and (game_state[row][col + shift_index] == 0):
                        game_state[row][col + shift_index] = game_state[row][col + shift_index - 1]
                        game_state[row][col + shift_index - 1] = 0
                        shift_index += 1
                    movements.append((row, col, row, col + shift_index - 1, tmp_n_var, 0))

    def SumTowardsRight():
        score_increase = 0
        for row in range(4):
            for col in range(2, -1, -1):
                if (game_state[row][col] != 0) and (game_state[row][col + 1] == game_state[row][col]):
                    tmp_n_var = game_state[row][col]
                    game_state[row][col + 1] = game_state[row][col + 1] * 2
                    game_state[row][col] = 0
                    movements.append((row, col, row, col + 1, tmp_n_var, 1))
                    score_increase += tmp_n_var * 2
        return score_increase

    def MovementTowardsUp():
        for row in range(1, 4):
            for col in range(4):
                if (game_state[row][col] != 0) and (game_state[row - 1][col] == 0):
                    tmp_n_var = game_state[row][col]
                    shift_index = 1
                    while (row - shift_index >= 0) and (game_state[row - shift_index][col] == 0):
                        game_state[row - shift_index][col] = game_state[row - shift_index + 1][col]
                        game_state[row - shift_index + 1][col] = 0
                        shift_index += 1
                    movements.append((row, col, row - shift_index + 1, col, tmp_n_var, 0))

    def SumTowardsUp():
        score_increase = 0
        for row in range(1, 4):
            for col in range(4):
                if (game_state[row][col] != 0) and (game_state[row - 1][col] == game_state[row][col]):
                    tmp_n_var = game_state[row][col]
                    game_state[row - 1][col] = game_state[row - 1][col] * 2
                    game_state[row][col] = 0
                    movements.append((row, col, row - 1, col, tmp_n_var, 1))
                    score_increase += tmp_n_var * 2
        return score_increase

    def MovementTowardsDown():
        for row in range(2, -1, -1):
            for col in range(4):
                if (game_state[row][col] != 0) and (game_state[row + 1][col] == 0):
                    tmp_n_var = game_state[row][col]
                    shift_index = 1
                    while (row + shift_index <= 3) and (game_state[row + shift_index][col] == 0):
                        game_state[row + shift_index][col] = game_state[row + shift_index - 1][col]
                        game_state[row + shift_index - 1][col] = 0
                        shift_index += 1
                    movements.append((row, col, row + shift_index - 1, col, tmp_n_var, 0))

    def SumTowardsDown():
        score_increase = 0
        for row in range(2, -1, -1):
            for col in range(4):
                if (game_state[row][col] != 0) and (game_state[row + 1][col] == game_state[row][col]):
                    tmp_n_var = game_state[row][col]
                    game_state[row + 1][col] = game_state[row + 1][col] * 2
                    game_state[row][col] = 0
                    movements.append((row, col, row + 1, col, tmp_n_var, 1))
                    score_increase += tmp_n_var * 2
        return score_increase

    def MergeMovements():  # in the "movements" list is currently possible to have 2 movements for the same tile or other disordinate combinations
        to_be_del = []
        for x in range(len(movements)):
            for y in range(x + 1, len(movements)):
                if (movements[x][4] == movements[y][4]) and (movements[x][2] == movements[y][0]) and (
                        movements[x][3] == movements[y][1]):
                    movements[x] = (movements[x][0], movements[x][1], movements[y][2], movements[y][3], movements[y][4],
                                    movements[y][5])
                    to_be_del.append(y)
                elif (movements[x][5] == 1) and (movements[x][4] * 2 == movements[y][4]) and (
                        movements[x][2] == movements[y][0]) and (movements[x][3] == movements[y][1]):
                    movements[x] = (movements[x][0], movements[x][1], movements[y][2], movements[y][3], movements[x][4],
                                    movements[x][5])
                    movements[y] = (movements[y][0], movements[y][1], movements[y][2], movements[y][3], movements[x][4],
                                    movements[x][5])
        to_be_del.sort(reverse=True)
        for z in to_be_del:
            del movements[z]

    def CreateRandomTiles(n):

        random_value_list = [2, 4]
        for i in range(n):
            empt_c = {'row': randint(0, 3), 'col': randint(0, 3)}
            while (game_state[empt_c['row']][empt_c['col']] != 0) or (
                    (empt_c['row'], empt_c['col'], 4) in showing_up_tiles) or (
                    (empt_c['row'], empt_c['col'], 2) in showing_up_tiles):
                empt_c = {'row': randint(0, 3), 'col': randint(0, 3)}
            chosen_rndm_val = choice(random_value_list)
            # Stores the created value in the list of tiles to show up when the moment comes
            showing_up_tiles.append((empt_c['row'], empt_c['col'], chosen_rndm_val))

    # ---Proper game code starts here---
    CreateRandomTiles(2)

    while True:

        DISPLAYSURF.fill(WHITE)
        drawTitle()
        drawBorderSquare()

        # Draw Score
        ScoreFont = pygame.font.Font('freesansbold.ttf', 20)
        Score_String = "Score:  " + str(game_score)
        ScoreObj = ScoreFont.render(Score_String, 1, BLACK)
        ScoreRect = ScoreObj.get_rect()
        ScoreRect.topleft = (8, 150)
        DISPLAYSURF.blit(ScoreObj, ScoreRect)

        # Draw Color Changer
        CC_String = "Select color:"
        CC_Obj = ScoreFont.render(CC_String, 1, BLACK)
        CC_Rect = CC_Obj.get_rect()
        CC_Rect.topleft = (171, 150)
        DISPLAYSURF.blit(CC_Obj, CC_Rect)

        SET1Square = pygame.Rect(0, 0, 20, 20)
        SET1Square.topleft = (296, 152)
        pygame.draw.rect(DISPLAYSURF, OUTER_SQ1_COLOR, SET1Square)
        SET1_white_Square = pygame.Rect(0, 0, 14, 14)
        SET1_white_Square.center = SET1Square.center
        pygame.draw.rect(DISPLAYSURF, WHITE, SET1_white_Square)
        SET1_inside_Square = pygame.Rect(0, 0, 10, 10)
        SET1_inside_Square.center = SET1Square.center
        pygame.draw.rect(DISPLAYSURF, SET_1[2], SET1_inside_Square)

        if SET1Square.collidepoint(pygame.mouse.get_pos()):
            OUTER_SQ1_COLOR = GREY2
        else:
            OUTER_SQ1_COLOR = BLACK

        SET2Square = pygame.Rect(0, 0, 20, 20)
        SET2Square.topleft = (321, 152)
        pygame.draw.rect(DISPLAYSURF, OUTER_SQ2_COLOR, SET2Square)
        SET2_white_Square = pygame.Rect(0, 0, 14, 14)
        SET2_white_Square.center = SET2Square.center
        pygame.draw.rect(DISPLAYSURF, WHITE, SET2_white_Square)
        SET2_inside_Square = pygame.Rect(0, 0, 10, 10)
        SET2_inside_Square.center = SET2Square.center
        pygame.draw.rect(DISPLAYSURF, SET_2[2], SET2_inside_Square)

        if SET2Square.collidepoint(pygame.mouse.get_pos()):
            OUTER_SQ2_COLOR = GREY2
        else:
            OUTER_SQ2_COLOR = BLACK

        SET3Square = pygame.Rect(0, 0, 20, 20)
        SET3Square.topleft = (346, 152)
        pygame.draw.rect(DISPLAYSURF, OUTER_SQ3_COLOR, SET3Square)
        SET3_white_Square = pygame.Rect(0, 0, 14, 14)
        SET3_white_Square.center = SET3Square.center
        pygame.draw.rect(DISPLAYSURF, WHITE, SET3_white_Square)
        SET3_inside_Square = pygame.Rect(0, 0, 10, 10)
        SET3_inside_Square.center = SET3Square.center
        pygame.draw.rect(DISPLAYSURF, SET_3[2], SET3_inside_Square)

        if SET3Square.collidepoint(pygame.mouse.get_pos()):
            OUTER_SQ3_COLOR = GREY2
        else:
            OUTER_SQ3_COLOR = BLACK

        # Drawing Background Squares
        for row in range(4):
            for col in range(4):
                background_rect = pygame.Rect(15 + (3 + 84) * col, 181 + (3 + 84) * row, 84, 84)
                pygame.draw.rect(DISPLAYSURF, GREY1, background_rect)

        # ------case: STATIC - END OF ANIMATION
        if (game_dynamics['status'] == 'static') and (game_dynamics['i'] == ANIMATION_FRAMES):

            drawGame_State(game_state)

            for event in pygame.event.get():
                # Managing Quit Input
                if event.type == QUIT:
                    terminate()
                # Managing Clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_click, y_click = event.pos
                    if SET1Square.collidepoint(x_click, y_click):
                        TILE_COLOR = SET_1
                    elif SET2Square.collidepoint(x_click, y_click):
                        TILE_COLOR = SET_2
                    elif SET3Square.collidepoint(x_click, y_click):
                        TILE_COLOR = SET_3
                # Managing Keydown Input

                # change here to add agent
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        actions = AGENT.run(game_state)
                        if FAIL_MOVE:
                            move = actions[random.randint(1, 3)][1]
                        else:
                            move = actions[0][1]

                        if move == 2:

                            game_state_premove = deepcopy(game_state)
                            MovementTowardsLeft()
                            game_score += SumTowardsLeft()
                            MovementTowardsLeft()
                            MergeMovements()

                            if (game_state != game_state_premove):
                                CreateRandomTiles(1)
                                game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'
                                FAIL_MOVE = False
                            else:
                                FAIL_MOVE = True

                        elif move == 3:

                            game_state_premove = deepcopy(game_state)
                            MovementTowardsRight()
                            game_score += SumTowardsRight()
                            MovementTowardsRight()
                            MergeMovements()

                            if (game_state != game_state_premove):
                                CreateRandomTiles(1)
                                game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'
                                FAIL_MOVE = False
                            else:
                                FAIL_MOVE = True

                        elif move == 0:

                            game_state_premove = deepcopy(game_state)
                            MovementTowardsUp()
                            game_score += SumTowardsUp()
                            MovementTowardsUp()
                            MergeMovements()

                            if (game_state != game_state_premove):
                                CreateRandomTiles(1)
                                game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'
                                FAIL_MOVE = False
                            else:
                                FAIL_MOVE = True

                        elif move == 1:

                            game_state_premove = deepcopy(game_state)
                            MovementTowardsDown()
                            game_score += SumTowardsDown()
                            MovementTowardsDown()
                            MergeMovements()

                            if (game_state != game_state_premove):
                                CreateRandomTiles(1)
                                game_dynamics['i'], game_dynamics['status'] = 0, 'dynamic'
                                FAIL_MOVE = False
                            else:
                                FAIL_MOVE = True

                        elif event.key == K_ESCAPE:
                            terminate()

        # ------case: DYNAMIC - ANIMATION PROGRESSING
        elif (game_dynamics['status'] == 'dynamic') and (game_dynamics['i'] < ANIMATION_FRAMES):
            busy_spot_flag = [[0 for x in range(4)] for y in range(
                4)]  # 0 = will remain as is, 1 = is the destination of a movement, 2 = is the destination of a sum
            for x in range(len(movements)):
                if (movements[x][5] == 0):
                    busy_spot_flag[movements[x][2]][movements[x][3]] = 1
                if (movements[x][5] == 1):
                    busy_spot_flag[movements[x][2]][movements[x][3]] = 2

            if (game_dynamics['i'] < 11):  # PROPER MOVEMENT OF TILES

                # Draw tiles in motion
                for x in range(len(movements)):
                    drawMovingTile(movements[x], game_dynamics['i'])

                # Draw tiles not moving in Game_State
                for row in range(4):
                    for col in range(4):
                        if (game_state[row][col] != 0) and (busy_spot_flag[row][col] == 0):
                            drawTile(row, col, game_state[row][col])
                        elif (game_state[row][col] != 0) and (busy_spot_flag[row][col] == 2) and (
                                game_state[row][col] == game_state_premove[row][col] * 2):
                            drawTile(row, col, game_state_premove[row][col])

            if (game_dynamics['i'] >= 11):  # SHOWING UP + SUMMING UP OF TILES
                # Draw tiles not moving in Game_State
                for row in range(4):
                    for col in range(4):
                        if (game_state[row][col] != 0) and (busy_spot_flag[row][col] != 2):
                            drawTile(row, col, game_state[row][col])
                        elif (game_state[row][col] != 0) and (busy_spot_flag[row][col] == 2):
                            summingTile(row, col, game_state[row][col], game_dynamics['i'] - 11)

                # Draw tiles showing up
                for i in range(len(showing_up_tiles)):
                    showupTile(showing_up_tiles[i][0], showing_up_tiles[i][1], showing_up_tiles[i][2],
                               game_dynamics['i'] - 11)

            game_dynamics['i'] += 1



        # ------case: DYNAMIC - END OF ANIMATION
        elif (game_dynamics['status'] == 'dynamic') and (game_dynamics['i'] == ANIMATION_FRAMES):

            # Scroll through the Tiles showing up and put them in the game_state
            for i in range(len(showing_up_tiles)):
                game_state[showing_up_tiles[i][0]][showing_up_tiles[i][1]] = showing_up_tiles[i][2]

            drawGame_State(game_state)

            # Perform A GameOverCheck
            gameover_check_flag = "Yes"
            for row in range(4):
                for col in range(4):
                    if (game_state[row][col] == 0):
                        gameover_check_flag = "No"
                    elif (game_state[row][col] == 16384):
                        gameover_check_flag = "MAX"
                        break
                        break

            if gameover_check_flag == "Yes":

                game_state_premove = deepcopy(game_state)
                MovementTowardsLeft()
                SumTowardsLeft()
                MovementTowardsRight()
                SumTowardsRight()
                MovementTowardsUp()
                SumTowardsUp()
                MovementTowardsDown()
                SumTowardsDown()

                if game_state_premove == game_state:

                    string_to_display = "Game Over"
                    game_dynamics['status'] = 'over'

                else:
                    game_state = game_state_premove
                    # Game Can Continue
                    showing_up_tiles = []
                    movements = []
                    game_dynamics['status'] = 'static'

            elif gameover_check_flag == "MAX":

                string_to_display = "Max Value"
                game_dynamics['status'] = 'over'

            else:
                # Game Can Continue
                showing_up_tiles = []
                movements = []
                game_dynamics['status'] = 'static'



        # ------case: GAME OVER - END OF ANIMATION
        elif (game_dynamics['status'] == 'over') and (game_dynamics['i'] == ANIMATION_FRAMES):

            drawGame_State(game_state)

            for event in pygame.event.get():  # Managing Inputs
                # Managing Quit Input
                if event.type == QUIT:
                    terminate()

                elif event.type == KEYDOWN:
                    # Managing Return
                    if event.key == K_RETURN:

                        game_state = [[0 for x in range(4)] for y in range(4)]
                        game_state_premove = [[0 for x in range(4)] for y in range(4)]
                        movements = []
                        showing_up_tiles = []
                        game_dynamics = {'status': 'dynamic', 'i': 11}
                        game_score = 0
                        CreateRandomTiles(2)

                    # Managing ESC
                    elif event.key == K_ESCAPE:
                        terminate()

            GOFont = pygame.font.Font('freesansbold.ttf', 50)
            GOObj = GOFont.render(string_to_display, 1, BLACK)
            GORect = GOObj.get_rect()
            GORect.center = (WINDOWWIDTH / 2, 560)
            DISPLAYSURF.blit(GOObj, GORect)

            GOFont = pygame.font.Font('freesansbold.ttf', 14)
            GOObj = GOFont.render("Press enter to start new game", 1, BLACK)
            GORect = GOObj.get_rect()
            GORect.center = (WINDOWWIDTH / 2, 600)
            DISPLAYSURF.blit(GOObj, GORect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
