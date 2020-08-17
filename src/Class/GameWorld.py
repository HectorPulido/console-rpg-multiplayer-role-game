class GameWorld():
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.world_objects = {}
        self.world_map = [[None for j in range(height)] for i in range(width)]

    def regularize_coordinates(self, x: int, y: int):
        if x < 0:
            x = self.width + x
        if y < 0:
            y = self.height + y

        x = x % self.width
        y = y % self.width

        return x, y

    def get_description_of_identifier(self, identifier):
        return self.world_objects[identifier]["obj"].description

    def get_data_of_point_relative(self, identifier, x: int, y: int):
        object_to_move = self.world_objects[identifier]
        x = object_to_move["x"] + x
        y = object_to_move["y"] + y
        x, y = self.regularize_coordinates(x, y)
        return self.world_map[x][y]

    def get_data_of_point(self, x: int, y: int):
        x, y = self.regularize_coordinates(x, y)
        return self.world_map[x][y]

    def get_data_arround_a_point_identifier(self, identifier: str):
        object_to_move = self.world_objects[identifier]
        x = object_to_move["x"]
        y = object_to_move["y"]
        return self.get_data_arround_a_point(x, y)

    def get_data_arround_a_point(self, x: int, y: int):
        north = self.get_data_of_point(x, y + 1)
        south = self.get_data_of_point(x, y - 1)
        west = self.get_data_of_point(x - 1, y)
        east = self.get_data_of_point(x + 1, y)
        return north, south, west, east

    def add_world_object(self, object_to_instantiate, identifier: str, x: int, y: int):
        if self.get_data_of_point(x, y) is not None:
            return False

        x, y = self.regularize_coordinates(x, y)

        self.world_objects[identifier] = {
            "obj": object_to_instantiate,
            "x": x,
            "y": y
        }
        self.world_map[x][y] = identifier

        return True

    def move_object_relative(self, identifier: str, x_relative: int, y_relative: int):
        object_to_move = self.world_objects[identifier]
        x = object_to_move["x"] + x_relative
        y = object_to_move["y"] + y_relative

        x, y = self.regularize_coordinates(x, y)

        if self.get_data_of_point(x, y) is not None:
            return False

        self.world_map[object_to_move["x"]][object_to_move["y"]] = None

        object_to_move["x"] = x
        object_to_move["y"] = y
        self.world_map[x][y] = identifier
        self.world_objects[identifier] = object_to_move

        if self.get_data_of_point(x, y) is not None:
            return True

    def destroy_object(self, identifier: str):
        object_to_move = self.world_objects[identifier]
        x = object_to_move["x"]
        y = object_to_move["y"]
        self.world_map[x][y] = None
        return self.world_objects.pop(identifier)
