
PLAYER_SPEED = 3

class Player():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.angle = 0
        self.move_forward = 0
        self.move_backward = 0
        self.max_ray_length = 150
        self.nb_ray = 5
        self.fov = 100 # in degrees