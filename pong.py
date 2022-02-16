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

# paddle configs
PADDLE_COLOR = WHITE
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_VELOCITY = 4

# ball configs
BALL_COLOR = WHITE
BALL_MAX_VELOCITY = 5
BALL_RADIUS = 7


# ====================================
# ============= CLASSES ==============
# ====================================

class Paddle:
    def __init__(self, x, y, width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        pygame.draw.rect(win, PADDLE_COLOR, (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        
        if up:
            self.y -= PADDLE_VELOCITY
        else:
            self.y += PADDLE_VELOCITY
            
            
class Ball:
    def __init__(self, x, y, radius=BALL_RADIUS):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = BALL_MAX_VELOCITY
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, BALL_COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        

# ====================================
# ============= METHODS ==============
# ====================================

def draw(win, paddles, ball):
    win.fill(BLACK)
    
    for paddle in paddles:
        paddle.draw(win)
        
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
        
    ball.draw(win)
    
    pygame.display.update()
    
def handle_paddle_movement(key, paddles):
    left, right = paddles
    if key[pygame.K_w] and left.y - PADDLE_VELOCITY >= 0:
        left.move(up=True)
    if key[pygame.K_s] and left.y + (PADDLE_VELOCITY+PADDLE_HEIGHT) <= HEIGHT:
        left.move(up=False)
        
    if key[pygame.K_UP] and right.y - PADDLE_VELOCITY >= 0:
        right.move(up=True)
    if key[pygame.K_DOWN] and right.y + (PADDLE_VELOCITY+PADDLE_HEIGHT) <= HEIGHT:
        right.move(up=False)
        
def handle_ball_movement(ball):
    pass

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    paddles = [left_paddle, right_paddle]
    
    ball = Ball(WIDTH//2, HEIGHT//2)
    
    
    while run:
        clock.tick(FPS)
        draw(WINDOW, paddles, ball)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, paddles)
        
        handle_ball_movement(ball)
    
    pygame.quit()
    
    
if __name__ == '__main__':
    main()