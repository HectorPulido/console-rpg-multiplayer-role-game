from Class.GameWorld import GameWorld
from Class.GameObject import GameObject
from Class.Console import Console

game_world = GameWorld(10, 10)

PLAYER = "player"
player_stats = {"health": 100, "level": 1,
                "potential": 0.95, "attack": 10, "variability": 0.1}

player = GameObject(player_stats, "Jugador Hector")
game_world.add_world_object(player, PLAYER, 0, 1)

console = Console(game_world)


while True:
    command = input(">> Player: ")
    resp = console.execute_command(command, PLAYER)
    print(resp)
