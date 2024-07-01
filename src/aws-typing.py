import pygame
import sys, os
import random
from typing import List
from resources.config import *

# Initialize Pygame
pygame.init()

# 外部ファイルインポート
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstallerの場合
        base_path = sys._MEIPASS
    except Exception:
        # 通常の実行の場合
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 単語集
words_path = resource_path('resources/word.py')
sys.path.insert(0, os.path.dirname(words_path))
from resources.word import WORDS

# 設定値
config_path = resource_path('resources/config.py')
sys.path.insert(0, os.path.dirname(config_path))
from resources.config import *

# Font
font_path = resource_path('resources/fonts/timemachine-wa.ttf')
FONT_SIZE = 36
FONT = pygame.font.Font(font_path, FONT_SIZE)  # 日本語フォントを指定

# # 難易度オプション
# difficulties = ["かんたん", "ふつう", "むずかしい"]

# # ボタンの設定
# button_width, button_height = 200, 50
# button_y = HEIGHT // 2 - button_height // 2
# buttons = []

# for i, diff in enumerate(difficulties):
#     button_x = WIDTH // 4 * (i + 1) - button_width // 2
#     buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))

class Word:
    def __init__(self, text, x):
        self.text = text
        self.x = x
        self.y = 0

    def move(self, speed):
        self.y += speed

    def draw(self, screen):
        text_surface = FONT.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.x, self.y))

class Game:
    GENERATE_WORD = pygame.USEREVENT + 1

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("タイピングゲーム")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.state = START
        self.words:List[Word] = []
        self.current_word = ""
        self.score = 0
        self.time_left = 60  # 60秒のゲーム時間
        self.word_speed = 1 # 単語の落ちてくる速さ
        self.input_text = ""
        self.composition = ""
        self.word_generation_interval = 3000  # 単語を生成する間隔(ms)
        self.exist_same_word_count = 5 #同時に存在できる単語の数
        pygame.time.set_timer(self.GENERATE_WORD, self.word_generation_interval)

    def generate_word(self):
        text = random.choice(WORDS)
        x = random.randint(0, WIDTH - (len(text)*FONT_SIZE/2))  # 日本語文字列の幅を考慮して調整
        return Word(text, x)

    def run(self):
        while True:
            if self.state == START:
                self.start_screen()
            elif self.state == PLAYING:
                self.game_screen()
            elif self.state == GAME_OVER:
                self.game_over_screen()
            elif self.state == RESULT:
                self.result_screen()

    def start_screen(self):
        self.screen.fill(WHITE)
        text = FONT.render("スペースキーを押してスタート", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = PLAYING

    def game_screen(self):
        self.screen.fill(WHITE)

        # Move and draw words
        for word in self.words:
            word.move(self.word_speed)
            word.draw(self.screen)

            # Check for game over
            if word.y > HEIGHT * 9/10:
                self.state = GAME_OVER

        # Draw current word being typed
        current_text = FONT.render(self.current_word, True, RED)
        self.screen.blit(current_text, (10, HEIGHT - 50))

        # Draw score
        score_text = FONT.render(f"スコア: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # Draw time left
        time_text = FONT.render(f"残り時間: {int(self.time_left)}", True, BLACK)
        self.screen.blit(time_text, (WIDTH - 300, 10))

        pygame.display.flip()

        # Update time
        self.time_left -= self.clock.get_time() / 1000
        if self.time_left <= 0:
            self.state = RESULT

        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.current_word = self.current_word[:-1]
                elif event.key == pygame.K_RETURN:
                    for word in self.words:
                        if word.text == self.current_word:
                            self.words.remove(word)
                            self.score += 1
                            break
                    self.current_word = ""
                elif event.unicode:
                    self.current_word += event.unicode
            
            elif event.type == self.GENERATE_WORD:
                if len(self.words) < self.exist_same_word_count:
                    self.words.append(self.generate_word())

    def game_over_screen(self):
        self.screen.fill(RED)
        text = FONT.render(f"ゲームオーバー！{self.score}点でした。。スペースキーでリスタート", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = PLAYING

    def result_screen(self):
        self.screen.fill(WHITE)
        text = FONT.render(f"クリア！あなたのスコア: {self.score}", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, text_rect)

        restart_text = FONT.render("スペースキーでリスタート", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = PLAYING

if __name__ == "__main__":
    game = Game()
    game.run()