import pygame

from game import constants
from enum import Enum

# マップの設定情報
class MapInfo(Enum):
    # 壁（キャラクターは移動不可能）
    WALL = 0
    # 道（キャラクターは移動可能）
    ROAD = 1

class Map:
    # コンストラクタ
    def __init__(self, map_data):
        # TODO マップ情報の検証処理を追加
        # 存在しない情報は入っている場合など
        self.map_data = map_data
        self.wall_list = []

        self.create_wall_list()

        wall = pygame.image.load(constants.WALL_IMAGE_PATH).convert()
        road = pygame.image.load(constants.ROAD_IMAGE_PATH).convert()

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