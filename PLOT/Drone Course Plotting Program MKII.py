import tkinter as tk
import os
import sys

GRID_SIZE = 13  # Has to be 13 cause starts on 0
CELL_SIZE = 40

# =================================== GUI CREATION ===================================

class RoutePlotter:
    def __init__(self):
        self.window = None
        self.canvas = None
        self.previous_coords = []

    def create_window(self):
        self.window = tk.Tk()  # GUI creation 
        self.window.title("Route Plotting Program for Drone")
        self.canvas = tk.Canvas(self.window, width=CELL_SIZE * GRID_SIZE, height=CELL_SIZE * GRID_SIZE)
        self.canvas.pack()

    def destroy_window(self):
        if self.window:
            self.window.destroy()

    # ================================== PROGRAM RUN DEF =================================

    def run(self):
        print('Initializing Route Plotting Program...')
        while True:
            filename = input("Enter the route instruction filename (or 'STOP' to exit): ")
            if filename.upper() == 'STOP':
                print('Shutting down Route Plotting Program...')
                break

            if not os.path.isfile(filename):
                print(f"Error: File not found: {filename}")
                continue

            try:
                coords = self._plot_route(filename)

                if coords:
                    self.create_window()  # Create the window and canvas for each new file
                    self._show_grid(coords)
                    self._show_drone_position(coords)

                    if self.previous_coords:
                        print('Moved from', self.previous_coords[-1], 'to', coords[-1])
                    else:
                        print('Initial position:', coords[0])

                    self.previous_coords = coords
                    self.window.mainloop()  # Enter the main loop
                    self.destroy_window()  # Close the window after each test

                else:
                    print("Error: Route goes outside the grid or an invalid direction was encountered.")

            except Exception as e:
                print(f"Error: An unexpected error occurred: {str(e)}")

            print()

        print("Route Plotting Program has been stopped.")

    # ================================ ROUTE PLOT FROM FILE ====================================

    def _plot_route(self, filename):  # plot route from file bit
        with open(filename, 'r') as file:
            lines = file.readlines()

        try:
            start_x = int(lines[0])
            start_y = int(lines[1])
        except ValueError:
            print("Error: Invalid start coordinates.")
            return []

        if start_x < 0 or start_x >= GRID_SIZE or start_y < 0 or start_y >= GRID_SIZE:
            print("Error: Drone starts outside the grid.")
            return []

        direction_mapping = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
        current_x, current_y = start_x, start_y
        coordinates = [(current_x, current_y)]

        for instruction in lines[2:]:
            direction = instruction.strip()

            if direction in direction_mapping:
                dx, dy = direction_mapping[direction]
                new_x = current_x + dx
                new_y = current_y + dy

                if new_x < 0 or new_x >= GRID_SIZE or new_y < 0 or new_y >= GRID_SIZE:
                    print("Error: Route goes outside the grid.")
                    return []  # Return an empty list to indicate the route is invalid

                current_x, current_y = new_x, new_y
                coordinates.append((current_x, current_y))
            else:
                print(f"Error: Invalid direction '{direction}' encountered.")
                return []  # Return an empty list to indicate the route is invalid

        for coord in coordinates:
            print(coord)  # Print each coordinate in the list

        return coordinates

    # ================================== CREATING GRID ==================================

    def _show_grid(self, coords):
        self.canvas.delete("all")

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                symbol = ' ' if (x, y) not in coords else 'X'
                if (x, y) == coords[-1]:
                    symbol = 'X'

                self.canvas.create_rectangle(x * CELL_SIZE, (GRID_SIZE - y - 1) * CELL_SIZE,
                                             (x + 1) * CELL_SIZE, (GRID_SIZE - y) * CELL_SIZE,
                                             fill="grey", outline="black")
                self.canvas.create_text((x + 0.5) * CELL_SIZE, (GRID_SIZE - y - 0.5) * CELL_SIZE,
                                        text=symbol)

    # ================================== DRONE FUNCTION =================================

    def _show_drone_position(self, coords):
        current_position = coords[-1]
        print("\rDrone Position: ", current_position, end='')
        sys.stdout.flush()
        self._show_grid(coords)

# ======================================= RUN =======================================

if __name__ == "__main__":
    plotter = RoutePlotter()
    plotter.run()
