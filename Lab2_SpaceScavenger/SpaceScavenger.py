import pygame
import random
import os

# Иницијализација на PyGame и прозорецот на играта
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Scavenger")

# Боја и фонт за текстови
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Вчитување ресурси
spaceship_img = pygame.image.load("spaceship.png")
asteroid_img = pygame.image.load("asteroid.png")
crystal_img = pygame.image.load("energy_crystal.png")
background_music = "background_music.wav"
clash_sound = pygame.mixer.Sound("clash_sound.wav")

# Подесување позадинска музика
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

# Класа за вселенски брод
class Spaceship:
    def __init__(self):
        self.image = pygame.transform.scale(spaceship_img, (60, 60))
        self.x = screen_width // 2
        self.y = screen_height - 100
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - 60:
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Класа за астероиди
class Asteroid:
    def __init__(self):
        self.image = pygame.transform.scale(asteroid_img, (50, 50))
        self.x = random.randint(0, screen_width - 50)
        self.y = -50
        self.speed = random.randint(3, 6)

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Класа за енергетски кристали
class Crystal:
    def __init__(self):
        self.image = pygame.transform.scale(crystal_img, (40, 40))
        self.x = random.randint(0, screen_width - 40)
        self.y = -40
        self.speed = random.randint(2, 4)

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Главна функција на играта
def game_loop():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]
    crystals = [Crystal() for _ in range(3)]
    score = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        spaceship.move(keys)

        for asteroid in asteroids:
            asteroid.move()
            if asteroid.y > screen_height:
                asteroids.remove(asteroid)
                asteroids.append(Asteroid())
            if spaceship.x < asteroid.x + 50 and spaceship.x + 60 > asteroid.x and spaceship.y < asteroid.y + 50 and spaceship.y + 60 > asteroid.y:
                pygame.mixer.Sound.play(clash_sound)
                running = False

        for crystal in crystals:
            crystal.move()
            if crystal.y > screen_height:
                crystals.remove(crystal)
                crystals.append(Crystal())
            if spaceship.x < crystal.x + 40 and spaceship.x + 60 > crystal.x and spaceship.y < crystal.y + 40 and spaceship.y + 60 > crystal.y:
                score += 1
                crystals.remove(crystal)
                crystals.append(Crystal())

        spaceship.draw()
        for asteroid in asteroids:
            asteroid.draw()
        for crystal in crystals:
            crystal.draw()

        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Стартување на играта
if __name__ == "__main__":
    game_loop()
