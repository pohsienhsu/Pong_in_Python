from multiprocessing.sharedctypes import SynchronizedBase
import pygame
pygame.init()

# ====================================
# ============ CONSTANTS =============
# ====================================

# window size
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# caption
pygame.display.set_caption("Pong")

# frame rate
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)

# font
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

# paddle configs
PADDLE_COLOR = WHITE
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_VELOCITY = 4

# ball configs
BALL_COLOR = WHITE
BALL_MAX_VELOCITY = 5
BALL_RADIUS = 7

# game configs
MAX_SCORE = 5


# ====================================
# ============= CLASSES ==============
# ====================================

class Paddle:
    def __init__(self, x, y, width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
        self.x = self.origin_x = x
        self.y = self.origin_y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        pygame.draw.rect(win, PADDLE_COLOR, (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        if up:
            self.y -= PADDLE_VELOCITY
        else:
            self.y += PADDLE_VELOCITY
            
    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
            
            
class Ball:
    def __init__(self, x, y, radius=BALL_RADIUS):
        self.x = self.origin_x = x
        self.y = self.origin_y = y
        self.radius = radius
        self.x_vel = BALL_MAX_VELOCITY
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, BALL_COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
        self.y_vel = 0
        self.x_vel *= -1
        

# ====================================
# ============= METHODS ==============
# ====================================

def draw(win, paddles, ball, scores):
    win.fill(BLACK)
    
    # p1_text = SCORE_FONT.render("P1", 2, WHITE)
    # p2_text = SCORE_FONT.render("P2", 2, WHITE)
    
    s_left, s_right = scores
    s_left_text = SCORE_FONT.render(f"{s_left}", 1, WHITE)
    s_right_text = SCORE_FONT.render(f"{s_right}", 1, WHITE)
    
    # win.blit(p1_text, (WIDTH//4 - s_left_text.get_width()//2, 20))
    # win.blit(p2_text, (WIDTH*3//4 - s_right_text.get_width()//2, 20))
    
    # win.blit(s_left_text, (WIDTH//4 - s_left_text.get_width()//2, 25+p1_text.get_height()))
    # win.blit(s_right_text, (WIDTH*3//4 - s_right_text.get_width()//2, 25+p2_text.get_height()))
    
    win.blit(s_left_text, (WIDTH//4 - s_left_text.get_width()//2, 20))
    win.blit(s_right_text, (WIDTH*3//4 - s_right_text.get_width()//2, 20))
    
    for paddle in paddles:
        paddle.draw(win)
        
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        
    ball.draw(win)
    
    pygame.display.update()
    
def handle_paddle_movement(key, paddles):
    p_left, p_right = paddles
    if key[pygame.K_w] and p_left.y - PADDLE_VELOCITY >= 0:
        p_left.move(up=True)
    if key[pygame.K_s] and p_left.y + (PADDLE_VELOCITY+PADDLE_HEIGHT) <= HEIGHT:
        p_left.move(up=False)
        
    if key[pygame.K_UP] and p_right.y - PADDLE_VELOCITY >= 0:
        p_right.move(up=True)
    if key[pygame.K_DOWN] and p_right.y + (PADDLE_VELOCITY+PADDLE_HEIGHT) <= HEIGHT:
        p_right.move(up=False)
        
def handle_collision(ball, paddles):
    p_left, p_right = paddles
    
    # collision with top-down wall
    if (ball.y + ball.radius >= HEIGHT) or (ball.y - ball.radius <= 0):
        ball.y_vel = (-1)*ball.y_vel
        
    # collision with left paddle
    if ball.x_vel < 0:
        if ball.y >= p_left.y and ball.y <= p_left.y + p_left.height:
            if ball.x - ball.radius <= p_left.x + p_left.width:
                ball.x_vel *= (-1)
                # displacement
                middle_y = p_left.y + p_left.height / 2
                diff_y = middle_y - ball.y
                r_factor = (p_left.height/2) / BALL_MAX_VELOCITY
                ball.y_vel = -(diff_y / r_factor)
    # collision with right paddle    
    else:
        if ball.y >= p_right.y and ball.y <= p_right.y + p_right.height:
            if ball.x - ball.radius >= p_right.x:
                ball.x_vel *= (-1)
                
                # displacement
                middle_y = p_right.y + p_right.height / 2
                diff_y = middle_y - ball.y
                r_factor = (p_right.height/2) / BALL_MAX_VELOCITY
                ball.y_vel = -(diff_y / r_factor)
                

def reset_game_board(ball, paddles):
    p_left, p_right = paddles
    ball.reset()
    p_left.reset()
    p_right.reset()
    
                
def handle_score(ball, paddles, scores):
    s_left, s_right = scores
    scored = False
    if ball.x < 0:
        s_right += 1
        scored = True
    elif ball.x > WIDTH:
        s_left += 1
        scored = True
    if scored:
        reset_game_board(ball, paddles)
        # print(f"Score {s_left}:{s_right}")
    return s_left, s_right

def game_over(ball, paddles, scores):
    s_left, s_right = scores
    if s_left >= MAX_SCORE or s_right >= MAX_SCORE:
        s_left, s_right = 0, 0
        reset_game_board(ball, paddles)
    return s_left, s_right 
    

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    paddles = [left_paddle, right_paddle]
    
    ball = Ball(WIDTH//2, HEIGHT//2)
    
    left_score, right_score = 0, 0
    
    while run:
        clock.tick(FPS)
        draw(WINDOW, paddles, ball, [left_score, right_score])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, paddles)
        
        ball.move()
        handle_collision(ball, paddles)
        left_score, right_score = handle_score(ball, paddles, [left_score, right_score])
        left_score, right_score = game_over(ball, paddles, [left_score, right_score])
    
    pygame.quit()
    
    
if __name__ == '__main__':
    main()