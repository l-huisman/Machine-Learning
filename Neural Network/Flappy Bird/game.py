import pygame
import neat
import time
import os
import random
import pickle

pygame.font.init()

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

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

gen = 0


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
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2

        # Terminal velocity
        if displacement >= 16:
            displacement = 16

        # Move up
        if displacement < 0:
            displacement -= 2

        # Move down
        self.y = self.y + displacement

        # If we are moving up or above the jump height
        if displacement < 0 or self.y < self.height + 50:
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
        # Height, Top, Bottom of the pipe
        self.height = 0
        self.top = 0
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
    def collide(self, bird, win):
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
def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    if gen == 0:
        gen = 1

    # Draw the background
    win.blit(BG_IMG, (0, 0))

    # Draw the pipes
    for pipe in pipes:
        pipe.draw(win)

    # Draw the base
    base.draw(win)

    # Draw the birds
    for bird in birds:
        bird.draw(win)

    # Draw the score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))  # type: ignore
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Update the display
    pygame.display.update()


# Main function
def main(genomes, config):
    # Set the global variables
    global WIN, gen
    win = WIN
    gen += 1

    # Create the networks, genomes, and birds
    nets = []
    ge = []
    birds = []

    # Set all the bird brains
    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(g)

    # Create a base and a list of pipes
    base = Base(730)
    pipes = [Pipe(700)]

    # Score
    score = 0

    # Set the clock
    clock = pygame.time.Clock()

    # Game loop
    run = True
    while run and len(birds) > 0:
        # Set the clock
        clock.tick(30)

        # Check for events
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        # Pipe index
        pipe_ind = 0
        # If there is more than one pipe
        if len(birds) > 0:
            # If the bird passed the first pipe
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                # Set the pipe index to 1
                pipe_ind = 1

        # Loop through the birds
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            # Get the output of the network
            output = nets[birds.index(bird)].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom),
                )
            )

            # If the output is greater than 0.5 then jump
            if output[0] > 0.5:
                bird.jump()

        base.move()

        # Add a new pipe
        add_pipe = False
        # Pipes to remove
        rem = []
        # Loop through the pipes
        for pipe in pipes:
            pipe.move()
            # Loop through the birds
            for bird in birds:
                if pipe.collide(bird, win):
                    # Remove the bird
                    ge[bird.index(bird)].fitness -= 1
                    nets.pop(bird.index(bird))
                    ge.pop(bird.index(bird))
                    birds.pop(bird.index(bird))

            # If the pipe is off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # Add the pipe to the list of pipes to remove
                rem.append(pipe)

            # If the bird passed the pipe
            if not pipe.passed and pipe.x < bird.x:
                # Set the pipe to passed
                pipe.passed = True
                # Set add pipe to true
                add_pipe = True

        # If the bird passed the pipe
        if add_pipe:
            # Increase the score
            score += 1
            # Increase the fitness
            for g in ge:
                g.fitness += 5
            # Add a new pipe
            pipes.append(Pipe(700))

        # Remove the pipes
        for r in rem:
            pipes.remove(r)

        for bird in birds:
            # If the bird hits the ground
            if bird.y + bird.img.get_height() - 10 >= 730 or bird.y < -50:
                # Remove the bird
                nets.pop(bird.index(bird))
                ge.pop(bird.index(bird))
                birds.pop(bird.index(bird))

        # Draw the window
        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)


# Define run
import neat.config


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Create a population
    p = neat.Population(config)

    # Add a stdout reporter
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations
    winner = p.run(main, 50)
    return winner


# Run the run function
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
