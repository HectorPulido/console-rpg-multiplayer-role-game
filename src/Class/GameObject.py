import random


class GameObject:
    def __init__(self, properties: dict, description: str, callbacks: dict):
        self.properties = properties
        self.description = description
        self.callbacks = callbacks

    def calc_damage(self, other_defense: int): 
        if "attack" not in self.properties:
            return None
        if "level" not in self.properties:
            return None
        if "potential" not in self.properties:
            return None
        if "variability" not in self.properties:
            return None

        damage = self.properties["attack"] * self.properties["level"] \
            * self.properties["potential"]

        variability = self.properties["variability"]
        dev = random.uniform(-variability, variability)

        final_damage = damage * (1 + dev)

        return final_damage - other_defense

    def check_health(self):
        if "health" not in self.properties:
            return None

        is_alive = self.properties["health"] > 0

        if "on_die" not in self.callbacks:
            return None

        self.callbacks["on_die"]()

        return is_alive

    def attack(self, other):
        if "health" not in self.properties:
            return None
        if "health" not in other.properties:
            return None

        self_defense = self.properties.get("defense", 0)
        other_defense = other.properties.get("defense", 0)

        self_damage = self.calc_damage(self_defense)
        other_damage = other.calc_damage(other_defense)

        if self_damage is not None:
            other.properties["health"] -= self_damage

        if other_damage is not None:
            self.properties["health"] -= other_damage

        return self_damage, other_damage

    def __str__(self):
        return self.description
