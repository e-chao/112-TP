import math, random, copy

class Cube():
    def __init__(self, cx, cy, cz, length):
        self.cx, self.cy, self.cz, self.length = cx, cy, cz, length
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.points = self.makeCube()

    def __eq__(self, other):
        return isinstance(other, Cube) and self.points == other.points

    def makeCube(self):
        cx, cy, cz, length = self.cx, self.cy, self.cz, self.length
        origin = [cx-length/2, cy+length/2, cz-length/2]
        point1 = [cx+length/2, cy+length/2, cz-length/2]
        point2 = [cx+length/2, cy-length/2, cz-length/2]
        point3 = [cx-length/2, cy-length/2, cz-length/2]
        point4 = [cx-length/2, cy+length/2, cz+length/2]
        point5 = [cx+length/2, cy+length/2, cz+length/2]
        point6 = [cx+length/2, cy-length/2, cz+length/2]
        point7 = [cx-length/2, cy-length/2, cz+length/2]
        return [origin, point1, point2, point3, point4, point5, point6, point7]

    def updateCenter(self):
        originX = self.points[0][0]
        originY = self.points[0][1]
        originZ = self.points[0][2]
        self.cx = originX + self.length/2
        self.cy = originY - self.length/2
        self.cz = originZ + self.length/2
