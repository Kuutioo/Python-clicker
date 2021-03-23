import pygame
pygame.init()

screen = pygame.display.set_mode((450, 600))

timer_font = pygame.font.Font(None, 38)
timer_sec = 60
timer_text = timer_font.render("01:00", True, (255, 255, 255))
current_timer_text = None

# USEREVENTS are just integers
# you can only have like 31 of them or something arbitrarily low
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1000)    # sets timer with USEREVENT and delay in milliseconds

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == timer:    # checks for timer event
            if timer_sec > 0:
                timer_sec -= 1
                timer_text = timer_font.render("00:%02d" % timer_sec, True, (255, 255, 255))
            else:
                pygame.time.set_timer(timer, 0)    # turns off timer event

# add another "if timer_sec > 0" here if you want the timer to disappear after reaching 0
    screen.blit(timer_text, (300, 20))
    pygame.display.update()