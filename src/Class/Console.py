class Console:
    def __init__(self, game_world):
        self.game_world = game_world

        self.commands = {
            "mover" : self.move,
            "equipo" : self.equipment,
            "info" : self.info,
            "atacar": self.attack
        }

        self.dict = {
            "coordinates": {
                "norte": (0, 1),
                "sur": (0, -1),
                "este": (1, 0),
                "oeste": (-1, 0),
                "arriba": (0, 1),
                "abajo": (0, -1),
                "derecha": (1, 0),
                "izquierda": (-1, 0),
            }
        }

    def execute_command(self, command: str, identifier: str):
        command_striped = command.lower().strip().split(" ")

        for key, callback in self.commands.items():
            if key.lower() == command_striped[0]:
                return callback(command_striped, identifier)

    def move(self, commands: list, identifier: str):
        direction = commands[1]
        if direction in self.dict["coordinates"]:
            if self.game_world.move_object_relative(identifier, *self.dict["coordinates"][direction]):
                return f"Te has movido a {direction} correctamente"
            else:
                return f"No se pudo mover correctamente, algo bloquea el paso en {direction}"
        return f"La direccion {direction} no existe"

    def info(self, commands: list, identifier: str):
        north, south, west, east = self.game_world.get_data_arround_a_point_identifier(identifier)
        return f"Informacion de {identifier}: Al norte hay {north}, al sur {south}, al este {east} y al oeste {west}"

    def equipment(self, commands: list, identifier: str):
        return self.game_world.world_objects[identifier]["obj"]

    def attack(self, commands: list, identifier: str):
        direction = commands[1]
        if direction in self.dict["coordinates"]:
            data_in_point = self.game_world.get_data_of_point_relative(identifier, *self.dict["coordinates"][direction])

            if data_in_point is None:
                return f"No hay nada en la direccion {direction}"

            attacked = self.game_world.world_objects[data_in_point]["obj"]

            attacker = self.game_world.world_objects[identifier]["obj"]

            damage_info = attacker.attack(attacked)

            if damage_info is None:
                return f"Este objeto no es atacable"

            self_damage, other_damage = damage_info
            self_damage = int(self_damage) if self_damage is not None else 0
            other_damage = int(other_damage) if other_damage is not None else 0

            return f"{data_in_point} recibio {self_damage} puntos de daño, {identifier} recibio {other_damage} "


        return f"La direccion {direction} no existe"