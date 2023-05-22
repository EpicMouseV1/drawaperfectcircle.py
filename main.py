import pygame, math, numpy

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#score_surface = pygame.Surface((300, 100))

BLUE = (0,191,255)
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

FPS = 60

def draw(last_pos, pos, color):
    #pygame.draw.circle(WIN, (255, 255, 255), pos, 5)
    pygame.draw.line(WIN, color, last_pos, pos)
    #print(pos[0]-last_pos[0])
    #pygame.display.update()

def identify_drawing_direction(last_pos, pos, rotation_center):
    theta = ((last_pos[0] - rotation_center[0]) * (pos[1] - rotation_center[1])) - ((last_pos[1] - rotation_center[1]) * (pos[0] - rotation_center[0]))
    if (theta == 0):
        return "undefined"
    if (theta < 0):
        return "counterclockwise"
    return "clockwise"

def display_text(text, x, y):
    text = "Score: " + str(text) + "%"
    text_surface = my_font.render(text, False, (255, 255, 255))
    score_surface = pygame.Surface((300, 100))
    score_surface.fill((0,0,0))
    score_surface.blit(text_surface, (x,y))
    WIN.blit(score_surface, (x, y))

def display_game_status(message):
    text_surface = my_font.render(message, False, (255, 255, 255))
    surface = pygame.Surface((600, 40))
    surface.fill((0,0,0))
    surface.blit(text_surface, (0,0))
    WIN.blit(surface, (300, 0))

def button_restart():
    surface = pygame.Surface((350, 40))
    #surface.fill((255,255,255))
    text_surface = my_font.render("PRESS R TO RESTART", False, (255, 255, 255))
    surface.blit(text_surface, (0,0))
    WIN.blit(surface, (0, 50))
    


count = 0

def main():
    clock = pygame.time.Clock()
    run = True
    circle_params = [0]
    avg_circle_param = 100
    cpy = None
    game_started = True
    game_restarted = False
    while run:
        clock.tick(FPS)
        if (game_restarted):
            game_started =True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0] and game_started:
                if (game_restarted):
                    WIN.fill((0, 0, 0))
                    if "last_pos" in locals():
                        del last_pos
                    if 'initial_mouse_pos' in locals():
                        del initial_mouse_pos
                    game_restarted = False
                
                pos = pygame.mouse.get_pos()

                if 'initial_mouse_pos' not in locals():
                    initial_mouse_pos = pos
                    radius = math.hypot(initial_mouse_pos[0] - 450, initial_mouse_pos[1] - 250)

                current_radius = math.hypot(pos[0]-450, pos[1]-250)

                if current_radius > radius:
                    circle_params.append((radius / current_radius)*100)  
                elif current_radius < radius:
                    circle_params.append((current_radius / radius) *100)
                
                for circle_param in circle_params:
                    avg_circle_param = avg_circle_param + circle_param

                avg_circle_param = avg_circle_param / len(circle_params)                

                if current_radius > radius - 10 and current_radius < radius + 10:
                    color = (0, 255, 0)
                elif current_radius > radius - 25 and current_radius < radius + 25:
                    color = (255, 255, 0)
                else:
                    color = (255, 0, 0)

                
                if cpy:
                    WIN.blit(cpy,(0,0))

                display_text(round(avg_circle_param, 2), 0, 0)

                if math.hypot(pos[0]-450, pos[1]-250) < 100:
                    display_game_status("Distance from the center is too small!")
                    game_started = False
                
                if 'last_pos' not in locals():
                    last_pos = pos

                draw(last_pos, pos, color)

                drawing_center = [450, 250]
                current_drawing_direction = identify_drawing_direction(last_pos, pos, drawing_center)

                if 'prev_drawing_direction' not in locals():
                    prev_drawing_direction = current_drawing_direction

                if ((prev_drawing_direction != current_drawing_direction) and 
                (prev_drawing_direction != "undefined") and
                (current_drawing_direction != "undefined")):
                    display_game_status("WRONG DIRECTION!!!")
                    game_started = False

                if (last_pos[0] < initial_mouse_pos[0] and pos[0] > initial_mouse_pos[0]) and current_drawing_direction == "clockwise":
                    display_game_status("Game over!")
                    game_started = False
                
                if (last_pos[0] > initial_mouse_pos[0] and pos[0] < initial_mouse_pos[0]) and current_drawing_direction == "counterclockwise":
                    display_game_status("Game over!")
                    game_started = False


                if math.hypot(pos[0]-last_pos[0], pos[1]-last_pos[1]) != 0 and math.hypot(pos[0]-last_pos[0], pos[1]-last_pos[1]) < 1.001:
                    print(math.hypot(pos[0]-last_pos[0], pos[1]-last_pos[1]) < 1)
                    display_game_status("Too slow!")
                    game_started = False
                print(math.hypot(pos[0]-last_pos[0], pos[1]-last_pos[1]))
                prev_drawing_direction = current_drawing_direction
                    
                
                last_pos = pos
                cpy = WIN.copy()



            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    #del last_pos
                    game_started = False
                    cpy = None
                    button_restart()
                    
            if game_started == False:
                cpy = None
        
            if pygame.key.get_pressed()[pygame.K_r]:
                game_restarted = True

        pygame.draw.circle(WIN, (255, 255, 255), (450, 250), 5)
        
        pygame.display.update()
        
        

    pygame.quit()

if __name__== "__main__":
    main ()