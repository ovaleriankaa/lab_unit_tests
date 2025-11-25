This project is a Unit Testing system for Robot Vacuum Simulator.

Its main purpose of simulator is to calculate the cleaning efficiency of a robot based on a predefined path.

It works by taking two main inputs:

A 2D map of a room, represented as a grid of 1s (walls) and 0s (cleanable floor).

A list of commands (a path), such as ["UP", "RIGHT", "DOWN", "LEFT"].

The simulator processes this path step-by-step. It tracks all the unique floor cells the robot visits. If a command tells the robot to move into a wall or off the map, the robot stays in its current position for that turn.

The final output is a single number: the coverage percentage. This is calculated by dividing the number of unique cells the robot visited by the total number of cleanable floor cells on the map.

## Documentation
Documentation for both RobotSimulator and UnitTests is generated automatically.
View it here: [Link to GitHub Pages]