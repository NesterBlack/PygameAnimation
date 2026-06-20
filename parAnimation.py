import pygame
from curves_animation import *


class Parameter:
    def __init__(self):
        self.start_time = 0
        self.end_time = 1

        self.start_value = 0
        self.end_value = 1

        self.easing = "linear"

        self.fps = 60
        self.frames = dict()

    def create_frames(self):
        self.start_frame = self.start_time * self.fps
        max_frame = ((self.end_time - self.start_time) * self.fps)-1

        for i in range(max_frame+1):
            try:
                eased = globals()[self.easing](i / max_frame)
            except KeyError:

                eased = globals()["linear"](i / max_frame)


            self.frames[self.start_frame + i] = self.start_value + (self.end_value - self.start_value) * eased


class Position(Parameter):
    def __init__(self, start_time: int, end_time: int, easing: str, start_pos: pygame.Vector2, end_pos: pygame.Vector2):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

        self.easing = easing

        self.start_value = start_pos
        self.end_value = end_pos


class Rotation(Parameter):
    def __init__(self, start_time: int, end_time: int, easing: str, start_angle: float, end_angle: float):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

        self.easing = easing

        self.start_value = start_angle
        self.end_value = end_angle

class Scale(Parameter):
    def __init__(self, start_time: int, end_time: int, easing: str, scale: float):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

        self.easing = easing

        self.start_value = 1
        self.end_value = scale

class Transparency(Parameter):
    def __init__(self, start_time: int, end_time: int, easing: str, start_transparency: float, end_transparency: float):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time

        self.easing = easing

        self.start_value = start_transparency
        self.end_value = end_transparency
