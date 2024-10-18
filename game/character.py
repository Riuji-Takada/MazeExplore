import threading
import pygame
import asyncio

from game import constants
from game.spritesheet import Spritesheet
from enum import Enum

# キャラクターの状態
class CharacterState(Enum):
    # 静止状態
    IDLE = 1
    # 移動状態
    MOVING = 2

# キャラクターが向いている方向
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def get_min_value(cls):
        return min(cls, key=lambda member: member.value)
    
    @classmethod
    def get_max_value(cls):
        return max(cls, key=lambda member: member.value)
    
    def from_value(value: int):
        try:
            return Direction(value)
        except ValueError:
            raise ValueError(f"指定された値 '{value}' に対応する列挙子がありません")

direction_pos = {
    Direction.UP:pygame.Vector2(0, -constants.TILE_SIZE),
    Direction.DOWN:pygame.Vector2(0, constants.TILE_SIZE),
    Direction.LEFT:pygame.Vector2(-constants.TILE_SIZE, 0),
    Direction.RIGHT:pygame.Vector2(constants.TILE_SIZE, 0)
}

class Character:
    def __init__(self, start_position:pygame.Vector2, wall_list):
        self.COMMAND_INTERVAL = 0.6
        self.__speed = 5
        self.__frame_count = 0
        self.__animation_frame_rate = 20
        self.__position = start_position
        self.__next_position = start_position
        self.__state = CharacterState.IDLE
        self.__direction = Direction.UP
        self.__is_game_over = False
        self.__is_game_clear = False
        self.__wall_list = wall_list

        self.create_animations()
        
    def create_animations(self):
        # キャラクター画像のスプライトシートを生成
        my_spritesheet = Spritesheet(constants.CHARACTER_IMAGE_PATH)

        # 移動アニメーションの定義
        moving_up = [
            my_spritesheet.get_sprite(96, 48, 48, 48),
            my_spritesheet.get_sprite(144, 48, 48, 48)
        ]
        moving_right = [
            my_spritesheet.get_sprite(96, 144, 48, 48),
            my_spritesheet.get_sprite(144, 144, 48, 48)
        ]
        moving_down = [
            my_spritesheet.get_sprite(96, 0, 48, 48),
            my_spritesheet.get_sprite(144, 0, 48, 48)
        ]
        moving_left = [
            my_spritesheet.get_sprite(96, 96, 48, 48),
            my_spritesheet.get_sprite(144, 96, 48, 48)
        ]
        self.moving_animation = [
            moving_up,
            moving_right,
            moving_down,
            moving_left
        ]

        # 静止アニメーションの定義
        idle_up = [
            my_spritesheet.get_sprite(0, 48, 48, 48),
            my_spritesheet.get_sprite(48, 48, 48, 48)
        ]
        idle_right = [
            my_spritesheet.get_sprite(0, 144, 48, 48),
            my_spritesheet.get_sprite(48, 144, 48, 48)
        ]
        idle_down = [
            my_spritesheet.get_sprite(0, 0, 48, 48),
            my_spritesheet.get_sprite(48, 0, 48, 48)
        ]
        idle_left = [
            my_spritesheet.get_sprite(0, 96, 48, 48),
            my_spritesheet.get_sprite(48, 96, 48, 48)
        ]
        self.idle_animation = [
            idle_up,
            idle_right,
            idle_down,
            idle_left
        ]
    
    def add_commands(self, commands):
        thread = threading.Thread(target=lambda: asyncio.run(commands(self)))
        thread.start()
        
    def is_idle_state(self):
        return self.__state == CharacterState.IDLE

    def is_hitting(self, target:pygame.Rect):
        return self.get_rect().colliderect(target)
    
    def is_hitting_wall(self):
        return self.get_rect().collidelist(self.__wall_list) >= 1
    
    def set_game_over(self):
        self.__is_game_over = True
        
    def set_game_clear(self):
        self.__is_game_clear = True
        
    async def is_game_clear(self):
        if self.__is_game_over:
            return True
        
        await self.__wait_until_idle()
        
        return self.__is_game_clear

    def get_rect(self):
        return pygame.Rect(self.__position.x, self.__position.y, constants.TILE_SIZE, constants.TILE_SIZE)

    async def move_forward(self):
        if not self.__can_move():
            return
        
        await self.__wait_until_idle()
        
        next_position = self.__position + direction_pos[self.__direction]
        
        self.__next_position = next_position
        
        await asyncio.sleep(self.COMMAND_INTERVAL)
    
    # キャラクターの向いている方向を右に90度回転
    async def turn_right(self):
        if not self.__can_move():
            return
        
        await self.__wait_until_idle()
        
        next_direction = self.__direction.value + 1

        if(next_direction > Direction.get_max_value().value):
            next_direction = Direction.get_min_value().value

        self.__direction = Direction.from_value(next_direction)
        
        await asyncio.sleep(self.COMMAND_INTERVAL)

    # キャラクターの向いている方向を左に90度回転
    async def turn_left(self):
        if not self.__can_move():
            return
        
        await self.__wait_until_idle()
        
        next_direction = self.__direction.value - 1

        if(next_direction < Direction.get_min_value().value):
            next_direction = Direction.get_max_value().value

        self.__direction = Direction.from_value(next_direction)
        
        await asyncio.sleep(self.COMMAND_INTERVAL)

    async def turn_around(self):
        if not self.__can_move():
            return
        
        await self.__wait_until_idle()
        
        next_direction = self.__direction.value + 2

        if(next_direction > Direction.get_max_value().value):
            next_direction = Direction.get_min_value().value

        self.__direction = Direction.from_value(next_direction)
        
        await asyncio.sleep(self.COMMAND_INTERVAL)
        
    async def can_move_forward(self):
        # ゲームを強制終了する場合はFalseを返す
        if not self.__can_move():
            return False
        
        await self.__wait_until_idle()
        
        forward_position = self.__position + direction_pos[self.__direction]
        position_rect = pygame.Rect(forward_position.x, forward_position.y, constants.TILE_SIZE, constants.TILE_SIZE)
        
        hasWall = position_rect.collidelist(self.__wall_list) == -1
        return hasWall
    
    async def can_move_right(self):
        # ゲームを強制終了する場合はFalseを返す
        if not self.__can_move():
            return False
        
        await self.__wait_until_idle()
        
        right_direction_value = self.__direction.value + 1

        if(right_direction_value > Direction.get_max_value().value):
            right_direction_value = Direction.get_min_value().value
            
        right_direction = Direction.from_value(right_direction_value)
        
        right_position = self.__position + direction_pos[right_direction]
        position_rect = pygame.Rect(right_position.x, right_position.y, constants.TILE_SIZE, constants.TILE_SIZE)
        
        hasWall = position_rect.collidelist(self.__wall_list) == -1
        return hasWall
    
    async def can_move_left(self):
        # ゲームを強制終了する場合はFalseを返す
        if not self.__can_move():
            return False
        
        await self.__wait_until_idle()
        
        left_direction_value = self.__direction.value - 1

        if(left_direction_value < Direction.get_min_value().value):
            left_direction_value = Direction.get_max_value().value
            
        left_direction = Direction.from_value(left_direction_value)
            
        left_position = self.__position + direction_pos[left_direction]
        position_rect = pygame.Rect(left_position.x, left_position.y, constants.TILE_SIZE, constants.TILE_SIZE)
        
        hasWall = position_rect.collidelist(self.__wall_list) == -1
        return hasWall
    
    def __can_move(self):
        if self.__is_game_clear or self.__is_game_over:
            return False
        return True
    
    async def __wait_until_idle(self):
        # ゲームを終了する場合は何も処理しない
        while(self.__can_move() and self.__state != CharacterState.IDLE):
            await asyncio.sleep(0.3)

    def __update_state(self):
        # 次の目的座標と現在の座標の距離を算出
        distance = self.__position.distance_to(self.__next_position)
        
        if distance == 0:
            self.__state = CharacterState.IDLE
        else:
            self.__state = CharacterState.MOVING

    def __update_direction(self):
        # キャラクターの移動方向を判定
        direction = self.__next_position - self.__position

        if direction.x > 0:
            self.__direction = Direction.RIGHT
        elif direction.x < 0:
            self.__direction = Direction.LEFT
        elif direction.y > 0:
            self.__direction = Direction.DOWN
        elif direction.y < 0:
            self.__direction = Direction.UP
    
    # 描画処理
    def draw(self, screen):
        self.__frame_count += 1
        
        # キャラクターの移動処理（座標変更）
        if self.__can_move():
            self.__position = self.__position.move_towards(self.__next_position, self.__speed)
        
        # キャラクターの状態（ステート）を更新
        self.__update_state()
        
        # キャラクターの向きを更新
        self.__update_direction()

        # アニメーションの種類を決定
        animation = None
        if self.__state == CharacterState.IDLE:
            animation = self.idle_animation[self.__direction.value]
        else:
            animation = self.moving_animation[self.__direction.value]
        
        if self.__frame_count >= self.__animation_frame_rate * len(animation):
                self.__frame_count = 0

        index = int(self.__frame_count / self.__animation_frame_rate)

        # TODO 無理やりサイズを合わせているが、もとの画像のサイズを調整すれば不要になる
        scaled_image = pygame.transform.scale(animation[index],(constants.TILE_SIZE, constants.TILE_SIZE))
        # キャラクターの描画処理    
        screen.blit(scaled_image, self.__position)
        
        # デバッグ用
        pygame.draw.rect(screen, (255,255,0), self.get_rect(), 1)