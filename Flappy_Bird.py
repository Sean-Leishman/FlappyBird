import pygame,sys,random
WIDTH = 250
HEIGHT = 450 # Play area 500
SCREEN = (WIDTH,HEIGHT)

class Bird():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.yspeed = 0
        self.yacc = 0.4
        self.define_rect()
        self.declare_bird_attributes()

    def define_rect(self):
        self.rect = pygame.Rect(self.x,self.y,10,10)

    def jump(self):
        self.yspeed =-7

    def move(self):
        self.yspeed += self.yacc
        self.rect.y += self.yspeed

    def check_dead(self):
        if self.rect.y >= HEIGHT - 100:
            return True
        return False

    def die(self):
        self.yspeed = 1
        self.rect.y += self.yspeed

    def declare_bird_attributes(self):
        if self.yspeed > 0:
            img = "Flappy_Bird_Images/down_bird.png"
        elif self.yspeed < 0:
            img = "Flappy_Bird_Images/up_bird.png"
        else:
            img = "Flappy_Bird_Images/normal_bird.png"

        self.bird = {"rect":self.rect,
                     "img":pygame.image.load(img),
                    }

    def draw_bird(self,screen):
        screen.blit(self.bird["img"],self.bird["rect"])


class Pipe():
    def __init__(self):
        self.x = WIDTH
        self.height = 0
        self.pipes = [[]]
        self.stop = False

    def move(self):
        for x in range(len(self.pipes)):
            for y in range(len(self.pipes[x])):
                self.pipes[x][y].move_ip(-2,0)

    def stop_pipe(self):
        self.stop = True

    def get_pipe_height(self):
        self.height1 = random.randint(50,250)
        self.height2 = self.height1 + 100

    def spawn_pipes(self):
        self.get_pipe_height()
        rect1 = pygame.Rect(WIDTH,self.height1-286,51,286)
        rect2 = pygame.Rect(WIDTH, self.height2 ,51,286)
        print(self.height1)
        print(self.height2)
        self.pipes.append((rect1,rect2))
        print(self.pipes)
        self.declare_pipe_attributes()

    def declare_pipe_attributes(self):
        self.pipeImg = []
        for x in range(len(self.pipes)):
            for y in range(len(self.pipes[x])):
                if y == 0:
                    img = "Flappy_Bird_Images/down_pipe.png"
                else:
                    img = "Flappy_Bird_Images/up_pipe.png"
                pipe = {
                    "img": pygame.image.load(img),
                    "rect":self.pipes[x][y]
                }
                self.pipeImg.append(pipe)


    def draw_pipe(self,screen):
        for x in range(len(self.pipeImg)):
            screen.blit(self.pipeImg[x]["img"],self.pipeImg[x]["rect"])

    def remove_pipe(self):
        self.pipes.remove(self.pipes[0])
    
class Game():
    def __init__(self):
        pygame.init()
        self.bird = Bird(100,100)
        self.pipe = Pipe()
        self.screen = pygame.display.set_mode(SCREEN)
        self.time = pygame.time.Clock()

    def draw_background(self):
        self.screen.blit(pygame.image.load("Flappy_Bird_Images/background.png"),(0,0,WIDTH,HEIGHT))

    def draw_window(self):
        self.screen.fill((255,255,255))
        self.draw_background()
        self.pipe.draw_pipe(self.screen)
        self.screen.blit(pygame.image.load("Flappy_Bird_Images/bottom.png"), (0, HEIGHT - 95, 300, 100))
        self.bird.draw_bird(self.screen)
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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    self.bird.jump()
            if self.pipe.stop == False:
                self.bird.move()
                self.pipe.move()
                if self.pipe.pipes[0][0].x < 125 and len(self.pipe.pipes) < 2:
                    self.pipe.spawn_pipes()
                if self.pipe.pipes[0][0].x < -50:
                    self.pipe.remove_pipe()
                if self.checkCollision():
                    while self.bird.rect.y < HEIGHT-110:
                        self.bird.die()
                        self.pipe.stop_pipe()
                        self.draw_window()
                if self.bird.check_dead():
                    self.pipe.stop_pipe()
            self.draw_window()
            self.time.tick(60)

if __name__ == "__main__":
    game = Game()
    game.main()