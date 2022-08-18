import numpy as np


class HomogeneousTransformation:
    def __init__(self):
        self.m1 = [0, 0, 0, 0]
        self.m2 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def set_m1(self, x, y, z):
        self.m1 = [x, y, z, 1]

    def set_m2(self, x, y, z):
        self.m2 = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]

    def get_m1(self):
        return np.delete(self.m1, 3, 0)

    def get_m2(self):
        return self.m2

    def get_translation(self):
        return np.delete(np.dot(self.m2, self.m1), 3, 0)

    def get_rotation_x(self, theta):
        self.m2 = [[1, 0, 0, 0], [0, np.cos(np.deg2rad(theta)), -np.sin(np.deg2rad(theta)), 0], [0, np.sin(np.deg2rad(theta)), np.cos(np.deg2rad(theta)), 0], [0, 0, 0, 1]]
        return np.delete(np.dot(self.m2, self.m1), 3, 0)

    def get_rotation_y(self, theta):
        self.m2 = [[np.cos(np.deg2rad(theta)), 0, np.sin(np.deg2rad(theta)), 0], [0, 1, 0, 0], [-np.sin(np.deg2rad(theta)), 0, np.cos(np.deg2rad(theta)), 0], [0, 0, 0, 1]]
        return np.delete(np.dot(self.m2, self.m1), 3, 0)

    def get_rotation_z(self, theta):
        self.m2 = [[np.cos(np.deg2rad(theta)), -np.sin(np.deg2rad(theta)), 0, 0], [np.sin(np.deg2rad(theta)), np.cos(np.deg2rad(theta)), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        return np.delete(np.dot(self.m2, self.m1), 3, 0)


#HT = HomogeneousTransformation()
#HT.set_m1(1, 1, 1)
#HT.set_m2(0, 0, 0)

#print("Matrix M1 :")
#print(HT.get_m1())
#result = HT.get_rotation_x(45)
#print("Matrix M2: " + str(HT.get_m2()))
#print("The matrix multiplication is :")
#print(result)


