import json
import numpy as np
import math
from PIL import Image

T_MAX = 999.0


class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(ray, hit=0, tmin=0):
        pass


class Sphere(Object3D):
    def __init__(self, data, ind=0):
        self.radiusSphere = data['group'][ind]['sphere']['radius']
        self.centerSphere = data['group'][ind]['sphere']['center']
        self.color = tuple(np.array(data['group'][ind]['sphere']['color']))

    def intersect(self, ray, hit, tmin=0.01):
        oc = ray.origin - self.centerSphere
        a = np.dot(ray.direction, ray.direction)
        b = 2 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - pow(self.radiusSphere, 2)
        d = (b * b - 4 * a * c)
        if d < 0:
            return -1
        else:
            d = math.sqrt(d)
            t1 = (-b + d) / (2 * a)
            t2 = (-b - d) / (2 * a)
            if tmin < t1 <= t2:
                t = t1
            else:
                t = t2
            if t < hit.t:
                hit.t = t
                hit.color = self.color


class Group(Object3D):

    def __init__(self):
        self.objects = []

    def addSphere(self, sphere):
        self.objects.append(sphere)

    def intersect(self, ray, hit, tmin=0):
        for s in self.objects:
            s.intersect(ray, hit)


class Camera:
    def generateRay(x, y):
        pass


class OrthographicCamera(Camera):
    def __init__(self, data):
        self.center = np.array(data['orthocamera']['center'])
        self.dir = np.array(data['orthocamera']['direction'])
        self.up = np.array(data['orthocamera']['up'])
        self.size = data['orthocamera']['size']

    def generateRay(self, x, y):
        horizontal = np.cross(self.dir * -1, self.up)
        return self.center + (x - 0.5) * self.size * horizontal + (y - 0.5) * self.size * self.up


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Hit:
    def __init__(self, t=T_MAX, color=(0, 0, 0)):
        self.t = t
        self.color = color


# normalization
def findNormalize(x, y, size):
    return (x + 0.5) / size[0], (y + 0.5) / size[1]


if __name__ == '__main__':
    # read the json file
    with open('scene2.json') as f:
        data = json.load(f)

    SIZE = (250, 250)
    back_color = np.array(data['background']['color'])
    # objects
    orthcam = OrthographicCamera(data)
    groupSphere = Group()
    h = Hit()
    im = Image.new('RGB', SIZE, tuple(back_color))
