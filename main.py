import pygame
from pygame.locals import *
import random


class Game():
    def __init__(self):
        self.topleft = (0, 0, 960, 540)
        self.topright = (960, 0, 960, 540)
        self.bottomleft = (0, 540, 960, 540)
        self.bottomright = (960, 540, 960, 540)
        self.white = [255, 255, 255]
        self.red = [255, 0, 0]
        self.green = [0, 255, 0]
        self.blue = [0, 0, 255]


class Background(Game):
    def __init__(self):
        super(Background, self).__init__()

    def start_hover(self, display):
        font = pygame.font.Font(size=100)
        correct_color = font.render('Start', True, self.white)
        # creates a new surface that is black and blit the correct_color onto it
        temp_surface = pygame.Surface(correct_color.get_size())
        temp_surface.fill((0, 0, 255))
        temp_surface.blit(correct_color, (0, 0))
        # blit the temp_surface onto the main screen
        temp_surface_rect = correct_color.get_rect(center=(1920 / 2, 1080 / 2))
        display.blit(temp_surface, temp_surface_rect)

        pygame.display.update()

    def start_background(self, display):
        pygame.draw.rect(display, self.white, self.topleft)
        pygame.draw.rect(display, self.red, self.topright)
        pygame.draw.rect(display, self.green, self.bottomleft)
        pygame.draw.rect(display, self.blue, self.bottomright)

        # creates the font object for the start and renders it
        font = pygame.font.Font(size=100)
        correct_color = font.render('Start', True, self.white)
        # creates a new surface that is black and blit the correct_color onto it
        temp_surface = pygame.Surface(correct_color.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(correct_color, (0, 0))
        # blit the temp_surface onto the main screen
        temp_surface_rect = correct_color.get_rect(center=(1920 / 2, 1080 / 2))
        display.blit(temp_surface, temp_surface_rect)

        pygame.display.update()

    def set_background(self, display, match_object, timer):
        # Sets the colors in each corner
        pygame.draw.rect(display, match_object.color_order[0], self.topleft)
        pygame.draw.rect(display, match_object.color_order[1], self.topright)
        pygame.draw.rect(display, match_object.color_order[2], self.bottomleft)
        pygame.draw.rect(display, match_object.color_order[3], self.bottomright)

        # creates the font object for the score and renders it
        font = pygame.font.Font(size=100)
        score_text = font.render(f'Score: {match_object}', True, (0, 0, 0))
        display.blit(score_text, (10, 10))

        timer_text = font.render(f'Timer: {timer}', True, (0, 0, 0))
        display.blit(timer_text, (1500, 10))

        # creates the font object for the correct color and renders it
        font = pygame.font.Font(size=100)
        correct_color = font.render(f'{match_object.correct_color}', True, (255, 255, 255))
        # creates a new surface that is black and blit the correct_color onto it
        temp_surface = pygame.Surface(correct_color.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(correct_color, (0, 0))
        # blit the temp_surface onto the main screen
        temp_surface_rect = correct_color.get_rect(center=(1920 / 2, 1080 / 2))
        display.blit(temp_surface, temp_surface_rect)
        pygame.display.update()

# def round sets the boundaries that need to be clicked to get a point
# def randomizer randomly chooses the correct corner/color and also randomly changes what color is in each corner
class Match(Game):
    def __init__(self):
        super(Match, self).__init__()
        # sets the boundaries of each corner for def round
        self.corner_list = [self.topleft, self.topright, self.bottomleft, self.bottomright]
        # empty list to be filled in by def randomizer
        self.correct_corner = []

        self.color_order = [self.white, self.red, self.green, self.blue]
        self.str_color_list = ['white', 'red', 'green', 'blue']
        self.count = 0
        self.start = True

    def __str__(self):
        return str(self.count)

    def correct_choice(self):
        self.count += 1

    def start_button(self):
        if 868 < pygame.mouse.get_pos()[0] < 868 + 184 and \
                506 < pygame.mouse.get_pos()[1] < 506 + 68:
            return True
        else:
            return False

    def round(self):
        if self.correct_corner[0] < pygame.mouse.get_pos()[0] < self.correct_corner[0] + self.correct_corner[2] and \
                self.correct_corner[1] < pygame.mouse.get_pos()[1] < self.correct_corner[1] + self.correct_corner[3]:
            return True
        else:
            return False

    def randomizer(self):
        self.color_order_index = random.sample(range(4), k=4)
        self.str_color_list = [self.str_color_list[i] for i in self.color_order_index]
        self.color_order = [self.color_order[i] for i in self.color_order_index]
        r = random.choice(range(4))
        self.correct_corner = self.corner_list[r]
        self.correct_color = self.str_color_list[r]

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Practice")

pygame.time.set_timer(pygame.USEREVENT, 1000)
counter, text = 30, '30'
# defines the Match() object and performs an initial randomizer
background = Background()
match = Match()
match.randomizer()
# defines the corner borders and the initial colors in each corner
background.start_background(screen)

clock = pygame.time.Clock()
gameloop = True

def match_loop():
    for event in pygame.event.get():
        # Stops the game when the quit button in the corner is pressed
        if event.type == QUIT:
            global gameloop
            gameloop = False
        if event.type == pygame.USEREVENT:
            global counter
            counter -= 1
            global text
            text = str(counter) if counter > 0 else 'boom!'
            background.set_background(screen, match, counter)
            if counter == 0:
                counter = 30
                match.count = 0
                match.start = True
                break
        elif event.type == MOUSEBUTTONDOWN:
            # adds 1 to the scoreboard
            match.correct_choice()
            # changes what the correct corner is and changes the color of each corner
            match.randomizer()
            # changes the color of each corner
            background.set_background(screen, match, counter)
        elif event.type == KEYDOWN:
            if event.key == K_r:
                counter = 30
                match.count = 0
                match.start = True


def start_loop():
    if not match.start_button():
        background.start_background(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            global gameloop
            gameloop = False
        # performs these actions if the mouse button is pressed and the mouse.get_pos is within the values set by match.round()
        elif match.start_button():
            background.start_hover(screen)
            if event.type == MOUSEBUTTONDOWN:
                # changes what the correct corner is and changes the color of each corner
                match.randomizer()
                # changes the color of each corner
                background.set_background(screen, match, counter)
                match.start = False

def main():
    while gameloop:
        clock.tick(100)
        if match.start:
            start_loop()
        else:
            match_loop()

main()
