#Create your own shooter

from random import randint

from pygame import *
winwidth = 700
winheight = 500
window = display.set_mode((winwidth, winheight))  
display.set_caption("Space shooter Game")
background = transform.scale(
  image.load("galaxy.jpg"), (winwidth, winheight)
)
mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()
firesound = mixer.Sound("fire.ogg")
clock = time.Clock()

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)

lost = 0
maxlost = 10
score = 0
class GameSprite(sprite.Sprite):
  def __init__(self, image, x, y, width, height, speed):
    super().__init__()
    self.image = transform.scale(image, (width, height))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y 
    self.speed = speed
  def reset(self):
    window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
  def update(self):
    keys = key.get_pressed()
    if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 0:
      self.rect.x -= self.speed
    if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < 650:
      self.rect.x += self.speed
    if (keys[K_w] or keys[K_UP]) and self.rect.y > 0:
      self.rect.y -= self.speed
    if (keys[K_s] or keys[K_DOWN]) and self.rect.y < 450:
      self.rect.y += self.speed
  def fire(self):
    bullet = Bullet(image.load("bullet.png"), self.rect.centerx, self.rect.top, 15, 20, 10)
    bullets.add(bullet)

class Enemy(GameSprite):
  def update(self):
    self.rect.y += self.speed
    global lost
    if self.rect.y > winheight:
      self.rect.x = randint(0, winwidth - 80)
      self.rect.y = 0
      lost += 1

class Bullet(GameSprite):
  def update(self):
    self.rect.y -= self.speed
    if self.rect.y < 0:
      self.kill()


ship = Player(image.load("rocket.png"), 300, 400, 50, 80, 5)

ufo = Enemy(image.load("ufo.png"), randint(0, winwidth - 80), 0, 80, 50, randint(1, 5))
jml_enemies = 6

monsters = sprite.Group()
bullets = sprite.Group()

for i in range(jml_enemies):

  ufo = Enemy(image.load("ufo.png"), randint(0, winwidth - 80), 0, 80, 50, randint(1, 2))       
  monsters.add(ufo)
game = True
game_over = False

win_text = font2.render("You win!", True, (0, 255, 0))
lose_text = font2.render("You lose!", True, (255, 0, 0))

setting_max_lost = 15
setting_goal = 20

while game:
  for e in event.get():
    if e.type == QUIT:
      game = False
    if e.type == KEYDOWN:
      if e.key == K_SPACE:
        firesound.play()
        ship.fire()
  if not game_over:
    window.blit(background, (0, 0))
    lost_text = font1.render("Missed: " + str(lost), True, (255, 255, 255))
    score_text = font1.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(lost_text, (10, 10))
    window.blit(score_text, (10, 50))
    if lost >= setting_max_lost:
      game_over = True
    if lost >= setting_max_lost:
          game_over = True
    colisions = sprite.groupcollide(monsters, bullets, True, True)
    for c in colisions:
          score += 1
          ufo = Enemy(image.load("ufo.png"), randint(0, winwidth - 80), 0, 80, 50, randint(1, 2))       
          monsters.add(ufo)
    if sprite.spritecollide(ship, monsters, False):
          game_over = True
          
    if score >= setting_goal:
          game_over = True
    ship.update()
    ship.reset()
    monsters.update()
    monsters.draw(window)
    bullets.update()
    bullets.draw(window)
    display.update()
  else:
    window.blit(background, (0, 0))
    lost_text = font1.render("You lost!", True, (255, 255, 255))
    score_text = font1.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(lost_text, (300, 200))
    window.blit(score_text, (300, 250))
    display.update()
  clock.tick(60)

