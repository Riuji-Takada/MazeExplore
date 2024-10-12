import pygame

from game import constants
from game.character import Character
from game.goal import Goal
from game.maze_map import Map
from enum import Enum

class Configuration(Enum):
    CHARACTER_START_POSITION = 1
    GOAL = 2
    
class GameState(Enum):
    GAMING = 0
    GAME_OVER = 1
    GAME_CLEAR = 2
    CLOSING = 4

class MazeGame:
    def __init__(self, map_data, configuration_data):
        # 画面サイズの算出
        self.SCREEN_WIDTH = len(map_data[0]) * constants.TILE_SIZE
        self.SCREEN_HEIGHT = len(map_data) * constants.TILE_SIZE
        
        self.game_state = GameState.GAMING

        # ゲーム画面の初期化
        # pygameの初期化処理
        pygame.init()

        # ゲームウィンドウの作成
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        # ゲーム画面のタイトルを変更
        pygame.display.set_caption('ゲームタイトル')

        # ゲーム画面のアイコンの設定
        icon = pygame.image.load('game/assets/maze.png').convert()
        pygame.display.set_icon(icon)
        
        # ゲームマップの初期化
        self.__map = Map(map_data)
        
         # キャラクターの初期化
        character_start_pos = get_configuration_position(configuration_data, Configuration.CHARACTER_START_POSITION)
        self.__character = Character(character_start_pos, self.__map.get_wall_list())
        
        # ゴールの初期化
        goal_position = get_configuration_position(configuration_data, Configuration.GOAL)
        self.__goal = Goal(goal_position)
        
        game_font = pygame.font.SysFont(None, 120)
        # ゲームクリアメッセージ画像の生成
        self.game_clear_text = game_font.render("Game Clear!", False, (0, 0, 0), (255, 255, 255))
        
        # ゲームオーバーメッセージ
        self.game_over_text = game_font.render("Game Over!", False, (0, 0, 0), (255, 255, 255))

    def main(self, character_commands):
        # キャラクターに動かすコマンドを登録
        self.__character.add_commands(character_commands)

        # ゲームループ
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.CLOSING
                    running = False
                    
            # ゲームのステートを更新
            self.change_game_state()

            # ゲーム画面のリセット
            self.screen.fill((255, 255, 255))
            
            # マップの描画
            self.__map.draw(self.screen)
            # キャラクターの描画
            self.__character.draw(self.screen)
            # ゴールの描画
            self.__goal.draw(self.screen)
            
            if self.game_state == GameState.GAME_OVER:
                self.__character.set_game_over()
                self.draw_text_centered(self.game_over_text)
            elif self.game_state == GameState.GAME_CLEAR:
                self.__character.set_game_over()
                self.draw_text_centered(self.game_clear_text)
            elif self.game_state == GameState.CLOSING:
                self.__character.set_game_over()
            
            # デバッグ用
            pygame.draw.rect(self.screen, (255,0,0), self.__character.get_rect(), 1)

            pygame.display.update()

            self.clock.tick(60)
    
    def change_game_state(self):
        if(self.__character.is_hitting_wall() & self.__character.is_idle_state()):
            self.game_state = GameState.GAME_OVER
            
        if(self.__character.is_hitting(self.__goal.get_rect()) & self.__character.is_idle_state()):
            self.game_state = GameState.GAME_CLEAR
            
    def draw_text_centered(self, text_surface:pygame.Surface):
        text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2,self.SCREEN_HEIGHT//2))
        self.screen.blit(text_surface, text_rect)

def get_configuration_position(configuration_data, configType:Configuration):
    for i in range(len(configuration_data[0])):
        for j in range(len(configuration_data)):
            if configuration_data[j][i] == configType.value:
                return pygame.Vector2(i * constants.TILE_SIZE, j  * constants.TILE_SIZE)
