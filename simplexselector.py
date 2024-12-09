"""
@author: nicolas-alexander-weiss
@created: 2024-10-24

@dependencies: numpy, matplotlib

# TODO: Should make sure to validate if the selected simplices form a simplicial complex.

"""

from pointselector import *
import time

from matplotlib import patches, lines

EPSILON = 0.05  # To be used as factor to determine if points are nearby.
KEY_TOGGLE_DELAY = 0.5  # Wait time after mode is toggled.


class Simplex:
    """
    Each simplex is expressed by its the vertices it is comprised of.
    """

    def __init__(self, vertex_indices):
        self.vertices = set(vertex_indices)

    def __repr__(self):
        return f"Simplex:{self.vertices.__repr__()}"


class Simplex_Selector(Point_Selector):
    """
    Extends the selector to also allow for creating 2d simplices.
    Now also an ordering over all simplices is added.

    TODO: Make separate event handlers.
    TODO: Make the points pickable. (See event_handling.)

    """

    def __init__(self, x_range=(0, 1), y_range=(0, 1)):
        super(Simplex_Selector, self).__init__(x_range, y_range)

        self.simplex_list = []  # here want to preserve order
        self.selected_point_indices = []
        self.tmp_overdrawn_figures = []

        # attach also a key event handler
        self.simplex_mode_on = False
        self.fig.canvas.mpl_connect("key_press_event", self._key_event_handler)

    def add_selected_point_indices_as_simplex(self):
        self.simplex_list.append(Simplex(self.selected_point_indices))
        self.selected_point_indices = []

    def _key_event_handler(self, event):

        if event.key == "shift":
            self.simplex_mode_on ^= True  # toggle boolean
        elif event.key == "enter" and self.simplex_mode_on:
            self.simplex_mode_on = False

            self.draw_simplex([self.point_list[i] for i in self.selected_point_indices])

            self.add_selected_point_indices_as_simplex()

            # Remove the overdrawn points and redraw figure
            for p in self.tmp_overdrawn_figures:
                p.remove()
            self.tmp_overdrawn_figures = []
            
            self.fig.canvas.draw()  

        time.sleep(KEY_TOGGLE_DELAY)

    # OVERRIDING THE PREVIOUS OBJECT CALL
    def __call__(self, event):
        x, y = event.xdata, event.ydata
        click_point = Point_2D(x, y)

        if x is not None and y is not None:

            if self.simplex_mode_on:  # Simplex selection

                nearest_point_index = int(np.argmin(
                    [p.distance(click_point) for p in self.point_list]
                ))
                nearest_point = self.point_list[nearest_point_index]

                # draw point in blue.
                overdrawn_point, = self.ax.plot(nearest_point.x, nearest_point.y, "bo")
                self.tmp_overdrawn_figures.append(overdrawn_point)
                self.fig.canvas.draw()

                # Add to selected vertices:
                self.selected_point_indices.append(nearest_point_index)

            else:  # Default point selection
                # add the point to selection

                self.point_list.append(click_point)
                point_index = len(self.point_list) - 1

                # Also add as a zero simplex:
                self.simplex_list.append(Simplex((point_index,)))

                # Plot the point
                self.ax.plot(x, y, "ro")  # Red dot for clicked points
                self.fig.canvas.draw()  # Redraw the figure

    def draw_simplex(self, points):
        
        corners = np.array([[p.x,p.y] for p in points ])

        if len(corners) == 3:
            polygon = patches.Polygon(corners,closed=True, fill=True)
            self.ax.add_patch(polygon)

            # print("Drew polygon with corners: ", corners)
        elif len(corners) == 2:
            self.ax.plot(corners[:,0],corners[:,1], "b-")
            
        self.fig.canvas.draw()


if __name__ == "__main__":
    simp_selector = Simplex_Selector()

    simp_selector.run()

    print("Selected Points:", simp_selector.get_points_numpy())
    print(f"Selected Simplices: {simp_selector.simplex_list}")
