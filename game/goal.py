import pygame

from game import constants
from game.spritesheet import Spritesheet

class Goal:
    def __init__(self, position:pygame.Vector2):
        self.__frame_count = 0
        # アニメーションのフレームレートを設定
        self.__animation_frame_rate = 4
        # ゴールの座標
        self.__position = position
        
        # キャラクター画像のスプライトシートを生成
        my_spritesheet = Spritesheet(constants.GOAL_IMAGE_PATH)

        # アニメーションの定義
        self.__animation = [
            my_spritesheet.get_sprite(0, 0, 32, 32),
            my_spritesheet.get_sprite(32, 0, 32, 32),
            my_spritesheet.get_sprite(64, 0, 32, 32),
            my_spritesheet.get_sprite(96, 0, 32, 32)
        ]
        
        # フレームカウンターの最大値
        self.MAX_FRAME_COUNT = self.__animation_frame_rate * len(self.__animation)

    def get_rect(self):
        return pygame.Rect(self.__position.x, self.__position.y, constants.TILE_SIZE, constants.TILE_SIZE)

    # 描画処理
    def draw(self, screen):
        self.__frame_count += 1

        # フレームカウンターのリセット
        if self.__frame_count >= self.MAX_FRAME_COUNT:
            self.__frame_count = 0
        
        # 表示する
        index = int(self.__frame_count / self.__animation_frame_rate)

        # 画像をタイルサイズにサイズ変更
        scaled_image = pygame.transform.scale(self.__animation[index],(constants.TILE_SIZE, constants.TILE_SIZE))
        
        # キャラクターの描画処理    
        screen.blit(scaled_image, self.__position)