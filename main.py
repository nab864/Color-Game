import pygame
from pygame.locals import *
import random


class Background:
    def __init__(self):
        pass
    def start_background(self, display):
        topleft = (0, 0, 960, 540)
        topright = (960, 0, 960, 540)
        bottomleft = (0, 540, 960, 540)
        bottomright = (960, 540, 960, 540)
        pygame.draw.rect(display, [250, 250, 250], topleft)
        pygame.draw.rect(display, [250, 0, 0], topright)
        pygame.draw.rect(display, [0, 250, 0], bottomleft)
        pygame.draw.rect(display, [0, 0, 250], bottomright)

        # creates the font object for the score and renders it
        font = pygame.font.Font(size=100)
        correct_color = font.render('Start', True, (255, 255, 255))
        # creates a new surface that is black and blit the correct_color onto it
        temp_surface = pygame.Surface(correct_color.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(correct_color, (0, 0))
        # blit the temp_surface onto the main screen
        temp_surface_rect = correct_color.get_rect(center=(1920 / 2, 1080 / 2))
        display.blit(temp_surface, temp_surface_rect)

        pygame.display.update()


    def set_background(self, display, match_object):
        # Sets the colors in each corner
        topleft = (0, 0, 960, 540)
        topright = (960, 0, 960, 540)
        bottomleft = (0, 540, 960, 540)
        bottomright = (960, 540, 960, 540)
        pygame.draw.rect(display, match_object.color_order[0], topleft)
        pygame.draw.rect(display, match_object.color_order[1], topright)
        pygame.draw.rect(display, match_object.color_order[2], bottomleft)
        pygame.draw.rect(display, match_object.color_order[3], bottomright)

        # creates the font object for the score and renders it
        font = pygame.font.Font(size=100)
        score_text = font.render(f'Score: {match_object}', True, (0, 0, 0))
        display.blit(score_text, (10, 10))

        # creates the font object for the correct color and renders it
        font2 = pygame.font.Font(size=100)
        correct_color = font2.render(f'{match_object.correct_color}', True, (255, 255, 255))
        # creates a new surface that is black and blit the correct_color onto it
        temp_surface = pygame.Surface(correct_color.get_size())
        temp_surface.fill((0, 0, 0))
        temp_surface.blit(correct_color, (0, 0))
        # blit the temp_surface onto the main screen
        temp_surface_rect = correct_color.get_rect(center=(1920 / 2, 1080 / 2))
        print(temp_surface_rect)
        display.blit(temp_surface, temp_surface_rect)
        pygame.display.update()

# def round sets the boundaries that need to be clicked to get a point
# def randomizer randomly chooses the correct corner/color and also randomly changes what color is in each corner
class Match:
    def __init__(self):
        # sets the boundaries of each corner for def round
        topleft = [0, 0, 960, 540]
        topright = [960, 0, 960, 540]
        bottomleft = [0, 540, 960, 540]
        bottomright = [960, 540, 960, 540]
        self.corner_list = [topleft, topright, bottomleft, bottomright]
        #empty list to be filled in by def randomizer
        self.correct_corner = []
        # Give the rgb value associated with each color
        white = [250, 250, 250]
        red = [250, 0, 0]
        green = [0, 250, 0]
        blue = [0, 0, 250]
        self.color_order = [white, red, green, blue]
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

def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Practice")
    # defines the Match() object and performs an initial randomizer
    background = Background()
    match = Match()
    match.randomizer()
    # defines the corner borders and the initial colors in each corner
    background.start_background(screen)

    clock = pygame.time.Clock()
    gameloop = True
    while gameloop:
        clock.tick(60)
        for event in pygame.event.get():
            # Stops the game when the quit button in the corner is pressed
            if event.type == QUIT:
                gameloop = False
            # performs these actions if the mouse button is pressed and the mouse.get_pos is within the values set by match.round()
            elif event.type == MOUSEBUTTONDOWN:
                if match.round() and not match.start:
                    # adds 1 to the scoreboard
                    match.correct_choice()
                    # changes what the correct corner is and changes the color of each corner
                    match.randomizer()
                    # changes the color of each corner
                    background.set_background(screen, match)
                elif match.start_button():
                    # changes what the correct corner is and changes the color of each corner
                    match.randomizer()
                    match.start = False
                    # changes the color of each corner
                    background.set_background(screen, match)
main()
