from dataclasses import dataclass

@dataclass
class Level:
    name: str
    word_speed: float # 単語の落ちてくる速さ
    word_generation_interval: int # 単語を生成する間隔(ms)
    exist_same_word_count: int # 同時に存在できる単語の数

easy_level = Level("かんたん", 0.7, 4000, 4)
normal_level = Level("ふつう", 1.2, 2000, 5)
hard_level = Level("むずかしい", 1.2, 1000, 6)

LEVELS = [
    easy_level,
    normal_level,
    hard_level
]