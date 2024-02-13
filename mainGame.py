import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1300, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Shape Survival")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40

PLAYER_HEIGHT = 40

PLAYER_VEL = 5
STAR_WIDTH = 15
STAR_HEIGHT = 15
STAR_VEL = 6

FONT = pygame.font.SysFont("arial", 36)

def draw(player, elapsed_time, stars):
	WIN.blit(BG, (0, 0))

	time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
	WIN.blit(time_text, (15,15))

	pygame.draw.rect(WIN, "yellow", player)

	for star in stars:
		pygame.draw.rect(WIN, "red", star)

	pygame.display.update()

def draw_pause():
	pygame.draw.rect(surface, (128, 128, 128, 50), [0, 0, WIDTH, HEIGHT])
	WIN.blit(surface, (0, 0))

def main():
	run = True
	pause = False
	last_escape_time = 0

	player = pygame.Rect(600, 450, PLAYER_WIDTH, PLAYER_HEIGHT)

	clock = pygame.time.Clock()

	start_time = time.time()
	elapsed_time = 0

	star_add_increment = 2000
	star_count = 0

	stars = []
	hit = False

	while run:
		star_count += clock.tick(60)
		elapsed_time = time.time() - start_time

		if not pause:
			if star_count > star_add_increment:
				for _ in range(5):
					star_x = random.randint(0, WIDTH - STAR_WIDTH)
					star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
					stars.append(star)

				star_add_increment = max(200, star_add_increment - 50)
				star_count = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

		keys = pygame.key.get_pressed()

		if not pause:
			if keys[pygame.K_a] and player.x - PLAYER_VEL >= 0:
				player.x -= PLAYER_VEL
			if keys[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
				player.x += PLAYER_VEL
			if keys[pygame.K_w] and player.y - PLAYER_VEL >= 0:
				player.y -= PLAYER_VEL
			if keys[pygame.K_s] and player.y + PLAYER_VEL + player.width <= HEIGHT:
				player.y += PLAYER_VEL

		if keys[pygame.K_ESCAPE]:
			current_time = pygame.time.get_ticks()
			time_passed = current_time - last_escape_time

			if time_passed >= 200:
				pause = not pause
				last_escape_time = current_time

		if not pause:
			for star in stars[:]:
				star.y += STAR_VEL
				if star.y > HEIGHT:
					stars.remove(star)
				elif star.colliderect(player):
					stars.remove(star)
					hit = True
					break

		if hit:
			lost_text = FONT.render("You lose!", 1, "white")
			WIN.blit(lost_text, (WIDTH/2- lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))		
			pygame.display.update()
			pygame.time.delay(3400)
			main()

		draw(player, elapsed_time, stars)
		if pause:
			draw_pause()

	pygame.quit()

if __name__ == "__main__":
	main()