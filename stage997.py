import asyncio
from game.main import MazeGame
from game.character import Character

map_data = [
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0],
    [0,0,1,1,1,1,1,0,1,0,0],
    [0,0,1,0,1,0,1,0,1,0,0],
    [0,0,1,0,1,1,1,1,1,0,0],
    [0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0]
]

configuration_data = [
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0]
]

if __name__ == '__main__':
    game = MazeGame(map_data, configuration_data)

    async def move_character(self:Character):
        # この下に命令を入力します
        while(not await self.is_game_clear()):
            if await self.can_move_right():
                await self.turn_right()
                await self.move_forward()
                continue
            
            if await self.can_move_forward():
                await self.move_forward()
            elif await self.can_move_left():
                await self.turn_left()
            else:
                await self.turn_around()

    game.main(move_character)