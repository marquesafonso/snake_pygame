import pygame, random
import numpy as np

class Snake_Game():

    def __init__(self,player="HUMAN"):
        
        # Initialize pygame
        pygame.init()
        
        # Set display window
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 600, 600
        
        self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("~~~Snake~~~")

        # Set FPS and clock
        self.FPS = 15
        self.clock = pygame.time.Clock()

        # Set game values
        self.SNAKE_SIZE = 20

        self.head_x, self.head_y = random.randint(0, self.WINDOW_WIDTH - self.SNAKE_SIZE), random.randint(0, self.WINDOW_HEIGHT - self.SNAKE_SIZE)

        self.snake_dx, self.snake_dy = 0, 0

        self.score = 0

        # Set colors
        self.GREEN,self.LIGHTGREEN, self.RED, self.BLACK = (0, 255, 0), (127, 193, 129), (255, 0, 0), (0,0,0)
        
        # Set fonts
        self.font = pygame.font.Font('AlwaysSmile-axWYR.ttf', 48)

        # Set text
        self.title_text = self.font.render("~~~Snake~~~", True, self.GREEN)
        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2)

        self.score_text = self.font.render("Score: " + str(self.score), True, self.GREEN)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.topright = (self.WINDOW_WIDTH - 25, 10)

        self.game_over_text = self.font.render("GAMEOVER", True, self.RED, self.LIGHTGREEN)
        self.game_over_rect = self.game_over_text.get_rect()
        self.game_over_rect.center = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2)

        self.continue_text = self.font.render("Press any key to play again", True, self.RED, self.LIGHTGREEN)
        self.continue_rect = self.continue_text.get_rect()
        self.continue_rect.center = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2 + 81)

        #Set images
        #For a rectangle you need (top-left x, top-left y, width, height)
        self.apple_coord = (random.randint(0, self.WINDOW_WIDTH - self.SNAKE_SIZE), random.randint(0, self.WINDOW_HEIGHT - self.SNAKE_SIZE), self.SNAKE_SIZE, self.SNAKE_SIZE)
        self.apple_rect = pygame.draw.rect(self.display_surface, self.RED, self.apple_coord)

        self.head_coord = (self.head_x, self.head_y, self.SNAKE_SIZE, self.SNAKE_SIZE)
        self.head_rect = pygame.draw.rect(self.display_surface, self.GREEN, self.head_coord)
        self.body_coords = []
        self.current_direction = -1
        self.is_game_over = False
        self.player = player
        print(f'Player: {self.player}')
        self.n_games = 0
        self.reward = 0
        self.game_over = False
        self.frame_iterations = 0
        #init the game loop
        if self.player != 'AI':
            self.game_loop()


    def get_score(self):
        return self.score
    
    def get_actions(self):
        return {
            "move_up" : 0,
            "move_right" : 1,
            "move_down" : 2,
            "move_left" : 3,
        }
    
    def get_apple_pos(self):
        return self.apple_coord[0], self.apple_coord[1]
    
    def get_current_pos(self):
        return self.head_coord[0], self.head_coord[1]

    def get_n_games(self):
        return self.n_games

    def get_current_direction(self):
        return self.current_direction

    def get_state(self):
        state = {"direction_up": bool(self.get_current_direction() == 0),
                "direction_right": bool(self.get_current_direction() == 1),
                "direction_down": bool(self.get_current_direction() == 2),
                "direction_left": bool(self.get_current_direction() == 3),
                "danger_horizontal":self.is_collision_snake(point=(self.SNAKE_SIZE, 0, self.SNAKE_SIZE, self.SNAKE_SIZE)),
                "danger_vertical": self.is_collision_snake(point=(0, self.SNAKE_SIZE, self.SNAKE_SIZE, self.SNAKE_SIZE)),
                "food_left": bool(self.get_current_pos()[0] > self.get_apple_pos()[0]),
                "food_right": bool(self.get_current_pos()[0] < self.get_apple_pos()[0]),
                "food_up": bool(self.get_current_pos()[1] > self.get_apple_pos()[1]),
                "food_down": bool(self.get_current_pos()[1] < self.get_apple_pos()[1])
                }
        return np.array(list(state.values()), dtype=int)

    def move(self, event):
        # R,L,U,D
        if event.key == pygame.K_LEFT:
            if self.current_direction != self.get_actions()["move_right"]:
                self.snake_dx = -1*self.SNAKE_SIZE
                self.snake_dy = 0
                self.current_direction = self.get_actions()["move_left"]
        elif event.key == pygame.K_RIGHT:
            if self.current_direction != self.get_actions()["move_left"]:
                self.snake_dx = self.SNAKE_SIZE
                self.snake_dy = 0
                self.current_direction = self.get_actions()["move_right"]
        elif event.key == pygame.K_UP:
            if self.current_direction != self.get_actions()["move_down"]:
                self.snake_dx = 0
                self.snake_dy = -1*self.SNAKE_SIZE
                self.current_direction = self.get_actions()["move_up"]
        elif event.key == pygame.K_DOWN:
            if self.current_direction != self.get_actions()["move_up"]:
                self.snake_dx = 0
                self.snake_dy = self.SNAKE_SIZE
                self.current_direction = self.get_actions()["move_down"]
            
    def is_collision_snake(self, point:tuple = None):
        if point != None:
            return bool(self.head_rect.left - point[0] < 0 or 
                self.head_rect.right + point[0] > self.WINDOW_WIDTH or
                self.head_rect.top - point[1] < 0  or
                self.head_rect.bottom + point[1] > self.WINDOW_HEIGHT or
                point in self.body_coords)
        else:
            return bool(self.head_rect.left < 0 or 
                self.head_rect.right > self.WINDOW_WIDTH or
                self.head_rect.top < 0 or
                self.head_rect.bottom > self.WINDOW_HEIGHT or
                self.head_coord in self.body_coords)
        
    def apple_generator(self):
        self.apple_x = random.randint(0, self.WINDOW_WIDTH - self.SNAKE_SIZE)
        self.apple_y = random.randint(0, self.WINDOW_HEIGHT - self.SNAKE_SIZE)
        self.apple_coord = (self.apple_x, self.apple_y, self.SNAKE_SIZE, self.SNAKE_SIZE)
    
    def is_collision_apple(self):
        if self.head_rect.colliderect(self.apple_rect):
                self.apple_generator()
                self.body_coords.append(self.head_coord)
                self.reward += 100
                self.score += 1
    
    def update_snake_position(self):
        #Update the x,y position of the snakes head and make a new coordinate
        self.head_x += self.snake_dx
        self.head_y += self.snake_dy
        self.head_coord = (self.head_x, self.head_y, self.SNAKE_SIZE, self.SNAKE_SIZE)

    def update_snake_body(self):
        # Add the head coordinate to the last index of the body coordinate list
        # then we remove the first item (reverse list approach) to display the snakes new coordinates
        # this function is what allows the snake's body to follow its head's movement
        self.body_coords += [self.head_coord]
        self.body_coords.pop(0)

    def update_screen(self):
        #Update HUD
        self.score_text = self.font.render("Score: " + str(self.get_score()), True, self.GREEN)

        #Fill the surface
        self.display_surface.fill(self.BLACK)
        
        #Blit HUD
        self.display_surface.blit(self.title_text, self.title_rect)
        self.display_surface.blit(self.score_text, self.score_rect)

        #Blit assets
        for body in self.body_coords:
            pygame.draw.rect(self.display_surface, self.LIGHTGREEN, body)
        self.head_rect = pygame.draw.rect(self.display_surface, self.GREEN, self.head_coord)
        self.apple_rect = pygame.draw.rect(self.display_surface, self.RED, self.apple_coord)

        #Update display and tick clock
        pygame.display.update()
        self.clock.tick(self.FPS)

    def check_game_over(self):

        if not self.is_collision_snake():
            return
        self.display_surface.blit(self.game_over_text, self.game_over_rect)
        self.display_surface.blit(self.continue_text, self.continue_rect)
        pygame.display.update()

        #Pause the game until the player presses a key, then reset the game
        self.is_paused = True
        while self.is_paused:
            for event in pygame.event.get():
                #The player wants to play again
                if event.type == pygame.KEYDOWN:
                    self.reset()
                #The play wants to quit
                if event.type == pygame.QUIT:
                    self.is_paused = False
                    self.running = False


    def reset(self):
        self.score = 0

        self.head_x, self.head_y = random.randint(0, self.WINDOW_WIDTH - self.SNAKE_SIZE), random.randint(0, self.WINDOW_HEIGHT - self.SNAKE_SIZE)
        self.head_coord = (self.head_x, self.head_y, self.SNAKE_SIZE, self.SNAKE_SIZE)
        self.body_coords = []
        self.snake_dx = 0
        self.snake_dy = 0
        self.current_direction = -1
        
        self.apple_coord = (random.randint(0, self.WINDOW_WIDTH - self.SNAKE_SIZE), random.randint(0, self.WINDOW_HEIGHT - self.SNAKE_SIZE), self.SNAKE_SIZE, self.SNAKE_SIZE)
        self.frame_iterations = 0
        self.is_paused = False
    
    def game_loop(self):
        #The main game loop
        self.running = True
        while self.running:
            #Check to see if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                #Move the snake
                if event.type == pygame.KEYDOWN:
                    self.move(event) 

            self.update_snake_body()
            self.update_snake_position()

            self.check_game_over()

            #Check for snake-apple collisions -> increment score
            self.is_collision_apple()
            
            self.update_screen()

        #End the game
        pygame.quit()

if __name__ == "__main__":
    snake = Snake_Game()
    