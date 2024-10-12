import pygame

from game import constants
from game.spritesheet import Spritesheet

class Goal:
    def __init__(self, position:pygame.Vector2):
        self.frame_count = 0
        self.animation_frame_rate = 4
        self.position = position
        
        # キャラクター画像のスプライトシートを生成
        my_spritesheet = Spritesheet('game/assets/select01.png')

        # 移動アニメーションの定義
        self.animation = [my_spritesheet.get_sprite(0, 0, 32, 32),
                      my_spritesheet.get_sprite(32, 0, 32, 32),
                      my_spritesheet.get_sprite(64, 0, 32, 32),
                      my_spritesheet.get_sprite(96, 0, 32, 32)]

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, constants.TILE_SIZE, constants.TILE_SIZE)

    # 描画処理
    def draw(self, screen):
        self.frame_count += 1

        if self.frame_count >= self.animation_frame_rate * len(self.animation):
            self.frame_count = 0
        
        index = int(self.frame_count / self.animation_frame_rate)

        # TODO 無理やりサイズを合わせているが、もとの画像のサイズを調整すれば不要になる
        scaled_image = pygame.transform.scale(self.animation[index],(constants.TILE_SIZE, constants.TILE_SIZE))
        # キャラクターの描画処理    
        screen.blit(scaled_image, self.position)