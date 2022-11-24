import pygame, sys, time, random, os
pygame.init()

speed = 5

soundtrack = pygame.mixer.music.load('BoxCat Games - Passing Time.mp3')
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound('smw_kick.wav')
game_over_sound = pygame.mixer.Sound('smw_ludwig_morton_roy_beat.wav')

FONT = pygame.font.SysFont('Arial', 20)

#windows sizes 

frame_size_x = 1000
frame_size_y = 600

check_errors = pygame.init()

if(check_errors[1] > 0):
    print("Error " + check_errors[1])
else:
    print("Game Sucessfully initialized")

# initialize game window

pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

#colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fps_controller = pygame.time.Clock()
# one snake square size
square_size = 40

def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1,(frame_size_x // square_size)) * square_size,
                 random.randrange(1,(frame_size_y // square_size)) * square_size]
    food_spawn = True
    score = 0
    
init_vars()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)




#game loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if( event.key == pygame.K_UP or event.key == ord("w")
                 and direction != "DOWN" ):
                direction = "UP"
            elif ( event.key == pygame.K_DOWN or event.key == ord("s")
                 and direction != "UP" ):
                direction = "DOWN"
            elif ( event.key == pygame.K_LEFT or event.key == ord("a")
                 and direction != "RIGHT" ):
                direction = "LEFT"
            elif ( event.key == pygame.K_RIGHT or event.key == ord("d")
                 and direction != "LEFT" ):
                direction = "RIGHT"
        

    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size

    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y -  square_size:
        head_pos[1] = 0
    
    # eating apple
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
        eat_sound.play()
    else:
        snake_body.pop()
    
    # velocity changes according to the score

    if(score == 5):
        speed = 7
    elif(score == 8):
        speed = 8
    elif(score == 14):
        speed = 9
    elif(score == 18):
        speed = 12
    elif(score == 25):
        speed = 15
    elif(score == 40):
        speed == 20
    elif(score == 55):
        speed == 25

    # spawn food
    if not food_spawn:
        food_pos = [random.randrange(1,(frame_size_x // square_size)) * square_size,
         random.randrange(1,(frame_size_y // square_size)) * square_size]
        food_spawn = True

    # GFX
    #game_window.fill(black)
    BG = pygame.image.load(os.path.join('GrassField.png')).convert()
    game_window.blit(BG, (0,0))

    APPLE = pygame.image.load(os.path.join('apple.jpg')).convert()
    game_window.blit(APPLE, (food_pos[0], food_pos[1]))
    pygame.display.flip()
    #pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0],
    #                 food_pos[1], square_size, square_size))


    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0] + 2, pos[1] + 2,
            square_size -2, square_size -2))

    

# game over conditions
    def game_over():
        #Text to render
        game_over_text = FONT.render(f"GAME OVER!", True, (255,255,255))
        score_text = FONT.render(f"Pontuação máxima: {score}", True, (255, 255, 255))
        game_window.blit(game_over_text, (frame_size_x/2, frame_size_y/2))
        game_window.blit(score_text, (frame_size_x/2, frame_size_y/2 + 60))

        game_over_sound.play()

        pygame.display.update()
        time.sleep(8)

        init_vars()
    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            game_over()
            
        
            

    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(speed)