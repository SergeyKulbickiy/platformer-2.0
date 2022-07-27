import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
tile_size = 50
cols = 20
margin = 100
screen_width = tile_size * cols
screen_height = (tile_size * cols) + margin

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')

# load images
bg_img = pygame.image.load('img/sky.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin))
dirt_img = pygame.image.load('img/dirt.png')
grass_img = pygame.image.load('img/grass.png')
blob_img = pygame.image.load('img/blob.png')
platform_x_img = pygame.image.load('img/platform_x.png')
platform_y_img = pygame.image.load('img/platform_y.png')
lava_img = pygame.image.load('img/lava.png')
coin_img = pygame.image.load('img/coin.png')
exit_img = pygame.image.load('img/exit.png')
save_img = pygame.image.load('img/save_btn.png')
load_img = pygame.image.load('img/load_btn.png')

# load additional images
stone_img = pygame.image.load('img/stone.png')
stone_coal_alt_img = pygame.image.load('img/stone_coal_alt.png')
stone_diamond_alt_img = pygame.image.load('img/stone_diamond_alt.png')
stone_dirt_img = pygame.image.load('img/stone_dirt.png')
stone_gold_alt_img = pygame.image.load('img/stone_gold_alt.png')
stone_grass_img = pygame.image.load('img/stone_grass.png')
dirt_sand_img = pygame.image.load('img/dirt_sand.png')
stone_silver_alt_img = pygame.image.load('img/stone_silver_alt.png')
stone_iron_alt_img = pygame.image.load('img/stone_iron_alt.png')
stone_browniron_alt_img = pygame.image.load('img/stone_browniron_alt.png')
stone_sand_img = pygame.image.load('img/stone_sand.png')
stone_snow_img = pygame.image.load('img/stone_snow.png')
greystone_img = pygame.image.load('img/greystone.png')
greystone_ruby_alt_img = pygame.image.load('img/greystone_ruby_alt.png')
greystone_sand_img = pygame.image.load('img/greystone_sand.png')
dirt_snow_img = pygame.image.load('img/dirt_snow.png')

mushroom_brown_img = pygame.image.load('img/mushroom_brown.png')
mushroom_red_img = pygame.image.load('img/mushroom_red.png')
brick_grey_img = pygame.image.load('img/brick_grey.png')
brick_red_img = pygame.image.load('img/brick_red.png')
fence_stone_img = pygame.image.load('img/fence_stone.png')
fence_wood_img = pygame.image.load('img/fence_wood.png')
grass_brown_img = pygame.image.load('img/grass_brown.png')
grass_tan_img = pygame.image.load('img/grass_tan.png')
grass1_img = pygame.image.load('img/grass1.png')
grass4_img = pygame.image.load('img/grass4.png')
leaves_transparent_img = pygame.image.load('img/leaves_transparent.png')
oven_img = pygame.image.load('img/oven.png')
rock_img = pygame.image.load('img/rock.png')
rock_moss_img = pygame.image.load('img/rock_moss.png')
trunk_bottom_img = pygame.image.load('img/trunk_bottom.png')
trunk_mid_img = pygame.image.load('img/trunk_mid.png')
wheat_stage2_img = pygame.image.load('img/wheat_stage2.png')
wheat_stage3_img = pygame.image.load('img/wheat_stage3.png')

# define game variables
clicked = False
level = 0

# define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

# create empty tile list
world_data = []
for row in range(20):
    r = [0] * 20
    world_data.append(r)

# create boundary
for tile in range(0, 20):
    world_data[19][tile] = 2
    world_data[0][tile] = 1
    world_data[tile][0] = 1
    world_data[tile][19] = 1


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_grid():
    for c in range(21):
        # vertical lines
        pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height - margin))
        # horizontal lines
        pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
    for row in range(20):
        for col in range(20):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # dirt blocks
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 2:
                    # grass blocks
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 3:
                    # enemy blocks
                    img = pygame.transform.scale(blob_img, (tile_size, int(tile_size * 0.75)))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size * 0.25)))
                if world_data[row][col] == 4:
                    # horizontally moving platform
                    img = pygame.transform.scale(platform_x_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 5:
                    # vertically moving platform
                    img = pygame.transform.scale(platform_y_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 6:
                    # lava
                    img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
                    screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
                if world_data[row][col] == 7:
                    # coin
                    img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
                    screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
                if world_data[row][col] == 8:
                    # exit
                    img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
                    screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))

                # load additional blocks
                if world_data[row][col] == 9:
                    # stone blocks
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 10:
                    # stone_coal_alt blocks
                    img = pygame.transform.scale(stone_coal_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 11:
                    # stone_diamond_alt blocks
                    img = pygame.transform.scale(stone_diamond_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 12:
                    # stone_dirt blocks
                    img = pygame.transform.scale(stone_dirt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 13:
                    # stone_gold_alt blocks
                    img = pygame.transform.scale(stone_gold_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 14:
                    # stone_grass blocks
                    img = pygame.transform.scale(stone_grass_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 15:
                    # dirt_sand blocks
                    img = pygame.transform.scale(dirt_sand_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 16:
                    # stone_silver_alt blocks
                    img = pygame.transform.scale(stone_silver_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 17:
                    # stone_iron_alt blocks
                    img = pygame.transform.scale(stone_iron_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 18:
                    # stone_browniron_alt blocks
                    img = pygame.transform.scale(stone_browniron_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 19:
                    # stone_sand blocks
                    img = pygame.transform.scale(stone_sand_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 20:
                    # stone_snow blocks
                    img = pygame.transform.scale(stone_snow_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 21:
                    # greystone blocks
                    img = pygame.transform.scale(greystone_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 22:
                    # greystone_ruby_alt blocks
                    img = pygame.transform.scale(greystone_ruby_alt_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 23:
                    # greystone_sand blocks
                    img = pygame.transform.scale(greystone_sand_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 24:
                    # dirt_snow blocks
                    img = pygame.transform.scale(dirt_snow_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))

                # add decoration

                if world_data[row][col] == 25:
                    # mushroom_brown blocks
                    img = pygame.transform.scale(mushroom_brown_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 26:
                    # mushroom_red blocks
                    img = pygame.transform.scale(mushroom_red_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 27:
                    # brick_grey blocks
                    img = pygame.transform.scale(brick_grey_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 28:
                    # brick_red blocks
                    img = pygame.transform.scale(brick_red_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 29:
                    # fence_stone blocks
                    img = pygame.transform.scale(fence_stone_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 30:
                    # fence_wood blocks
                    img = pygame.transform.scale(fence_wood_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 31:
                    # grass_brown blocks
                    img = pygame.transform.scale(grass_brown_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 32:
                    # grass_tan blocks
                    img = pygame.transform.scale(grass_tan_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 33:
                    # grass1 blocks
                    img = pygame.transform.scale(grass1_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 34:
                    # grass4 blocks
                    img = pygame.transform.scale(grass4_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 35:
                    # leaves_transparent blocks
                    img = pygame.transform.scale(leaves_transparent_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 36:
                    # oven blocks
                    img = pygame.transform.scale(oven_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 37:
                    # rock blocks
                    img = pygame.transform.scale(rock_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 38:
                    # rock_moss blocks
                    img = pygame.transform.scale(rock_moss_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 39:
                    # trunk_bottom blocks
                    img = pygame.transform.scale(trunk_bottom_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 40:
                    # trunk_mid blocks
                    img = pygame.transform.scale(trunk_mid_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 41:
                    # wheat_stage2 blocks
                    img = pygame.transform.scale(wheat_stage2_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))
                if world_data[row][col] == 42:
                    # wheat_stage3 blocks
                    img = pygame.transform.scale(wheat_stage3_img, (tile_size, tile_size))
                    screen.blit(img, (col * tile_size, row * tile_size))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# create load and save buttons
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

# main game loop
run = True
while run:

    clock.tick(fps)

    # draw background
    screen.fill(green)
    screen.blit(bg_img, (0, 0))

    # load and save level
    if save_button.draw():
        # save level data
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
    if load_button.draw():
        # load in level data
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)

    # show the grid and draw the level tiles
    draw_grid()
    draw_world()

    # text showing current level
    draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
    draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 40)

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # mouseclicks to change tiles
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
            pos = pygame.mouse.get_pos()
            x = pos[0] // tile_size
            y = pos[1] // tile_size
            # check that the coordinates are within the tile area
            if x < 20 and y < 20:
                # update tile value
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[y][x] += 1
                    if world_data[y][x] > 42:
                        world_data[y][x] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[y][x] -= 1
                    if world_data[y][x] < 0:
                        world_data[y][x] = 42
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        # up and down key presses to change level number
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1

    # update game display window
    pygame.display.update()

pygame.quit()
