# CENG 415 Applications of Computer Graphics
# Assignment 2, Perspective Camera

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

    def __init__(self, data, ind):
        self.radiusSphere = data['group'][ind]['sphere']['radius']
        self.centerSphere = data['group'][ind]['sphere']['center']
        self.color = np.array(data['group'][ind]['sphere']['color'])

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
                vector = ray.origin + t * ray.direction - self.centerSphere
                hit.normal = normVector(vector)

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


# Orthographic camera
class OrthographicCamera(Camera):

    def __init__(self, data):
        self.center = np.array(data['orthocamera']['center'])
        self.dir = np.array(data['orthocamera']['direction'])
        self.up = np.array(data['orthocamera']['up'])
        self.size = data['orthocamera']['size']

    def generateRay(self, x, y):
        horizontal = np.cross(self.dir * -1, self.up)
        return self.center + (x - 0.5) * self.size * horizontal + (y - 0.5) * self.size * self.up


# Perspective Camera
class PerspectiveCamera(Camera):
    def __init__(self, data):
        self.center = np.array(data["perspectivecamera"]['center'])
        self.dir = np.array(data["perspectivecamera"]['direction'])
        self.up = np.array(data["perspectivecamera"]['up'])
        self.angle = data["perspectivecamera"]['angle']

    def generateRay(self, x, y):
        distance_fromcam = 1;
        horizontal = np.cross(self.dir, self.up)
        radian_angle = self.angle * math.pi / 180
        leftbottom = self.center + self.dir * distance_fromcam - math.tan(radian_angle / 2) * self.up \
                     - math.tan(radian_angle / 2) * horizontal
        size = 2 * distance_fromcam * math.tan(radian_angle / 2)
        direction = leftbottom + x * size * horizontal + y * size * self.up - self.center
        return self.center, normVector(direction)

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Hit:
    def __init__(self, t=T_MAX, color=(0, 0, 0), normal=0):
        self.t = t
        self.color = color
        self.normal = normal

# normalization
def findNormalize(x, y, size):
    return (x + 0.5) / size[0], (y + 0.5) / size[1]


def normVector(v):
    return v / np.linalg.norm(v)


def makeGroup(group, data):
    for i in range(5):
        group.addSphere(Sphere(data, i))


if __name__ == '__main__':
    # read the json file
    with open('scene3_perspective.json') as f:
        data = json.load(f)

    # variables
    SIZE = (250, 250)
    back_color = np.array(data['background']['color'])
    ambient = np.array(data['background']['ambient'])
    light_dir = np.array(data['light']['direction']) * -1
    light_color = tuple(np.array(data['light']['color']))

    # objects
    pcam = PerspectiveCamera(data)
    group = Group()

    im = Image.new('RGB', SIZE, tuple(np.array(back_color).dot(255).astype(int)))
    makeGroup(group, data)
    # pixels
    pixel = im.load()

    # ray tracing for every pixel
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            h = Hit()
            x, y = findNormalize(i, j, SIZE)
            ro, rd = pcam.generateRay(x, y)
            ray = Ray(ro, rd)
            group.intersect(ray, h)

            # make control the t whether there is a hit.
            if h.t < T_MAX:
                pixel_color = np.array(ambient * h.color + max(np.dot(light_dir, h.normal), 0) * h.color * light_color)
                pixel[i, SIZE[0] - j - 1] = tuple(np.array(pixel_color * 255).astype(int))
            else:
                pixel[i, SIZE[0] - j - 1] = tuple(np.array(ambient * back_color).dot(255).astype(int))
    im.save("scene3_perspective.jpg")
