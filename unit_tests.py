import unittest
from solution import Room, RobotSimulator 

class TestRobotSimulator(unittest.TestCase):

    def setUp(self):
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


    # if the room layout is None or an empty list [], the total cleanable area is 0.
    def test_empty_room(self): # Test 1

        room_none = Room(None, {'x': 0, 'y': 0})
        self.assertEqual(room_none.get_area(), 0)
        
        room_empty_list = Room([], {'x': 0, 'y': 0})
        self.assertEqual(room_empty_list.get_area(), 0)

    # if the room layout consists entirely of walls (1), the total cleanable area is 0.
    def test_only_walls(self): # Test 2

        layout = [[1, 1, 1], [1, 1, 1]]
        room = Room(layout, {'x': 0, 'y': 0})
        self.assertEqual(room.get_area(), 0)

    # a simple 2x2 open room correctly reports a total cleanable area of 4.
    def test_no_walls(self): # Test 3
        self.assertEqual(self.open_2.get_area(), 4)

    # check for boundary and wall detection.
    def test_wall_and_bounds(self): # Test 4
        room = self.boxed_3
        
        # In-bounds checks
        self.assertTrue(room.in_bounds(0, 0))
        self.assertTrue(room.in_bounds(2, 2))
        self.assertFalse(room.in_bounds(3, 1))
        self.assertFalse(room.in_bounds(1, 3))
        self.assertFalse(room.in_bounds(-1, 1))

        # Wall checks
        self.assertTrue(room.is_wall(0, 0))
        self.assertFalse(room.is_wall(1, 1))
        self.assertTrue(room.is_wall(1, 2))
        self.assertTrue(room.is_wall(3, 1))

    # checks that a single valid "UP", "DOWN", "LEFT", or "RIGHT"
    def test_moves(self): # Test 5
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        for direction in directions:
            with self.subTest(direction=direction):
                coverage = self.sim.coverage(
                    self.open_3, 
                    [direction]
                )
                self.assertEqual(coverage, 2 / 9)

    # Checks that if the robot moves "UP", "DOWN", "LEFT", or "RIGHT" into a wall, it stays put.
    def test_walls(self): # Test 6
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        for direction in directions:
            with self.subTest(direction=direction):
                coverage = self.sim.coverage(
                    self.boxed_3, 
                    [direction]
                )
                self.assertEqual(coverage, 1 / 1)

    # Verifies that an empty path list
    def test_empty_path(self): # Test 7
        coverage = self.sim.coverage(self.open_2, [])
        self.assertEqual(coverage, 1 / 4)

    # Ensures that a path that revisits a cell counts unique cells correctly
    def test_revisited(self): # Test 8
        coverage = self.sim.coverage(self.open_3, ["UP", "DOWN"])
        self.assertEqual(coverage, 2 / 9)

    # Verifies that a path designed to visit every cleanable cell correctly returns 1.0.
    def test_entire_room(self): # Test 9
        path = ["RIGHT", "DOWN", "LEFT"]
        coverage = self.sim.coverage(self.open_2, path)
        self.assertEqual(coverage, 4 / 4)
        self.assertEqual(coverage, 1.0)

    # Verifies that a path that intentionally misses one cellbreturns the correct fractional coverage.
    def test_missing_one(self): # Test 10
        path = ["RIGHT", "DOWN"]
        coverage = self.sim.coverage(self.open_2, path)
        self.assertEqual(coverage, 3 / 4)

    # Tests a circular path to ensure the final move onto a visited cell isn't counted twice.
    def test_circle(self): # Test 11
        path = ["UP", "RIGHT", "DOWN", "LEFT"]
        coverage = self.sim.coverage(self.open_3, path)
        self.assertEqual(coverage, 4 / 9)

    # Checks the edge case where the robot's start_pos is on a wall
    def test_start_on_a_wall(self): # Test 12
        layout = [[1, 0], [0, 0]]
        room = Room(layout, {'x': 0, 'y': 0})
        coverage = self.sim.coverage(room, ["RIGHT"])
        self.assertEqual(coverage, 0.0)

    # Checks that in a 1x1 room, a long path of collision commands still correctly reports 1.0 coverage.
    def test_long_path_1_room(self): # Test 13
        layout = [[0]]
        room = Room(layout, {'x': 0, 'y': 0})
        path = ["UP", "DOWN", "LEFT", "RIGHT", "UP"]
        coverage = self.sim.coverage(room, path)
        self.assertEqual(coverage, 1 / 1)
        self.assertEqual(coverage, 1.0)

    # Verifies that invalid commands are ignored.
    def test_invalid_commands(self): # Test 14
        path = ["UP", "JUMP", "RIGHT"]
        coverage = self.sim.coverage(self.open_3, path)
        self.assertEqual(coverage, 3 / 9)

    # The robot's start_pos is outside the map boundaries
    def test_starts_out_of_bounds(self): # Test 15
        layout = [
            [0, 0], 
            [0, 0]]
        room = Room(layout, {'x': -1, 'y': 5})
        coverage = self.sim.coverage(room, ["RIGHT"])
        self.assertEqual(coverage, 0.0)

    # Checks that using float coordinates in start_pos
    def test_start_is_float(self): # Test 16
        layout = [
            [0, 0], 
            [0, 0]]
        room = Room(layout, {'x': 1.5, 'y': 0.5}) 
        path = ["UP"]
        with self.assertRaises(TypeError):
            self.sim.coverage(room, path)

    # Checks that passing None
    def test_path_is_none(self): # Test 17
        with self.assertRaises(TypeError):
            self.sim.coverage(self.open_2, None)

   

if __name__ == '__main__':
    unittest.main()