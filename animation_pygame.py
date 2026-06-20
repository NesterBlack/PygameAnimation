import pygame
from curves_animation import *
from parAnimation import *
from tabulate import tabulate


class Animation:
    def __init__(self, surface: pygame.Surface, name: str, anim_time_s: float, easing: str="linear", fps: int=60,
             close_after_end: bool=True, loop_count_after_close: int = 1, event_after_animation: pygame.event.Event=None,
             loop: bool=False, revers_for_loop: bool=False,

             par_positions: list = [Position(0,0,"linear", pygame.Vector2(0,0), pygame.Vector2(0,0))],
             par_rotations: list = Rotation(0,0,"linear", 0,0),
             par_scales: list = Scale(0,0,"linear", 1),
             par_transparencys: list = Transparency(0,0,"linear", 100,100),
             ):
        self.surface = surface
        self.name = name
        self.easing = easing

        self.event_after_animation = event_after_animation
        self.close_after_end = close_after_end
        self.loop_count_after_close = loop_count_after_close
        self.loop_count = 0
        self.is_playing = False
        self.is_revers = False

        self.loop = loop
        self.revers_for_loop = revers_for_loop

        self.anim_time = anim_time_s
        self.max_frame = int(anim_time_s * fps)
        self.current_frame = 0
        self.fps = fps

        self.positions = par_positions
        self.rotations = par_rotations
        self.scales = par_scales
        self.transparencys = par_transparencys

        self.all_frames = dict()
        for i in range(self.max_frame):
            self.all_frames[i] = {"position": None, "rotation": None, "scale": None, "transparency": None}

        for position in self.positions:
            position.fps = fps
            position.create_frames()
            for frame in position.frames:
                self.all_frames[frame]["position"] = position.frames[frame]

        for rotation in self.rotations:
            rotation.fps = fps
            rotation.create_frames()
            for frame in rotation.frames:
                self.all_frames[frame]["rotation"] = rotation.frames[frame]

        for scale in self.scales:
            scale.fps = fps
            scale.create_frames()
            for frame in scale.frames:
                self.all_frames[frame]["scale"] = scale.frames[frame]

        for transparency in self.transparencys:
            transparency.fps = fps
            transparency.create_frames()
            for frame in transparency.frames:
                self.all_frames[frame]["transparency"] = transparency.frames[frame]

        prev_position = pygame.Vector2(0,0)
        prev_rotation = 0
        prev_scale = 1
        prev_transparency = 100
        for frame in self.all_frames:
            if self.all_frames[frame]["position"] is None:
                self.all_frames[frame]["position"] = prev_position
            else:
                prev_position = self.all_frames[frame]["position"]

            if self.all_frames[frame]["rotation"] is None:
                self.all_frames[frame]["rotation"] = prev_rotation
            else:
                prev_rotation = self.all_frames[frame]["rotation"]

            if self.all_frames[frame]["scale"] is None:
                self.all_frames[frame]["scale"] = prev_scale
            else:
                prev_scale = self.all_frames[frame]["scale"]

            if self.all_frames[frame]["transparency"] is None:
                self.all_frames[frame]["transparency"] = prev_transparency
            else:
                prev_transparency = self.all_frames[frame]["transparency"]

    def __str__(self):
        text = f"Animation: {self.name}, fps:{self.fps}, easing: {self.easing}\n"
        text += f"Parameter:\n"
        if self.loop:
            text += "Loop"
        if self.revers_for_loop:
            text += "revers"
        if self.event_after_animation:
            text += f", event after animation: {self.event_after_animation}"
        if self.close_after_end:
            text += ", close after end"
        text += "\n"

        text += f"Frame: \n"

        headers = list(self.all_frames[0])
        rows = [list(f.values()) for f in self.all_frames.values()]

        text += tabulate(rows, headers, tablefmt="fancy_grid")

        return text

class Animator:
    def __init__(self, fps):
        self.fps = fps
        self.animations = dict()

    def play_animations(self, screen: pygame.Surface):
        for animation_name in self.animations:
            animation = self.animations[animation_name]
            if animation.is_playing:
                print("Starting animation " + animation_name, animation.loop_count)
                frames = animation.all_frames

                surface = animation.surface

                transparency = 255*(frames[animation.current_frame]["transparency"]/100)
                size_f = frames[animation.current_frame]["scale"]
                pos = frames[animation.current_frame]["position"]
                w_s, h_s = surface.get_size()

                surface = pygame.transform.rotozoom(surface, frames[animation.current_frame]["rotation"], size_f)
                rect = surface.get_rect(center=(pos.x+w_s//2, pos.y+h_s//2))

                surface.set_alpha(transparency)
                print(surface.get_alpha(), "transparency")

                screen.blit(surface, rect.topleft)
                if animation.current_frame != animation.max_frame-1 and not animation.is_revers:
                    animation.current_frame += 1
                    print(animation.current_frame, "0")

                if animation.current_frame != 0 and animation.is_revers:
                    animation.current_frame -= 1
                    print(animation.current_frame, "1")



                if animation.close_after_end and (not animation.loop or animation.loop_count == animation.loop_count_after_close) and (animation.current_frame == animation.max_frame-1 or animation.current_frame == 0):
                    animation.is_playing = False
                    print(animation.current_frame, "2")
                    return



                if animation.loop and (animation.current_frame == animation.max_frame-1 or animation.current_frame == 0):
                    if animation.is_revers:
                        self.start_animation(animation.name)
                        print(animation.current_frame, "3")
                    else:
                        self.start_reverse_animation(animation.name)
                        print(animation.current_frame, "4")
                    animation.loop_count += 1



                if animation.current_frame == animation.max_frame-1 and animation.event_after_animation:
                    pygame.event.post(animation.event_after_animation)


    def create_animation(self, surface: pygame.Surface, name: str, anim_time_s: float, easing: str="linear", fps: int=60,
             close_after_end: bool=True, loop_count_after_close: int = 1 , event_after_animation: pygame.event.Event=None,
             loop: bool=False, revers_for_loop: bool=False,

             par_positions: list = [Position(0, 0, "linear", pygame.Vector2(0, 0), pygame.Vector2(0, 0))],
             par_rotations: list = [Rotation(0, 0, "linear", 0, 0)],
             par_scales: list = [Scale(0, 0, "linear", 1)],
             par_transparencys: list = [Transparency(0, 0, "linear", 100, 100)],
             ):
        self.animations[name] = Animation(surface, name, anim_time_s, easing, fps, close_after_end, loop_count_after_close, event_after_animation, loop, revers_for_loop,
                                          par_positions, par_rotations, par_scales, par_transparencys)
        return self.animations[name]

    def start_animation(self, name):
        self.animations[name].is_playing = True
        self.animations[name].current_frame = 0

    def start_reverse_animation(self, name):
        self.animations[name].is_playing = True
        self.animations[name].is_revers = True
        self.animations[name].current_frame = self.animations[name].max_frame-1
        print(self.animations[name].is_revers, "revers")



