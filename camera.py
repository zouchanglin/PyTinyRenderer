from vector import Vec3


class Camera:
    def __init__(self, eye_p: Vec3 = Vec3([0, 0, 0]),
                 world_up: Vec3 = Vec3([0, 1, 0]),
                 front: Vec3 = Vec3([0, 0, -1])):
        self.position = eye_p
        self.word_up = world_up
        self.front = front.normalize()
        self.right = self.front.cross(self.word_up).normalize()
        self.up = self.right.cross(self.front).normalize()
