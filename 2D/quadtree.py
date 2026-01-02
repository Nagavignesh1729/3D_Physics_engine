class QuadTree:
    def __init__(self, r, topLeft = None, topRight = None, bottomLeft = None, bottomRight = None):
        self.points = []
        self.range = r
        self.capacity = 1
        
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        
    def _is_within(self, point):
        x0, y0, x1, y1 = self.range
        x, y = point
        return (x0 <= x < x1) and (y0 <= y < y1)
    
    def insert(self, point):
        if self.topLeft is None:
            if len(self.points) < self.capacity:
                self.points.append(point)
            else:
                self.subdivide()
                self.points.append(point)
                for pt in self.points:
                    if self.topLeft._is_within(pt):
                        self.topLeft.insert(pt)
                    elif self.topRight._is_within(pt):
                        self.topRight.insert(pt)
                    elif self.bottomLeft._is_within(pt):
                        self.bottomLeft.insert(pt)
                    elif self.bottomRight._is_within(pt):
                        self.bottomRight.insert(pt)
                    else:
                        pass
                self.points = []   
        else:
            if self.topLeft._is_within(point):
                self.topLeft.insert(point)
            elif self.topRight._is_within(point):
                self.topRight.insert(point)
            elif self.bottomLeft._is_within(point):
                self.bottomLeft.insert(point)
            elif self.bottomRight._is_within(point):
                self.bottomRight.insert(point)
            else:
                pass
        
    def subdivide(self):
        xmin, ymin, xmax, ymax = self.range
        midx = (xmin + xmax)/2
        midy = (ymin + ymax)/2
        topleft_range = (xmin, ymin, midx, midy)
        topright_range = (midx, ymin, xmax, midy)
        bottomleft_range = (xmin, midy, midx, ymax)
        bottomright_range = (midx, midy, xmax, ymax)
        
        self.topLeft = QuadTree(topleft_range)
        self.topRight = QuadTree(topright_range)
        self.bottomLeft = QuadTree(bottomleft_range)
        self.bottomRight = QuadTree(bottomright_range)
    
    def print_tree(self, depth):
        indent = '\t' * depth
        x, y, _x, _y = self.range
        boundary = f"[{x}, {y}] - [{_x}, {_y}]"
        if self.topLeft is not None:
            print(f"{indent}Node: {boundary}")
            self.topLeft.print_tree(depth+1)
            self.topRight.print_tree(depth+1)
            self.bottomLeft.print_tree(depth+1)
            self.bottomRight.print_tree(depth+1)
        else:
            print(f"{indent}Node: {boundary} -> {self.points}")


if __name__ == "__main__":
    test = QuadTree((0, 0, 8, 8))
    points = [
        (1, 1),
        (7, 1),
        (1, 7),
        (7, 7),
        (4, 4),
        (7, 5)
    ]
    for point in points:
        test.insert(point)
        
    test.print_tree(0)