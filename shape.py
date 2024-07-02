import random
import math

TWO_PI = 2 * math.pi


class Shape:
    def __init__(self, coords=None):
        if coords is None:
            self.coords = []
        else:
            self.coords = coords

    def add_coords(self, x, y):
        """
        Function to add a coordinate into the shape.
        Runs `validate_coordinates` to check for valid
        coordinates.

        Returns True if coordinates can be added successfully,
        else False. Shape coordinates are updated in-place
        if True.
        """
        self.coords.append(
            (
                x,
                y,
            )
        )
        result = self.validate_coordinates()

        if not result:
            del self.coords[-1]

        return result

    def validate_coordinates(self, new_coords=None):
        """
        Function to validate a list of coordinates on whether:
        1) There are duplicate coordinates
        2) Whether formed polygon is convex

        Returns True if coordinates are valid, else False.
        """
        if new_coords is None:
            new_coords = self.coords

        if len(new_coords) <= 2:
            return True

        return self.is_convex_polygon(new_coords)

    # from https://stackoverflow.com/questions/471962/how-do-i-efficiently-determine-if-a-polygon-is-convex-non-convex-or-complex
    def is_convex_polygon(self, polygon=None):
        """Return True if the polynomial defined by the sequence of 2D
        points is 'strictly convex': points are valid, side lengths non-
        zero, interior angles are strictly between zero and a straight
        angle, and the polygon does not intersect itself.

        NOTES:  1.  Algorithm: the signed changes of the direction angles
                    from one side to the next side must be all positive or
                    all negative, and their sum must equal plus-or-minus
                    one full turn (2 pi radians). Also check for too few,
                    invalid, or repeated points.
                2.  No check is explicitly done for zero internal angles
                    (180 degree direction-change angle) as this is covered
                    in other ways, including the `n < 3` check.
        """
        if polygon is None:
            polygon = self.coords

        try:  # needed for any bad points or direction changes
            # Get starting information
            old_x, old_y = polygon[-2]
            new_x, new_y = polygon[-1]
            new_direction = math.atan2(new_y - old_y, new_x - old_x)
            angle_sum = 0.0
            # Check each point (the side ending there, its angle) and accum. angles
            for ndx, newpoint in enumerate(polygon):
                # Update point coordinates and side directions, check side length
                old_x, old_y, old_direction = new_x, new_y, new_direction
                new_x, new_y = newpoint
                new_direction = math.atan2(new_y - old_y, new_x - old_x)
                if old_x == new_x and old_y == new_y:
                    return False  # repeated consecutive points
                # Calculate & check the normalized direction-change angle
                angle = new_direction - old_direction
                if angle <= -math.pi:
                    angle += TWO_PI  # make it in half-open interval (-Pi, Pi]
                elif angle > math.pi:
                    angle -= TWO_PI
                if ndx == 0:  # if first time through loop, initialize orientation
                    if angle == 0.0:
                        return False
                    orientation = 1.0 if angle > 0.0 else -1.0
                else:  # if other time through loop, check orientation is stable
                    if orientation * angle <= 0.0:  # not both pos. or both neg.
                        return False
                # Accumulate the direction-change angle
                angle_sum += angle
            # Check that the total number of full turns is plus-or-minus 1
            return abs(round(angle_sum / TWO_PI)) == 1
        except (ArithmeticError, TypeError, ValueError):
            return False  # any exception means not a proper convex polygon

    def generate_convex_shape(
        self, max_x: int = 25, max_y: int = 25, max_coords: int = 8
    ):
        """
        Function to generate a random convex shape via Valtr's algorithm.
        """

        if max_x <= 10:
            max_x = 10
        if max_y <= 10:
            max_y = 10
        if max_coords <= 3:
            max_coords = 3

        # Generate random points
        points = [
            (random.randint(0, max_x), random.randint(0, max_y))
            for _ in range(random.randint(3, max_coords))
        ]

        while not self.is_convex_polygon(points):
            points = [
                (random.randint(0, 25), random.randint(0, 25))
                for _ in range(random.randint(3, 8))
            ]

        self.coords = self.convex_hull(points)

    def convex_hull(self, points):
        """
        Function to find the convex hull of a set of points using Valtr's algorithm.
        """
        n = len(points)
        if n < 3:
            return "Convex hull not possible with less than 3 points"

        hull = []

        # Find the leftmost point
        l = 0
        for i in range(1, n):
            if points[i][0] < points[l][0]:
                l = i

        # Start from leftmost point, keep moving counterclockwise until the start point is reached again
        p = l
        while True:
            hull.append(points[p])

            # Search for a point 'q' such that orientation(p, q, r) is counterclockwise for all points 'r'
            q = (p + 1) % n
            for r in range(n):
                if self.orientation(points[p], points[q], points[r]) == 2:
                    q = r

            p = q

            # If we come back to the first point, we have completed the convex hull
            if p == l:
                break

        return hull

    def orientation(self, p, q, r):
        """
        Function to find the orientation of ordered triplet (p, q, r).
        The function returns the following values:
        0 : Collinear points
        1 : Clockwise points
        2 : Counterclockwise points
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or Counterclockwise

    def point_in_polygon(self, x, y):
        if (x, y) in self.coords:
            return True

        # Cast a horizontal ray from the point and count intersections with polygon edges
        intersections = 0
        for i in range(len(self.coords)):
            p1 = self.coords[i]
            p2 = self.coords[(i + 1) % len(self.coords)]

            if y >= min(p1[1], p2[1]) and y <= max(p1[1], p2[1]):
                if x <= max(p1[0], p2[0]):
                    if p1[1] != p2[1]:
                        x_intersect = (y - p1[1]) * (p2[0] - p1[0]) / (
                            p2[1] - p1[1]
                        ) + p1[0]
                        if p1[0] == p2[0] or x <= x_intersect:
                            intersections += 1

        # If the number of intersections is odd, the point is inside the polygon
        return intersections % 2 == 1

    def get_coords(self):
        """
        Function to pretty print coordinates.

        Example:
        1: (5, 25)
        2: (21, 10)
        3: (18, 7)
        4: (6, 11)
        """
        coords = ""
        for i, c in enumerate(self.coords):
            coords += f"{i+1}: {c}\n"

        return coords
