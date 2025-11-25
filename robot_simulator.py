from typing import List, Dict, Optional, Tuple

Layout = List[List[int]]
Position = Dict[str, int]
Path = List[str]

class Room:
    """
    @brief Клас, що описує середовище (кімнату) для робота.
    
    Зберігає структуру кімнати (стіни та вільний простір) і початкову позицію робота.
    """
    def __init__(self, layout: Optional[Layout], start_pos: Position):
        """
        @brief Ініціалізація кімнати.
        
        @param layout Двовимірний список, де 0 - простір, 1 - стіна. Може бути None.
        @param start_pos Словник з координатами {'x': int, 'y': int}.
        """
        self.layout = layout if layout else []
        self.robot_start = start_pos
        
        self.height = len(self.layout)
        self.width = len(self.layout[0]) if self.height > 0 else 0

    def get_area(self) -> int:
        """
        @brief Обчислює площу чистого простору.
        
        @return Кількість клітинок, які не є стінами (значення 0).
        """
        if not self.layout:
            return 0
        
        total = 0
        for row in self.layout:
            for cell in row:
                if cell == 0:
                    total += 1
        return total

    def in_bounds(self, x: int, y: int) -> bool:
        """
        @brief Перевіряє, чи знаходяться координати в межах кімнати.
        
        @param x Координата X (стовпець).
        @param y Координата Y (рядок).
        @return True, якщо координати валідні, інакше False.
        """
        return 0 <= y < self.height and 0 <= x < self.width

    def is_wall(self, x: int, y: int) -> bool:
        """
        @brief Перевіряє наявність стіни за вказаними координатами.
        
        @param x Координата X.
        @param y Координата Y.
        @return True, якщо це стіна або координати поза межами.
        """
        if not self.in_bounds(x, y):
            return True  
        
        return self.layout[y][x] == 1


class RobotSimulator:
    """
    @brief Симулятор руху робота-пилососа.
    
    Відповідає за обробку шляху робота та розрахунок покриття прибирання.
    """

    def coverage(self, room: Room, path: Path) -> float:
        """
        @brief Розраховує відсоток прибирання кімнати.
        
        Симулює рух робота згідно з переданим шляхом. Робот не проходить крізь стіни.
        
        @param room Об'єкт класу Room.
        @param path Список команд ("UP", "DOWN", "LEFT", "RIGHT").
        @return Число від 0.0 до 1.0, що вказує частку прибраної території.
        """
        total = room.get_area()

        if total == 0:
            return 0.0
        
        visited = [[False for _ in range(room.width)] for _ in range(room.height)]

        current_pos = room.robot_start.copy()
        x, y = current_pos['x'], current_pos['y']

        if not room.in_bounds(x, y) or room.is_wall(x, y):
            return 0.0
        
        visited[y][x] = True
        cleaned = 1

        moves = {
            "UP":    {'x': 0,  'y': -1},
            "DOWN":  {'x': 0,  'y': 1},
            "LEFT":  {'x': -1, 'y': 0},
            "RIGHT": {'x': 1,  'y': 0}
        }

        for command in path:

            if command not in moves:
                continue

            delta = moves[command]
            next_x = current_pos['x'] + delta['x']
            next_y = current_pos['y'] + delta['y']

            if room.in_bounds(next_x, next_y) and not room.is_wall(next_x, next_y):
                current_pos['x'] = next_x
                current_pos['y'] = next_y

                if not visited[current_pos['y']][current_pos['x']]:
                    visited[current_pos['y']][current_pos['x']] = True
                    cleaned += 1
            

        return cleaned / total
