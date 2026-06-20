from unittest import case

import pygame
import pygame_gui
import pyperclip

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("AnimatoEditor")
font = pygame.font.SysFont("Arial", 10)
# manager = pygame_gui.UIManager(window_size)
clock = pygame.time.Clock()
offset = 0

# input_box = pygame_gui.elements.UITextEntryLine(
#     relative_rect=pygame.Rect((200, 120), (200, 40)),
#     manager=manager
# )
#
# # Кнопка
# button = pygame_gui.elements.UIButton(
#     relative_rect=pygame.Rect((250, 180), (100, 40)),
#     text='OK',
#     manager=manager
# )

class Parameter:
    def __init__(self, type, start_time, end_time, start_value, end_value, easing,):
        self.is_interact = False

        self.type = type
        match type:
            case "rotation":
                self.posY = 320
                self.color = "#EF4444"
            case "scale":
                self.posY = 376
                self.color = "#10B981"
            case "time_line":
                self.posY = 432
                self.color = "#EEEEFF"
            case "position":
                self.posY = 488
                self.color = "#FBBF24"
            case "transparency":
                self.posY = 544
                self.color = "#60A5FA"
            case _:
                raise "dont change this, no have this parameter"
        self.start_time = start_time
        self.end_time = end_time
        self.start_value = start_value
        self.end_value = end_value
        self.easing = easing

    def draw(self):
        posX_start = ((self.start_time / s_in_frame)*10*part_sc)-offset
        posX_end = ((self.end_time / s_in_frame)*10*part_sc)-offset
        if posX_end > 550:
            posX_end = 550
        rect = pygame.Rect(posX_start, self.posY, posX_end-posX_start, 56)
        pygame.draw.rect(screen, self.color, rect)
        posX_end = ((self.end_time / s_in_frame) * 10 * part_sc) - offset

        if not posX_end > 550:
            pygame.draw.line(screen, "#353839", (posX_end-15, self.posY+5), (posX_end-5, self.posY+28), 5)
            pygame.draw.line(screen, "#353839", (posX_end-15, self.posY+51), (posX_end-5, self.posY+28), 5)
        if self.type != "time_line":
            pygame.draw.line(screen, "#353839", (posX_start+15, self.posY+5), (posX_start+5, self.posY+28), 5)
            pygame.draw.line(screen, "#353839", (posX_start+15, self.posY+51), (posX_start+5, self.posY+28), 5)

        if self.is_interact:
            pygame.draw.rect(screen, "#1D4ED8", rect, 5)

        if pygame.mouse.get_pressed(3)[0]:
            self.is_change_size(pygame.mouse.get_pos())

    def click_on(self, mouse_pos: tuple[int, int]):
        posX_end = ((self.end_time / s_in_frame)*10*part_sc)-offset
        posX_start = ((self.start_time / s_in_frame)*10*part_sc)-offset
        if posX_start<=mouse_pos[0]-offset<=posX_end and self.posY<=mouse_pos[1]<=self.posY+56:
            self.is_interact = True
            return True
        self.is_interact = False
        return False

    def is_change_size(self, mouse_pos: tuple[int, int]):
        posX_end = ((self.end_time / s_in_frame) * 10 * part_sc) - offset
        if posX_end-15 <= mouse_pos[0]-offset <= posX_end-5 and self.posY<=mouse_pos[1]<=self.posY+56:
            posX_end = mouse_pos[0]+10-offset
            # posX_end = ((self.end_time / s_in_frame) * 10 * part_sc) - offset
            self.end_time = ((posX_end*s_in_frame)/10/part_sc)+offset


class Parameters:
    def __init__(self):
        self.parameter = list()
    def draw(self):
        for parameter in self.parameter:
            parameter.draw()
    def create_parameter(self, type, start_time, end_time, start_value, end_value, easing,):
        self.parameter.append(Parameter(type, start_time, end_time, start_value, end_value, easing))


editor_rect_d = {"0": {"rect": pygame.Rect(0, 285, 550, 20), "color": "#4A4A4A"},
                 "1": {"rect": pygame.Rect(550, 0, 20, 800), "color": "#4A4A4A"}, }
parameters = Parameters()
parameters.create_parameter("rotation", 0, 0.5,0,0,"")
parameters.create_parameter("scale", 0, 1,0,0,"")
parameters.create_parameter("time_line", 0, 1.5,0,0,"")
parameters.create_parameter("position", 0, 2,0,0,"")
parameters.create_parameter("transparency", 0, 2.5,0,0,"")

part_sc = 2
s_in_frame = 0.1

temp_mouse_posX = 0
is_mouse_pressed = False

running = True
while running:
    # time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
        #     if event.ui_element == input_box:
        #         pass
        elif event.type == pygame.MOUSEWHEEL:
            part_sc += 1*event.y
            if part_sc <= 2:
                part_sc = 2
        elif pygame.mouse.get_pressed(3)[0]:
            mouse_posX = pygame.mouse.get_pos()[0]
            for parameter in parameters.parameter:
                if parameter.click_on(pygame.mouse.get_pos()):
                    interact_parameter = parameter
                    for parameter_i in parameters.parameter:
                        if parameter_i != interact_parameter:
                            parameter_i.is_interact = False
                    break
            else:
                if is_mouse_pressed:
                    offset -= mouse_posX-temp_mouse_posX
                    if offset < 0:
                        offset = 0
                temp_mouse_posX = mouse_posX
                is_mouse_pressed = True
        elif not pygame.mouse.get_pressed(3)[0]:
            is_mouse_pressed = False


        # manager.process_events(event)

    # manager.update(time_delta)
    screen.fill("#3A3A38")

    for i in range(-offset%20-20, 550, int(part_sc*10)):
        pygame.draw.line(screen, "#4B5563", (i, 305), (i, 600))

        text_surface = font.render(str(s_in_frame), True, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (i+10, 310)
        screen.blit(text_surface, text_rect)
    parameters.draw()

    for name_l in editor_rect_d:
        pygame.draw.rect(screen, editor_rect_d[name_l]["color"], editor_rect_d[name_l]["rect"])

    # manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
