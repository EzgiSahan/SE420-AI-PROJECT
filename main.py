import tkinter as tk
from tkinter import messagebox
import heapq


class GameState:
    # Initializes the room, cost, path, and heuristic attributes.
    def __init__(self, room, cost, path, heuristic):
        self.room = room
        self.cost = cost
        self.path = path
        self.heuristic = heuristic

    # It returns True if the total cost of the current instance is less than the total cost of the other instance, and False otherwise.
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Room Navigation Game")

        self.rooms = [
            ['A', 'B', 'C'],
            ['D', 'E', 'F'],
            ['G', 'H', 'I']
        ]
        self.costs = {'up': 1, 'down': 1, 'right': 2, 'left': 2}
        self.walls = set()

        self.source_label = tk.Label(master, text="Source Room:")
        self.source_entry = tk.Entry(master)
        self.source_label.grid(row=0, column=0)
        self.source_entry.grid(row=0, column=1)

        self.goal_label = tk.Label(master, text="Goal Room:")
        self.goal_entry = tk.Entry(master)
        self.goal_label.grid(row=1, column=0)
        self.goal_entry.grid(row=1, column=1)

        self.wall_label = tk.Label(master, text="Add Walls (room pairs, e.g., AD GH BC EF):")
        self.wall_entry = tk.Entry(master)
        self.wall_label.grid(row=2, column=0)
        self.wall_entry.grid(row=2, column=1)

        self.algorithm_label = tk.Label(master, text="Choose Algorithm:")
        self.algorithm_var = tk.StringVar()
        # The algorithm_var is a StringVar that stores the chosen algorithm.
        # By default, it is set to "Uniform Cost Search." This change makes the default algorithm option clearer.
        self.algorithm_var.set("Uniform Cost Search")
        self.algorithm_dropdown = tk.OptionMenu(master, self.algorithm_var, "Uniform Cost Search", "A* Search")
        self.algorithm_label.grid(row=3, column=0)
        self.algorithm_dropdown.grid(row=3, column=1)

        self.run_button = tk.Button(master, text="Run Algorithm", command=self.run_algorithm)
        self.run_button.grid(row=4, column=0, columnspan=2)

        self.output_text = tk.Text(master, height=15, width=55)
        self.output_text.grid(row=5, column=0, columnspan=2)

        self.canvas = tk.Canvas(master, width=300, height=300)
        self.canvas.grid(row=6, column=0, columnspan=2)

    def draw_board(self, current_room):
        self.canvas.delete("all")  # clears the canvas before redrawing
        cell_size = 100
        wall_color = "black"  # Color for drawing walls

        for i, row in enumerate(self.rooms):  # It processes each row and room of the board in turn.
            for j, r in enumerate(row):  # Gets the index and label of each room in each row.
                x1, y1 = j * cell_size, i * cell_size  # Determines the coordinates of the upper left corner of the room.
                x2, y2 = (j + 1) * cell_size, (i + 1) * cell_size  # Determines the coordinates of the lower right corner of the room.

                # Draw room rectangles and labels
                if r == self.source_entry.get().upper():
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'[{r}]', fill="white")
                elif r == self.goal_entry.get().upper():
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'[{r}]', fill="white")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f'[{r}]', fill="white")

                # Draw walls
                if j < 2 and (r, row[j + 1]) in self.walls:
                    # Draw vertical wall to the right
                    self.canvas.create_line(x2, y1, x2, y2, fill=wall_color, width=2)

                if i < 2 and (r, self.rooms[i + 1][j]) in self.walls:
                    # Draw horizontal wall below
                    self.canvas.create_line(x1, y2, x2, y2, fill=wall_color, width=2)

        # Draw outer boundaries
        self.canvas.create_line(0, 0, 0, 300, fill=wall_color, width=2)
        self.canvas.create_line(0, 0, 300, 0, fill=wall_color, width=2)
        self.canvas.create_line(300, 0, 300, 300, fill=wall_color, width=2)
        self.canvas.create_line(0, 300, 300, 300, fill=wall_color, width=2)

    # The method iterates through each row of the game board(self.rooms) and then througt each room(r) within that row.
    def print_board(self, current_room):
        board_str = ""
        for row in self.rooms:
            for r in row:
                # If the current room(r) matches the current_room parameter, it adds[room] to the board_str, indicating the current position.
                if r == current_room:
                    board_str += f'[{r}]'
                # If there is a wall between the current room and current_room, or vice versa, it adds[] to the board_str.
                elif (r, current_room) in self.walls or (current_room, r) in self.walls:
                    board_str += '[#]'
                # If none of the above conditions are met, it adds a space and the room label to the board_str.
                else:
                    board_str += f' {r} '
            board_str += '\n'
        return board_str

    # The method takes two room labels, room1 and room2, as parameters. It adds the pair(room1, room2) to the self.walls
    def add_wall(self, room1, room2):
        self.walls.add((room1, room2))
        self.walls.add((room2, room1))

        self.draw_board(self.source_entry.get().upper())

    def run_algorithm(self):
        self.walls.clear()

        source = self.source_entry.get().upper()
        goal = self.goal_entry.get().upper()

        # It validates whether the source and goal are valid room labels('A' to 'I') and displays an error message if not.
        if source not in 'ABCDEFGHI' or goal not in 'ABCDEFGHI':
            messagebox.showerror("Error", "Invalid input. Please enter a valid room.")
            return

        if source == goal:
            messagebox.showerror("Error", "Source and goal are the same.")
            return

        # It extracts the user input for walls from the entry field and adds the walls to the game using the add_wall method.
        walls_input = self.wall_entry.get().upper()
        walls_list = [walls_input[i:i + 2] for i in range(0, len(walls_input), 3)]
        for room1, room2 in walls_list:
            self.add_wall(room1, room2)

        algorithm_choice = self.algorithm_var.get()
        if algorithm_choice == 'Uniform Cost Search':
            self.uniform_cost_search(source, goal)
        elif algorithm_choice == 'A* Search':
            self.a_star_search(source, goal)
        else:
            messagebox.showerror("Error", "Invalid algorithm choice.")

        # Add a line of dashes at the end
        self.output_text.insert(tk.END, '-' * 30 + '\n')
        self.output_text.see(tk.END)

    def uniform_cost_search(self, source, goal):
        priority_queue = []  # This queue ensures that states are stored in order of priority.
        heapq.heappush(priority_queue, GameState(source, 0, [source], 0))  # source room, cost, route and estimated cost
        expanded_nodes = 0

        # It enters a loop that continues until the priority queue is empty.
        # In each iteration, it pops the state with the lowest cost from the priority queue and updates the board visualization.
        while priority_queue:
            current_state = heapq.heappop(priority_queue)
            current_room = current_state.room
            current_cost = current_state.cost
            current_path = current_state.path

            self.draw_board(current_room)

            board_str = self.print_board(current_room)
            board_str += f'Cost: {current_cost}\n'
            board_str += f'Path: {current_path}\n'
            self.output_text.insert(tk.END, board_str)
            self.output_text.see(tk.END)

            print(board_str)

            if current_room == goal:
                messagebox.showinfo("Goal Reached", f"Goal reached! Total Cost: {current_cost}")
                return

            expanded_nodes += 1
            if expanded_nodes == 10:
                messagebox.showinfo("Limit Reached", "Expanded node limit reached.")
                return

            # For each possible move, it checks if the move is valid, and if so, it calculates the new state and adds it to the priority queue.
            possible_moves = ['up', 'down', 'right', 'left']
            for move in possible_moves:
                if self.is_valid_move(current_room, move, current_path):
                    new_room = self.move(current_room, move)
                    new_cost = current_cost + self.costs[move]
                    new_path = current_path + [new_room]
                    heapq.heappush(priority_queue, GameState(new_room, new_cost, new_path, 0))

    def a_star_search(self, source, goal):
        # It enters a loop that continues until the priority queue is empty.
        # In each iteration, it pops the state with the lowest total cost (cost + heuristic) from the priority queue and updates the board visualization.
        priority_queue = []
        heapq.heappush(priority_queue, GameState(source, 0, [source], self.manhattan_distance(source, goal)))
        expanded_nodes = 0

        while priority_queue:
            current_state = heapq.heappop(priority_queue)
            current_room = current_state.room
            current_cost = current_state.cost
            current_path = current_state.path

            self.draw_board(current_room)

            board_str = self.print_board(current_room)
            board_str += f'Cost: {current_cost}\n'
            board_str += f'Path: {current_path}\n'
            self.output_text.insert(tk.END, board_str)
            self.output_text.see(tk.END)

            print(board_str)

            if current_room == goal:
                messagebox.showinfo("Goal Reached", f"Goal reached! Total Cost: {current_cost}")
                return

            expanded_nodes += 1
            if expanded_nodes == 10:
                messagebox.showinfo("Limit Reached", "Expanded node limit reached.")
                return

            possible_moves = ['up', 'down', 'right', 'left']
            for move in possible_moves:
                if self.is_valid_move(current_room, move, current_path):
                    new_room = self.move(current_room, move)
                    new_cost = current_cost + self.costs[move]
                    new_path = current_path + [new_room]
                    heuristic = self.manhattan_distance(new_room, goal)
                    heapq.heappush(priority_queue, GameState(new_room, new_cost, new_path, heuristic))

    def manhattan_distance(self, room1, room2):
        # Calculate the Manhattan distance between two rooms
        row1, col1 = self.find_position(room1)
        row2, col2 = self.find_position(room2)
        return abs(row1 - row2) + abs(col1 - col2)

    def is_valid_move(self, current_room, move, path):
        # It uses the find_position method to determine the current row and column of the room in the game board.
        row, col = self.find_position(current_room)
        # The row must be greater than 0, and there should be no wall between the current room and the room above,
        # and the room above should not be in the current path.
        if move == 'up' and row > 0 and (self.rooms[row - 1][col], current_room) not in self.walls and \
                self.rooms[row - 1][col] not in path:
            return True
        elif move == 'down' and row < 2 and (self.rooms[row + 1][col], current_room) not in self.walls and \
                self.rooms[row + 1][col] not in path:
            return True
        # The column must be less than 2, and there should be no wall between the current room and the room to the right,
        # and the room to the right should not be in the current path.
        elif move == 'right' and col < 2 and (self.rooms[row][col + 1], current_room) not in self.walls and \
                self.rooms[row][col + 1] not in path:
            return True
        elif move == 'left' and col > 0 and (self.rooms[row][col - 1], current_room) not in self.walls and \
                self.rooms[row][col - 1] not in path:
            return True
        return False

    def find_position(self, room):
        for i, row in enumerate(self.rooms):  # It traverses the rows and row indices (i) respectively on the 2D room array.
            for j, r in enumerate(row):  # It traverses the rooms (r) and column indices (j) within each row respectively.
                if r == room:
                    return i, j

    def move(self, current_room, direction):
        row, col = self.find_position(current_room)  # determine the current row and column indices of the room in the game board.
        if direction == 'up':
            return self.rooms[row - 1][col]
        elif direction == 'down':
            return self.rooms[row + 1][col]
        elif direction == 'right':
            return self.rooms[row][col + 1]
        elif direction == 'left':
            return self.rooms[row][col - 1]


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
