import pygame
pygame.font.init()
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

# Load images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Bird class
class Bird:
    IMGS = BIRD_IMGS
    # How much the bird tilts
    MAX_ROTATION = 25
    # How much the bird moves up and down on each frame
    ROT_VEL = 20
    # How long to show each bird animation
    ANIMATION_TIME = 5

    # Constructor
    def __init__(self, x, y):
        # Initial position of the bird
        self.x = x
        self.y = y
        # Tilt of the bird
        self.tilt = 0
        # Tick count
        self.tick_count = 0
        # Velocity
        self.vel = 0
        # Height of the bird
        self.height = self.y
        # Image count
        self.img_count = 0
        # Which image to show
        self.img = self.IMGS[0]

    # Jump
    def jump(self):
        # Set velocity to jump velocity
        self.vel = -10.5
        # Keep track of when we last jumped
        self.tick_count = 0
        # Keep track of where the bird jumped from
        self.height = self.y

    # Move
    def move(self):
        # Keep track of how many times we moved since last jump
        self.tick_count += 1
        # Displacement
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # Terminal velocity
        if d >= 16:
            d = 16

        # Move up
        if d < 0:
            d -= 2

        # Move down
        self.y = self.y + d

        # If we are moving up or above the jump height
        if d < 0 or self.y < self.height + 50:
            # Tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # Otherwise, tilt down
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    # Draw
    def draw(self, win):
        # Which image to show
        self.img_count += 1

        # Show the first image for 5 frames, then the second for 5 frames, etc.
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If the bird is falling, don't flap
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate the image around the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # Get the rectangle of the image
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        # Draw the rotated image
        win.blit(rotated_image, new_rect.topleft)

    # Get mask
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
# Pipe class
class Pipe:
    GAP = 200
    VEL = 5

    # Constructor
    def __init__(self, x):
        # Initial position of the pipe
        self.x = x
        # Height of the pipe
        self.height = 0
        # Where the top of the pipe is
        self.top = 0
        # Where the bottom of the pipe is
        self.bottom = 0
        # Top pipe image
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        # Bottom pipe image
        self.PIPE_BOTTOM = PIPE_IMG
        # If the bird passed the pipe
        self.passed = False
        # Set the height of the pipe
        self.set_height()

    # Set height
    def set_height(self):
        # Set the height of the pipe
        self.height = random.randrange(50, 450)
        # Set the top and bottom of the pipe
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    # Move
    def move(self):
        # Move the pipe
        self.x -= self.VEL

    # Draw
    def draw(self, win):
        # Draw the top pipe
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # Draw the bottom pipe
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # Collision
    def collide(self, bird):
        # Get the mask of the bird
        bird_mask = bird.get_mask()
        # Get the mask of the top pipe
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        # Get the mask of the bottom pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # Offset
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # Point of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        # If there is a collision
        if t_point or b_point:
            return True
        return False
    
# Base class
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    # Constructor
    def __init__(self, y):
        # Initial position of the base
        self.y = y
        # Initial position of the first base
        self.x1 = 0
        # Initial position of the second base
        self.x2 = self.WIDTH

    # Move
    def move(self):
        # Move the base
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # If the first base is off the screen
        if self.x1 + self.WIDTH < 0:
            # Move the first base to the right of the second base
            self.x1 = self.x2 + self.WIDTH
        # If the second base is off the screen
        if self.x2 + self.WIDTH < 0:
            # Move the second base to the right of the first base
            self.x2 = self.x1 + self.WIDTH

    # Draw
    def draw(self, win):
        # Draw the first base
        win.blit(self.IMG, (self.x1, self.y))
        # Draw the second base
        win.blit(self.IMG, (self.x2, self.y))

# Draw the window
def draw_window(win, bird, pipes, base, score):
    # Draw the background
    win.blit(BG_IMG, (0, 0))
    # Draw the pipes
    for pipe in pipes:
        pipe.draw(win)
    # Draw the base
    base.draw(win)
    # Draw the bird
    bird.draw(win)
    # Draw the score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    # Update the display
    pygame.display.update()

# Main function
def main():
    # Create a window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # Create a clock
    clock = pygame.time.Clock()
    # Create a bird
    bird = Bird(230, 350)
    # Create a base
    base = Base(730)
    # Create a list of pipes
    pipes = [Pipe(700)]
    # Score
    score = 0

    # Game loop
    run = True
    while run:
        # Set the clock
        clock.tick(30)
        # Check for events
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                run = False
        # Move the bird
        bird.move()
        # Move the base
        base.move()
        # Add a new pipe
        add_pipe = False
        # Pipes to remove
        rem = []
        # Loop through the pipes
        for pipe in pipes:
            # If the bird collided with the pipe
            if pipe.collide(bird):
                # Quit the game
                run = False
            # If the pipe is off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # Add the pipe to the list of pipes to remove
                rem.append(pipe)
            # If the bird passed the pipe
            if not pipe.passed and pipe.x < bird.x:
                # Set the pipe to passed
                pipe.passed = True
                # Add a new pipe
                add_pipe = True
            # Move the pipe
            pipe.move()
        # If the bird passed the pipe
        if add_pipe:
            # Increase the score
            score += 1
            # Add a new pipe
            pipes.append(Pipe(700))
        # Remove the pipes
        for r in rem:
            pipes.remove(r)
        # If the bird hit the ground
        if bird.y + bird.img.get_height() >= 730:
            # Quit the game
            run = False
        # Draw the window
        draw_window(win, bird, pipes, base, score)
    
    # Quit the game
    pygame.quit()
    # Print the score
    print("Score: " + str(score))

# Run the main function
main()
