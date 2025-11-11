from typing import List, Dict, Optional, Tuple

Layout = List[List[int]]
Position = Dict[str, int]
Path = List[str]

class Room:
    
    def __init__(self, layout: Optional[Layout], start_pos: Position):
        self.layout = layout if layout else []
        self.robot_start = start_pos
        
        self.height = len(self.layout)
        self.width = len(self.layout[0]) if self.height > 0 else 0

    def get_area(self) -> int:
        if not self.layout:
            return 0
        
        total = 0
        for row in self.layout:
            for cell in row:
                if cell == 0:
                    total += 1
        return total

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_wall(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            return True  
        
        return self.layout[y][x] == 1


class RobotSimulator:

    def coverage(self, room: Room, path: Path) -> float:
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
