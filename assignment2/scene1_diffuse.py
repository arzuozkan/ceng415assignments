# CENG 415 Applications of Computer Graphics
# Student: Arzu ÖZKAN 16050111051
# Assignment 2, Diffuse shading

import json
import numpy as np
import math
from PIL import Image, ImageDraw


class Object3D:
    def __init__(self, color):
        self.color = color

    def intersect(ray, hit=0, tmin=0):
        pass


class Sphere(Object3D):

    def __init__(self, data):
        self.radiusSphere = data['group'][0]['sphere']['radius']
        self.centerSphere = data['group'][0]['sphere']['center']
        self.color = np.array(data['group'][0]['sphere']['color'])

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
            t = t2
            hit.t = t
            hit.color = self.color
            vector = ray.origin + t * ray.direction - self.centerSphere
            hit.normal = normVector(vector)
            return t


class Group(Object3D):
    def __init__(self):
        self.objects = []

    def intersect(ray, hit=False, tmin=0):
        pass


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
        horizontal = np.cross(self.dir, self.up)
        return (self.center + (x - 0.5) * self.size * horizontal + (y - 0.5) * self.size * self.up)


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction


class Hit:
    def __init__(self, t=0, color=(0, 0, 0), normal=0):
        self.t = t
        self.color = color
        self.normal = normal


# normalization
def findNormalize(x, y, size):
    return ((x + 0.5) / size[0], (y + 0.5) / size[1])


def normVector(v):
    return v / np.linalg.norm(v)


if __name__ == '__main__':
    # read the json file
    with open('scene1_diffuse.json') as f:
        data = json.load(f)

    # variables
    SIZE = (200, 200)
    back_color = np.array(data['background']['color'])
    ambient = np.array(data['background']['ambient'])
    light_dir = np.array(data['light']['direction']) * -1
    light_color = np.array(data['light']['color'])

    # objects
    orthcam = OrthographicCamera(data)
    s = Sphere(data)
    h = Hit()
    im = Image.new('RGB', SIZE, tuple(np.array(back_color).dot(255).astype(int)))

    # pixels
    pixel = im.load()

    # ray tracing for every pixel
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            x, y = findNormalize(i, j, SIZE)
            r = orthcam.generateRay(x, y)
            ray = Ray(r, orthcam.dir)
            t = s.intersect(ray, h)
            # make control the t whether there is a hit.
            if t != -1:
                pixel_color = np.array(ambient * h.color + max(np.dot(light_dir, h.normal), 0) * h.color * light_color)
                pixel[i, SIZE[0] - j - 1] = tuple(np.array(pixel_color * 255).astype(int))
            else:
                pixel[i, SIZE[0] - j - 1] = tuple(np.array(ambient * back_color).dot(255).astype(int))

    im.save("scene1_diffuse.jpg")
