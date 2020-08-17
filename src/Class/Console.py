import random
from Class.GameObject import GameObject


class Console:
    def __init__(self, game_world):
        self.game_world = game_world

        self.prefabs = {
            "rock": {
                "count": 5,
                "stats":  {"health": 100},
                "description": "Es solo una roca, no tiene mucho mas",
                "name": "rock"
            }
        }

        self.commands = {
            "mover": self.move,
            "equipo": self.equipment,
            "info": self.info,
            "atacar": self.attack,
            "inspeccionar": self.inspect
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

        self.text = {
            "nothing_in_that_direction": "No hay nada en la direccion {direction}",
            "direction_doesnt_exist": "La direccion {direction} no existe",
            "correct_movement": "Te has movido a {direction} correctamente",
            "cant_move": "No se pudo mover correctamente, algo bloquea el paso en {direction}",
            "arround_info": "Informacion de {identifier}: Al norte hay {north}, al sur {south}, al este {east} y al oeste {west}",
            "object_not_attackable": "Este objeto no es atacable",
            "attack_summary_something_destroyed": "{data_in_point} recibio {self_damage} puntos de daño, {identifier} recibio {other_damage}, {data_in_point} fue destruido por {identifier}",
            "attack_summary_something_destroyed_inverted": "{data_in_point} recibio {self_damage} puntos de daño, {identifier} recibio {other_damage}, {data_in_point} fue destruido por {identifier}",
            "attack_summary": "{data_in_point} recibio {self_damage} puntos de daño, {identifier} recibio {other_damage}"
        }

        self.instantiate_prefabs(self.prefabs)

        
    def instantiate_prefabs(self, prefabs):
        for prefab in prefabs.values():
            print(prefab)
            self.instantiate_prefab(prefab)

    def instantiate_prefab(self, data_pref: dict):
        count = data_pref["count"]
        stats = data_pref["stats"]
        description = data_pref["description"]
        name = data_pref["name"]

        for i in range(count):
            rock = GameObject(stats, description)
            while True:
                position = (random.randint(0, self.game_world.width),
                            random.randint(0, self.game_world.height))
                if self.game_world.get_data_of_point(*position) is None:
                    self.game_world.add_world_object(
                        rock, name + f"_{i}", *position)
                    break

    def execute_command(self, command: str, identifier: str):
        command_striped = command.lower().strip().split(" ")

        for key, callback in self.commands.items():
            if key.lower() == command_striped[0]:
                return callback(command_striped, identifier)

    def move(self, commands: list, identifier: str):
        direction = commands[1]
        if direction in self.dict["coordinates"]:
            if self.game_world.move_object_relative(identifier, *self.dict["coordinates"][direction]):
                return self.text["correct_movement"].format(direction=direction)
            else:
                return self.text["cant_move"].format(direction=direction)
        return self.text["direction_doesnt_exist"].format(direction=direction)

    def info(self, commands: list, identifier: str):
        north, south, west, east = self.game_world.get_data_arround_a_point_identifier(
            identifier)
        return self.text["arround_info"].format(identifier=identifier, north=north, south=south, east=east, west=west)

    def equipment(self, commands: list, identifier: str):
        return self.game_world.world_objects[identifier]["obj"]

    def inspect(self, commands: list, identifier: str):
        direction = commands[1]
        if direction in self.dict["coordinates"]:
            data_point = self.game_world.get_data_of_point_relative(
                identifier, *self.dict["coordinates"][direction])
            if data_point is None:
                return self.text["nothing_in_that_direction"].format(direction=direction)
            return self.game_world.get_description_of_identifier(data_point)
        return self.text["direction_doesnt_exist"].format(direction=direction)

    def attack(self, commands: list, identifier: str):
        direction = commands[1]
        if direction in self.dict["coordinates"]:
            data_in_point = self.game_world.get_data_of_point_relative(
                identifier, *self.dict["coordinates"][direction])

            if data_in_point is None:
                return self.text["nothing_in_that_direction"].format(direction=direction)

            attacked = self.game_world.world_objects[data_in_point]["obj"]
            attacker = self.game_world.world_objects[identifier]["obj"]

            damage_info = attacker.attack(attacked)

            if damage_info is None:
                return self.text["object_not_attackable"]

            self_damage, other_damage = damage_info
            self_damage = int(self_damage) if self_damage is not None else 0
            other_damage = int(other_damage) if other_damage is not None else 0

            check_health_attacked = attacked.check_health()
            if check_health_attacked is not None:
                if check_health_attacked == False:
                    self.game_world.destroy_object(data_in_point)
                    return self.text["attack_summary_something_destroyed"].format(data_in_point=data_in_point,
                                                                                  self_damage=self_damage,
                                                                                  identifier=identifier,
                                                                                  other_damage=other_damage)

            check_health_attacker = attacker.check_health()
            if check_health_attacker is not None:
                if check_health_attacker == False:
                    self.game_world.destroy_object(identifier)
                    return self.text["attack_summary_something_destroyed_inverted"].format(data_in_point=data_in_point,
                                                                                           self_damage=self_damage,
                                                                                           identifier=identifier,
                                                                                           other_damage=other_damage)

            return self.text["attack_summary"].format(data_in_point=data_in_point, self_damage=self_damage,
                                                      identifier=identifier, other_damage=other_damage)

        return self.text["direction_doesnt_exist"].format(direction=direction)
