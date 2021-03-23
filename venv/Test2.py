import os
import pygame
from pygame.sprite import Sprite, Group


class Text(Sprite):
    def __init__(self, text, font, color, position, anchor="topleft"):
        Sprite.__init__(self)
        self._text = text
        self._font = font
        self._color = color
        self._anchor = anchor
        self._position = position
        self.render()

    def render(self):
        self.image = self._font.render(self._text, 1, self._color)
        self.rect = self.image.get_rect(**{self._anchor: self._position})

    def set_text(self, text):
        self._text = text
        self.render()


class Timer:
    def __init__(self, start, interval, callback):
        self.tick = start
        self.interval = interval
        self.callback = callback

    def update(self, ticks):
        while ticks > self.tick:
            self.tick += self.interval
            self.callback(self)


class CountDownTimer:
    def __init__(self, count, callback, interval=1000):
        self.count = count
        self.callback = callback
        self.timer = Timer(pygame.time.get_ticks(), interval, self.countdown)

    def countdown(self, timer):
        self.count -= 1
        self.callback(self)

    def update(self, ticks):
        if self.count >= 0:
            self.timer.update(ticks)


class DisplayCountDown:
    def __init__(self, count, font, color, position, anchor="topleft", interval=1000):
        self.countdown = CountDownTimer(count, self.update_text, interval)
        self.display = "{:02d}"
        self.text = Text(self.display.format(self.countdown.count), font, color, position, anchor)

    def update_text(self, countdown):
        if countdown.count >= 0:
            self.text.set_text(self.display.format(countdown.count))
        else:
            self.text.kill()

    def update(self, ticks):
        self.countdown.update(ticks)


def main():
    pygame.init()
    # center pygame screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # Basic pygame setup
    pygame.display.set_caption("CountDown Timer Example")
    surface = pygame.display.set_mode((450, 600))
    clock = pygame.time.Clock()
    rect = surface.get_rect()
    delta = 0
    fps = 60

    # Setup variables
    timer_font = pygame.font.Font(None, 38)
    position = rect.centerx, 20

    # Game Variables
    timer = DisplayCountDown(11, timer_font, pygame.Color("white"), position, "midtop")
    timer_group = Group(timer.text)

    # Main loop
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        ticks = pygame.time.get_ticks()
        timer.update(ticks)

        # Draw
        surface.fill(pygame.Color("black"))
        timer_group.draw(surface)

        # Render to screen
        pygame.display.flip()

        # Sleep, Idle, and Delta
        delta = clock.tick(fps)


main()