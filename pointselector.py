"""
@author: nicolas-alexander-weiss
@created: 2024-10-24

@dependencies: numpy, matplotlib

"""

import numpy as np
from matplotlib import pyplot as plt


class Point_2D:
    """Simple wrapper for a 2D point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x}, y={self.y})"

    def to_numpy(self):
        return np.array([self.x, self.y])
    
    def distance(p1, p2) -> float:
        return np.sqrt(np.square(p1.x - p2.x) + np.square(p1.y - p2.y))

class Point_Selector:

    def __init__(self, x_range=(0, 1), y_range=(0, 1)):

        self.point_list = []

        ##### PYPLOT CODE ##########

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()

        # Set limits, aspect ratio and grid
        self.ax.set_xlim(x_range)
        self.ax.set_ylim(y_range)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.grid(True)

        # Connect the click event handler
        self.fig.canvas.mpl_connect("button_press_event", self)
        ###############################

    def __call__(self, event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # add the point to selection
            self.point_list.append(Point_2D(x, y))
            # Plot the point
            self.ax.plot(x, y, "ro")  # Red dot for clicked points
            self.fig.canvas.draw()  # Redraw the figure

    def run(self):
        plt.show()

    def get_points(self):
        """Getter function for the selected points.

        return
        ----------
        set of Point_2D
        """
        return self.point_list

    def get_points_numpy(self):
        """Returns the set of points as a numpy array.

        return
        ----------
        2d numpy array, each row a point.
        """
        return np.array([p.to_numpy() for p in self.point_list])


if __name__ == "__main__":

    print(
        "-- Select points by clicking into the pyplot figure and then closing the window. --"
    )

    x_range = (0, 1)
    y_range = (0, 1)

    point_selector = Point_Selector(x_range, y_range)
    point_selector.run()

    points = point_selector.get_points_numpy()

    # Outputs selected points:
    print(f"Selected points:\n{points.__repr__()}")
