import unittest
from robot_simulator import Room, RobotSimulator 

class TestRobotSimulator(unittest.TestCase):
    """
    @brief Набір модульних тестів для RobotSimulator.
    
    Перевіряє коректність роботи логіки руху, зіткнень та розрахунку площі.
    """

    def setUp(self):
        """
        @brief Налаштування тестового оточення перед кожним тестом.
        
        Створює екземпляри симулятора та тестові кімнати (відкриті, закриті стінами).
        """
        self.sim = RobotSimulator()
        
        layout_2 = [
            [0, 0], 
            [0, 0]]
        self.open_2 = Room(layout_2, {'x': 0, 'y': 0})
        
        layout_3 = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
        self.open_3 = Room(layout_3, {'x': 1, 'y': 1})
        
        layout_3_boxed = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]]
        self.boxed_3 = Room(layout_3_boxed, {'x': 1, 'y': 1})


    def test_empty_room(self): # Test 1
        """
        @brief Перевірка обробки порожньої кімнати.
        @details Якщо layout None або [], площа має бути 0.
        """

        room_none = Room(None, {'x': 0, 'y': 0})
        self.assertEqual(room_none.get_area(), 0)
        
        room_empty_list = Room([], {'x': 0, 'y': 0})
        self.assertEqual(room_empty_list.get_area(), 0)


    def test_only_walls(self): # Test 2
        """
        @brief Перевірка кімнати, що складається лише зі стін.
        """

        layout = [[1, 1, 1], [1, 1, 1]]
        room = Room(layout, {'x': 0, 'y': 0})
        self.assertEqual(room.get_area(), 0)


    def test_no_walls(self): # Test 3
        """
        @brief Перевірка площі відкритої кімнати 2x2.
        """
        self.assertEqual(self.open_2.get_area(), 4)


    def test_wall_and_bounds(self): # Test 4
        """
        @brief Перевірка детекора стін та меж кімнати.
        """
        room = self.boxed_3
        
        # Test coordinates that are explicitly in bounds
        self.assertTrue(room.in_bounds(0, 0))
        self.assertTrue(room.in_bounds(2, 2))
        self.assertTrue(room.in_bounds(1, 1))

        # Test coordinates that are explicitly out of bounds
        self.assertFalse(room.in_bounds(3, 1))
        self.assertFalse(room.in_bounds(1, 3))
        self.assertFalse(room.in_bounds(-1, 1))
        self.assertFalse(room.in_bounds(1, -1))

        # Should be a wall
        self.assertTrue(room.is_wall(0, 0))
        self.assertTrue(room.is_wall(1, 2))
        self.assertTrue(room.is_wall(2, 1))

        # Should not be a wall
        self.assertFalse(room.is_wall(1, 1))


    def test_moves(self): # Test 5
        """
        @brief Перевірка базових рухів (UP, DOWN, LEFT, RIGHT).
        """
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        for direction in directions:
            with self.subTest(direction=direction):
                coverage = self.sim.coverage(
                    self.open_3, 
                    [direction]
                )
                self.assertAlmostEqual(coverage, 2 / 9)


    def test_walls(self): # Test 6
        """
        @brief Перевірка зіткнення зі стінами (робот має стояти на місці).
        """
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        for direction in directions:
            with self.subTest(direction=direction):
                coverage = self.sim.coverage(
                    self.boxed_3, 
                    [direction]
                )
                self.assertAlmostEqual(coverage, 1.0)


    def test_empty_path(self): # Test 7
        """
        @brief Перевірка поведінки при порожньому шляху.
        """
        coverage = self.sim.coverage(self.open_2, [])
        self.assertAlmostEqual(coverage, 1 / 4)


    def test_revisited(self): # Test 8
        """
        @brief Перевірка, що повторне відвідування клітинки не збільшує лічильник.
        """
        coverage = self.sim.coverage(self.open_3, ["UP", "DOWN"])
        self.assertAlmostEqual(coverage, 2 / 9)


    def test_entire_room(self): # Test 9
        """
        @brief Перевірка повного покриття кімнати.
        """
        path = ["RIGHT", "DOWN", "LEFT"]
        coverage = self.sim.coverage(self.open_2, path)
        self.assertAlmostEqual(coverage, 1.0)


    def test_missing_one(self): # Test 10
        """
        @brief Перевірка часткового покриття (пропущена одна клітинка).
        """
        path = ["RIGHT", "DOWN"]
        coverage = self.sim.coverage(self.open_2, path)
        self.assertAlmostEqual(coverage, 3 / 4)

   
    def test_start_on_a_wall(self): # Test 11
        """
        @brief Тест старту всередині стіни (має бути 0 покриття).
        """
        layout = [[1, 0], [0, 0]]
        room = Room(layout, {'x': 0, 'y': 0})
        coverage = self.sim.coverage(room, ["RIGHT"])
        self.assertAlmostEqual(coverage, 0.0)

    
    def test_long_path_1_room(self): # Test 12
        """
        @brief Перевірка довгого шляху в кімнаті 1x1.
        """
        layout = [[0]]
        room = Room(layout, {'x': 0, 'y': 0})
        path = ["UP", "DOWN", "LEFT", "RIGHT", "UP"]
        coverage = self.sim.coverage(room, path)
        self.assertAlmostEqual(coverage, 1.0)


    def test_invalid_commands(self): # Test 13
        """
        @brief Перевірка ігнорування невалідних команд.
        """
        path = ["UP", "JUMP", "RIGHT"]
        coverage = self.sim.coverage(self.open_3, path)
        self.assertAlmostEqual(coverage, 3 / 9)


    def test_starts_out_of_bounds(self): # Test 14
        """
        @brief Перевірка старту за межами мапи.
        """
        layout = [
            [0, 0], 
            [0, 0]]
        room = Room(layout, {'x': -1, 'y': 5})
        coverage = self.sim.coverage(room, ["RIGHT"])
        self.assertAlmostEqual(coverage, 0.0)


    def test_start_is_float(self): # Test 15
        """
        @brief Перевірка реакції на дробові координати (TypeError).
        """
        layout = [
            [0, 0], 
            [0, 0]]
        room = Room(layout, {'x': 1.5, 'y': 0.5}) 
        path = ["UP"]
        with self.assertRaises(TypeError):
            self.sim.coverage(room, path)


    def test_path_is_none(self): # Test 16
        """
        @brief Перевірка обробки path=None (TypeError).
        """
        with self.assertRaises(TypeError):
            self.sim.coverage(self.open_2, None)


    def test_start_pos_is_none(self): # Test 17
        """
        @brief Перевірка обробки start_pos=None (AttributeError).
        """
        room = Room([[0]], None)
        with self.assertRaises(AttributeError):
            self.sim.coverage(room, ["UP"])
       

    def test_path_is_string(self): # Test 18
        """
        @brief Перевірка обробки шляху у вигляді рядка.
        """
        path = "UP"
        coverage = self.sim.coverage(self.open_3, path)
        self.assertAlmostEqual(coverage, 1 / 9)


    def test_layout_with_strings(self): # Test 19
        """
        @brief Перевірка layout з некоректними даними (рядки замість чисел).
        """
        layout = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f']]
        room = Room(layout, {'x': 0, 'y': 0})
        self.assertEqual(room.get_area(), 0)
        coverage = self.sim.coverage(room, ["RIGHT"])
        self.assertAlmostEqual(coverage, 0.0)
   

    def test_lowercase_directions_ignored(self): # Test 20
        """
        @brief Перевірка ігнорування команд у нижньому регістрі.
        """
        path = ["up", "right", "DOWN"]
        coverage = self.sim.coverage(self.open_3, path)
        self.assertAlmostEqual(coverage, 2 / 9)

if __name__ == '__main__':
    unittest.main()