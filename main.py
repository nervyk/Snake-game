"""
Игра «Змейка». Управляй змейкой и собирай яблоки!
"""

import pygame
import random

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """
    Базовый класс игрового объекта на поле.
    Содержит позицию и метод отрисовки (реализуется в потомках).
    """

    def __init__(self, position=None, body_color=BLACK):
        if position is None:
            # По центру поля
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Метод отрисовки должен быть переопределён в дочерних классах.
        """
        raise NotImplementedError


class Apple(GameObject):
    """
    Яблоко на игровом поле.
    Появляется в случайной клетке.
    """

    def __init__(self):
        super().__init__(body_color=RED)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайные координаты в пределах поля."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """
    Змейка. Управляет движением, ростом и отрисовкой сегментов.
    """

    def __init__(self):
        super().__init__(body_color=GREEN)
        self.reset()

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)  # движение вправо
        self.next_direction = None

    def update_direction(self):
        """Применяет новое направление движения, если оно корректно."""
        if self.next_direction:
            # Запрет разворота назад
            if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещение змейки на одну клетку."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % SCREEN_WIDTH, (head_y + dir_y) % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовка всех сегментов змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает координаты головы."""
        return self.positions[0]


def handle_keys(snake):
    """Обработка нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (CELL_SIZE, 0)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BLACK)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
