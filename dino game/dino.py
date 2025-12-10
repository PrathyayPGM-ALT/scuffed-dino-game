import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1200, 700
GROUND_Y = 550
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino - Scuffed Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 32)

# cheap highscore - 99% discount lol 
def load_highscore(): 
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0   # if file missing or corrupted

def save_highscore(new_score):
    with open("highscore.txt", "w") as f:
        f.write(str(int(new_score)))


highscore = load_highscore()


# Dinosaur - raaaauwr
class Dino:
    def __init__(self):
        self.w = 50
        self.h = 50
        self.x = 100
        self.y = GROUND_Y - self.h
        self.gravity = 0
        self.on_ground = True

        # cheap “animation”
        self.leg = 0
        self.time = 0

    def draw(self):
        pygame.draw.rect(screen, "red", (self.x, self.y + self.leg, self.w, self.h - self.leg))

    def update(self, dt):
        self.gravity += 0.9
        self.y += self.gravity

        # hit the floor
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.gravity = 0
            self.on_ground = True

        # tiny run animation
        if self.on_ground:
            self.time += dt
            if self.time >= 120:
                self.time = 0
                self.leg = 0 if self.leg == 5 else 5

    def jump(self):
        if self.on_ground:
            self.gravity = -20
            self.on_ground = False


# cactisuses
class Cactus:
    def __init__(self, speed):
        self.w = 30
        self.h = random.randint(60, 120)
        self.x = WIDTH + random.randint(0, 200)
        self.y = GROUND_Y - self.h
        self.speed = speed

    def update(self, dt, speed):
        self.speed = speed
        self.x -= self.speed * (dt / 16)

    def draw(self):
        pygame.draw.rect(screen, "green", (self.x, self.y, self.w, self.h))

    def offscreen(self):
        return self.x + self.w < 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


# loading random aahh stuff
dino = Dino()
cacti = []

score = 0
speed = 10
spawn_timer = 0
spawn_delay = 1200
dead = False


def draw_ground():
    pygame.draw.line(screen, "white", (0, GROUND_Y), (WIDTH, GROUND_Y), 3)


def draw_score():
    s = font.render(f"Score: {int(score)}", True, "white")
    hs = font.render(f"High Score: {int(highscore)}", True, "white")
    screen.blit(s, (20, 20))
    screen.blit(hs, (20, 60))


def draw_game_over():
    t1 = font.render("SKILL ISSUE GET BETTER", True, "white")
    t2 = font.render("Press R to restart", True, "white")
    t3 = font.render("Press ESC to quit - quitter noob", True, "white")

    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 - 10))
    screen.blit(t3, (WIDTH//2 - t3.get_width()//2, HEIGHT//2 + 40))


def reset():
    global dino, cacti, score, speed, spawn_timer, dead
    dino = Dino()
    cacti = []
    score = 0
    speed = 10
    spawn_timer = 0
    dead = False


# HAHA GAME LOOP GO BRRR
running = True
while running:
    dt = clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not dead:

        # JUMP
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            dino.jump()

        dino.update(dt)

        # score increments
        score += 0.1

        # speed ramps up
        speed = 10 + (score // 50)

        # spawn cactus
        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            cacti.append(Cactus(speed))

        # update cactus list
        for c in cacti[:]:
            c.update(dt, speed)
            if c.offscreen():
                cacti.remove(c)

        # collision detection
        dino_rect = pygame.Rect(dino.x, dino.y, dino.w, dino.h)
        for c in cacti:
            if dino_rect.colliderect(c.rect()):
                dead = True

                # update highscore
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)

                break

    else:
        # Game Over controls
        if keys[pygame.K_r]:
            reset()
        if keys[pygame.K_ESCAPE]:
            running = False

    # DRAW EVERYTHING
    screen.fill("black")
    draw_ground()
    dino.draw()

    for c in cacti:
        c.draw()

    draw_score()

    if dead:
        draw_game_over()

    pygame.display.flip()

pygame.quit()
