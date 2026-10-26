# Auto Snake Player

This project scans your screen while you are playing Google's Snake and attempts to move the snake to collect as many apples as possible.

If you'd like to try it, run Google Snake on a 1920x1080 screen and then run the program.

I'd recommend setting the snake to Turtle speed. The project isn't super well optimized for higher speeds, so it may struggle to keep up.

I also started working on collision detection for walls and the snake's own body, but this was never completed, and I don't currently plan on finishing it.

## Features

Apple detection

Player (snake) detection

Movement tracking to prevent impossible inputs

Direction calculation

Performance optimizations to make the screen scanning and movement as efficient as I could manage

## How it works

When I started this project, my idea to getting the snake to the apple was simple: detect the colors of the apple and the snake to determine their positions on the screen, then calculate 
the difference between their positions and move the snake up down left or right accordingly.

This is a valid approach, but it's definitely not the greatest way of solving the problem

# How I'd do it now

If I were to remake the project to make the snake play reliably, I'd stop treating it as a "react to the apples position and move based on that," and consider it what it really is: pathfinding

For example, I could have the snake board as a grid and use an algorithm such as BFS (breadth first search).

BFS answers: Starting from the snakes head, whats the shortest legal path to the apple without running into the snake

Rather than just comparing the snake and the apples positions, the algorithm explores possible legal moves, starting with the closest position, until it finds a correct path to the apple.

An even more advanced version could also figure out whether out a specific path would leave the snake trapped after eating the apple.

Overall, this isnt the most sophisticated project ive made, but it was an extremely fun project from Grade 11 and a great intro to screen automation and thinking about
how a program can make decisions based on visual info!
