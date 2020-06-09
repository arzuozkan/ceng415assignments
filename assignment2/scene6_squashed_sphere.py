# CENG 415 Applications of Computer Graphics
# Assignment 2 ,Squashed Sphere

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
    def __init__(self, data):
        self.radiusSphere = data['sphere']['radius']
        self.centerSphere = data['sphere']['center']
        self.color = np.array(data['sphere']['color'])

    def intersect(self, ray, hit, tmin=0.01):
        a = 1
        b = 2 * np.dot(ray.origin, ray.direction)
        c = np.dot(ray.origin, ray.origin) - pow(self.radiusSphere, 2)
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
            hit.t = t
            hit.color = self.color
            vector = ray.origin + t * ray.direction - self.centerSphere
            hit.normal = normVector(vector)
            return t


class Transformation(Object3D):
    m = np.zeros((4, 4), float)

    def __init__(self, data):
        self.object = Sphere(data["group"][0]["transform"]["object"])
        scale = np.append(data["group"][0]["transform"]["transformations"][0]["scale"], 1)
        np.fill_diagonal(self.m, scale)

    def intersect(self, ray, hit=0, tmin=0):
        inverse_matrix = np.linalg.inv(self.m)
        new_origin = np.delete(np.dot(inverse_matrix, np.append(ray.origin, 1)), 3)
        new_dir = np.delete(np.dot(inverse_matrix, np.append(ray.direction, 1)), 3)
        r = Ray(new_origin, new_dir)
        self.object.intersect(r, hit)


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
    def __init__(self, t=T_MAX, color=(0, 0, 0), normal=0):
        self.t = t
        self.color = color
        self.normal = normal


# normalization
def findNormalize(x, y, size):
    return (x + 0.5) / size[0], (y + 0.5) / size[1]


def normVector(v):
    return v / np.linalg.norm(v)

if __name__ == '__main__':
    # read the json file
    with open('scene6_squashed_sphere.json') as f:
        data = json.load(f)

    SIZE = (250, 250)
    back_color = np.array(data['background']['color'])
    ambient = np.array(data['background']['ambient'])
    light_dir = np.array(data['light']['direction']) * -1
    light_color = np.array(data['light']['color'])
    # objects
    orthcam = OrthographicCamera(data)
    im = Image.new('RGB', SIZE, tuple(np.array(back_color).dot(255).astype(int)))
    transformedObject = Transformation(data)
    # pixels
    pixel = im.load()

    # ray tracing for every pixel
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            hit = Hit()
            x, y = findNormalize(i, j, SIZE)
            r = orthcam.generateRay(x, y)
            ray = Ray(r, orthcam.dir)
            transformedObject.intersect(ray, hit)

            # make control the t whether there is a hit.
            if hit.t < T_MAX - 1:
                pixel_color = np.array(
                    ambient * hit.color + max(np.dot(light_dir, hit.normal), 0) * hit.color * light_color)
                pixel[i, SIZE[0] - j - 1] = tuple(np.array(pixel_color * 255).astype(int))
            else:
                pixel[i, SIZE[0] - j - 1] = tuple(np.array(ambient * back_color).dot(255).astype(int))
    im.save("scene6_squashed_sphere.jpg")
