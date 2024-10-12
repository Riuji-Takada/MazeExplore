import pygame

from game import constants
from enum import Enum

class MapInfo(Enum):
    WALL = 0
    ROAD = 1

class Map:
    # コンストラクタ
    def __init__(self, map_data):
        self.map_data = map_data
        self.wall_list = []

        self.create_wall_list()

        wall = pygame.image.load('game/assets/wall.png').convert()
        road = pygame.image.load('game/assets/road.png').convert()

        self.map_dic = {
            MapInfo.WALL.value: wall,
            MapInfo.ROAD.value: road
        }

    def create_wall_list(self):
        max_i = len(self.map_data[0])
        max_j = len(self.map_data)

        for i in range(max_i):
            for j in range(max_j):
                if(self.map_data[j][i] != MapInfo.WALL.value):
                    continue
                x = i * constants.TILE_SIZE
                y = j * constants.TILE_SIZE
                self.wall_list.append(pygame.Rect(x, y, constants.TILE_SIZE, constants.TILE_SIZE))

    def get_wall_list(self):
        return self.wall_list

    def draw(self, screen):
        max_i = len(self.map_data[0])
        max_j = len(self.map_data)

        for i in range(max_i):
            for j in range(max_j):
                number = self.map_data[j][i] 
                image = self.map_dic[number] 
                x = i * constants.TILE_SIZE
                y = j * constants.TILE_SIZE
                screen.blit(image, (x, y))
                # TODO 本番で使うか要検討
                # pygame.draw.rect(screen, (200,200,200), (x, y, constants.TILE_SIZE, constants.TILE_SIZE), 1)

                # TODO 各マスの中心に円を描画
                # pygame.draw.circle(screen, (255,0,0), (i * constants.TILE_SIZE + constants.TILE_SIZE / 2, j * constants.TILE_SIZE + constants.TILE_SIZE / 2), 3)