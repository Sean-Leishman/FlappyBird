import pygame,sys,random
#import neat
from time import sleep

WIDTH = 500
HEIGHT = 900 # Play area 500
SCREEN = (WIDTH,HEIGHT)

class Pipe():
    def __init__(self):
        self.x = WIDTH
        self.height = 0
        self.pipes = [[]]
        self.stop = False

    def move(self):
        for x in range(len(self.pipes)):
            for y in range(len(self.pipes[x])):
                self.pipes[x][y].move_ip(-5,0)

    def stop_pipe(self):
        self.stop = True

    def get_pipe_height(self):
        self.height1 = random.randint(50,250)
        self.height2 = self.height1 + 200

    def spawn_pipes(self):
        self.get_pipe_height()
        rect1 = pygame.Rect(WIDTH,self.height1-640,104,620)
        rect2 = pygame.Rect(WIDTH, self.height2 ,104,620)
        self.pipes.append((rect1,rect2))
        self.declare_pipe_attributes()

    def declare_pipe_attributes(self):
        self.pipeImg = []
        for x in range(len(self.pipes)):
            for y in range(len(self.pipes[x])):
                if y == 0:
                    img = "Flappy_Bird_Images/dpipe.png"
                else:
                    img = "Flappy_Bird_Images/pipe.png"
                pipe = {
                    "img": pygame.transform.scale2x(pygame.image.load(img)),
                    "rect":self.pipes[x][y]
                }
                self.pipeImg.append(pipe)


    def draw_pipe(self,screen):
        for x in range(len(self.pipeImg)):
            screen.blit(self.pipeImg[x]["img"],self.pipeImg[x]["rect"])

    def remove_pipe(self):
        self.pipes.remove(self.pipes[0])

class Bird():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.yspeed = 0
        self.yacc = 1
        self.define_rect()
        self.declare_bird_attributes()

    def define_rect(self):
        self.rect = pygame.Rect(self.x,self.y,20,20)

    def jump(self):
        self.yspeed =-14

    def move(self):
        self.yspeed += self.yacc
        self.rect.y += self.yspeed

    def check_dead(self):
        if self.rect.y >= HEIGHT - 200:
            return True
        return False

    def die(self):
        self.yspeed = 2
        self.rect.y += self.yspeed

    def declare_bird_attributes(self):
        if self.yspeed > 0:
            img = "Flappy_Bird_Images/bird1.png"
        elif self.yspeed < 0:
            img = "Flappy_Bird_Images/bird2.png"
        else:
            img = "Flappy_Bird_Images/bird3.png"

        self.bird = {"rect":self.rect,
                     "img":pygame.transform.scale2x(pygame.image.load(img)),
                    }

    def draw_bird(self,screen):
        screen.blit(self.bird["img"],self.bird["rect"])

gen = 0

class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.bird = Bird(100,100)
        self.pipe = Pipe()
        self.screen = pygame.display.set_mode(SCREEN)
        self.time = pygame.time.Clock()
        self.count = 0

    def draw_background(self):
        self.screen.blit(pygame.transform.scale2x(pygame.image.load("Flappy_Bird_Images/bg.png")),(0,0,WIDTH,HEIGHT))

    def draw_window(self):
        self.screen.fill((255,255,255))
        self.draw_background()
        self.pipe.draw_pipe(self.screen)
        self.screen.blit(pygame.transform.scale2x(pygame.image.load("Flappy_Bird_Images/base.png")), (0, HEIGHT - 190, 600, 200))
        self.bird.draw_bird(self.screen)
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = font.render(str(self.count), False, (0, 0, 0))
        self.screen.blit(text_surface, (400, 0))
        pygame.display.update()

    def checkCollision(self):
        for x in range(len(self.pipe.pipes)):
            for y in range(len(self.pipe.pipes[x])):
                if self.bird.rect.colliderect(self.pipe.pipes[x][y]):
                    return True
        return False

    def main(self):
        pressed_down = False
        self.pipe.spawn_pipes()
        self.pipe.remove_pipe()
        count = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.bird.jump()
            if self.pipe.stop == False:
                self.bird.move()
                self.pipe.move()
                if self.pipe.pipes[0][0].x < 150 and len(self.pipe.pipes) < 2:
                    self.pipe.spawn_pipes()
                    self.count += 1
                if self.pipe.pipes[0][0].x < -100:
                    self.pipe.remove_pipe()
                if self.checkCollision():
                    while self.bird.rect.y < HEIGHT-220:
                        self.bird.die()
                        self.pipe.stop_pipe()
                        self.draw_window()
                if self.bird.check_dead():
                    self.pipe.stop_pipe()
            self.draw_window()
            self.time.tick(30)

    def eval_genomes(self, genomes, config):
        global gen
        gen += 1

        nets = []
        birds = []
        ge = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            birds.append(Bird())
            ge.append(genome)

        pipes = [Pipe()]
        score = 0

        while len(birds)>0 and True:
            self.time.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[
                0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1

        for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        rem = []
        add_pipe = False

        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if self.checkCollision():
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))



if __name__ == "__main__":
    game = Game()
    game.main()