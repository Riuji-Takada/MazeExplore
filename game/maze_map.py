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
        # マップの行数
        self.ROW_COUNT = len(self.map_data)
        # マップの列数
        self.COLUMN_COUNT = len(self.map_data[0])
        # 壁のRectのリスト（当たり判定用）
        self.wall_list = []

        self.create_wall_list()

        # タイル画像の読み込み
        wall = pygame.image.load(constants.WALL_IMAGE_PATH).convert()
        road = pygame.image.load(constants.ROAD_IMAGE_PATH).convert()

        self.map_dic = {
            MapInfo.WALL.value: wall,
            MapInfo.ROAD.value: road
        }

    def create_wall_list(self):
        for i in range(self.COLUMN_COUNT):
            for j in range(self.ROW_COUNT):
                if(self.map_data[j][i] != MapInfo.WALL.value):
                    continue
                
                x = i * constants.TILE_SIZE
                y = j * constants.TILE_SIZE
                
                wall_rect = pygame.Rect(x, y, constants.TILE_SIZE, constants.TILE_SIZE)
                
                self.wall_list.append(wall_rect)

    # 壁のRectのリストを返す
    def get_wall_list(self):
        return self.wall_list

    # 描画処理
    def draw(self, screen):
        # マップの設定情報に基づいてマップのタイルを描画
        for i in range(self.COLUMN_COUNT):
            for j in range(self.ROW_COUNT):
                # マップの設定情報をもとに描画するタイル画像を取得
                number = self.map_data[j][i] 
                image = self.map_dic[number] 
                x = i * constants.TILE_SIZE
                y = j * constants.TILE_SIZE
                # タイル画像を描画
                screen.blit(image, (x, y))