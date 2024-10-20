import pygame

from enum import Enum
from game import constants
from game.goal import Goal
from game.maze_map import Map
from game.character import Character

# マップの配置情報の設定値
class Configuration(Enum):
    # キャラクターの開始位置
    CHARACTER_START_POSITION = 1
    # ゴール
    GOAL = 2

# ゲームの状態
class GameState(Enum):
    # ゲームプレイ中
    GAMING = 0
    # ゲームオバー（壁に触れた場合）
    GAME_OVER = 1
    # ゲームクリア（ゴールに到着した場合）
    GAME_CLEAR = 2
    # ゲームを終了中
    CLOSING = 4

class MazeGame:
    def __init__(self, map_data, configuration_data):
        # TODO 引数の検証処理を追加
        # リストが空の場合
        # 行または列が0
        # 二つの二次元配列のサイズが異なる場合
        if not has_same_array_size(map_data, configuration_data):
            return
        
        # pygameの初期化処理
        pygame.init()
        # ゲーム画面のタイトルを変更
        pygame.display.set_caption('MazeExplore')
        
        # ゲームマップの行数
        map_row_count = len(map_data)
        # ゲームマップの列数
        map_column_count = len(map_data[0])
        
        # ゲーム画面の横幅（マップ情報列数×タイルサイズ）
        self.__SCREEN_WIDTH = map_column_count * constants.TILE_SIZE
        # ゲーム画面の縦幅（マップ情報行数×タイルサイズ）
        self.__SCREEN_HEIGHT = map_row_count * constants.TILE_SIZE
        # ゲームウィンドウの作成
        self.__screen = pygame.display.set_mode((self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT))
        
        # ゲーム画面のアイコンの設定
        icon = pygame.image.load(constants.GAME_ICON_PATH).convert()
        pygame.display.set_icon(icon)

        # ゲームの状態管理
        self.__game_state = GameState.GAMING

        # ゲーム時間管理オブジェクト
        self.__clock = pygame.time.Clock()
        
        # ゲームマップの初期化
        self.__map = Map(map_data)
        
        # マップ配置データからキャラクターの初期座標を取得
        character_start_pos = get_configuration_position(configuration_data, Configuration.CHARACTER_START_POSITION)
        # キャラクターの初期化
        self.__character = Character(character_start_pos, self.__map.get_wall_list())
        
        # マップ配置データからゴールの初期座標を取得
        goal_position = get_configuration_position(configuration_data, Configuration.GOAL)
        # ゴールの初期化
        self.__goal = Goal(goal_position)
        
        # メッセージを描画するフォントを設定
        # game_font = pygame.font.SysFont(None, 80)
        game_font = pygame.font.Font('game/fonts/Silkscreen-Regular.ttf', 42)
        # ゲームクリアメッセージ画像の生成
        self.__game_clear_text = game_font.render("Game Clear!", False, (230, 255, 148), (0, 103, 105))
        # self.__game_clear_text = game_font.render("Game Clear!", False, (255, 251, 230), (0, 103, 105))
        
        # ゲームオーバーメッセージ
        self.__game_over_text = game_font.render("Game Over!", False, (243, 254, 184), (255, 76, 76))

    def main(self, character_commands):
        # キャラクターに動かすコマンドを登録
        self.__character.add_commands(character_commands)

        # ゲームループ
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__game_state = GameState.CLOSING
                    running = False
                    
            # ゲームのステートを更新
            self.change_game_state()

            # ゲーム画面のリセット
            self.__screen.fill((255, 255, 255))
            
            # マップの描画
            self.__map.draw(self.__screen)
            # キャラクターの描画
            self.__character.draw(self.__screen)
            # ゴールの描画
            self.__goal.draw(self.__screen)
            
            if self.__game_state == GameState.GAME_OVER:
                self.__character.set_game_over()
                self.draw_text_centered(self.__game_over_text, True)
            elif self.__game_state == GameState.GAME_CLEAR:
                self.__character.set_game_over()
                self.draw_text_centered(self.__game_clear_text, True)
            elif self.__game_state == GameState.CLOSING:
                self.__character.set_game_over()

            # 画面を更新
            pygame.display.update()

            # ゲームのFPSを設定
            self.__clock.tick(constants.FRAME_RATE)
    
    def change_game_state(self):
        if(self.__character.is_hitting_wall()
           and self.__character.is_idle_state()):
            self.__game_state = GameState.GAME_OVER
            
        if(self.__character.is_hitting(self.__goal.get_rect())
           and self.__character.is_idle_state()):
            self.__game_state = GameState.GAME_CLEAR
    
    # 
    def draw_text_centered(self, text_surface:pygame.Surface, drawBorder:bool):
        text_rect = text_surface.get_rect(center=(self.__SCREEN_WIDTH//2,self.__SCREEN_HEIGHT//2))
        
        if drawBorder:
            border_size = 2
            border_rect = pygame.Rect(text_rect.x - border_size, text_rect.y - border_size,
                                    text_rect.width + border_size * 2, text_rect.height + border_size * 2)
            pygame.draw.rect(self.__screen, (230, 230, 230), border_rect)
        
        self.__screen.blit(text_surface, text_rect)

# 引数で受け取った二次元配列が同じ行数・列数かを判定する
def has_same_array_size(first_2d_array: list[list[int]], second_2d_array: list[list[int]]) -> bool:   
    # 行数が一致しない場合の処理
    if len(first_2d_array) != len(second_2d_array):
        return False

    # 列数が一致しない場合の処理
    if len(first_2d_array[0]) != len(second_2d_array[0]):
        return False
    
    return True

# マップ設定情報から引数で指定した設定値検索して、ゲームマップの座標情報（x ,y)として返す
def get_configuration_position(configuration_data:list[list[int]], configType:Configuration) -> pygame.Vector2:
    max_i = len(configuration_data[0])
    max_j = len(configuration_data)
    
    # 二次元配列の列方向を制御（x座標）
    for i in range(max_i):
        # 二次元配列の行方向を制御（y座標）
        for j in range(max_j):
            if configuration_data[j][i] == configType.value:
                return pygame.Vector2(i * constants.TILE_SIZE, j  * constants.TILE_SIZE)
