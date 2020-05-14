# CENG 415 Applications of Computer Graphics
# Student: Arzu ÖZKAN 16050111051
# Assignment 1

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
    def __init__(self, data, ind=0):
        self.radiusSphere = data['group'][ind]['sphere']['radius']
        self.centerSphere = data['group'][ind]['sphere']['center']
        self.color = tuple(np.array(data['group'][ind]['sphere']['color']))

    def intersect(self, ray, hit=None, tmin=0.001):
        oc = ray.origin - self.centerSphere
        a = np.dot(ray.direction, ray.direction)
        b = 2 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - pow(self.radiusSphere, 2)
        d = (b * b - 4 * a * c)
        if d < 0:
            return -1
        else:
            d = math.sqrt(d)
            # print("a,b,c,d,", a, b, c, d)
            t1 = (-b + d) / (2 * a)
            t2 = (-b - d) / (2 * a)
            if tmin < t1 <= t2:
                t = t1
            t = t2
            hit.t = t
            h.color = self.color
            return t


class Group(Object3D):

    def __init__(self):
        self.objects = []

    def addSphere(self, sphere):
        self.objects.append(sphere)

    def intersect(self, ray, hit, tmin=0):
        hit_tmp = {}
        for s in self.objects:
            t_tmp = s.intersect(ray, hit)
            if (t_tmp != -1):
                hit_tmp[self.objects.index(s)] = -t_tmp
        if len(hit_tmp) == 0:
            hit.color = back_color
            return -1
        else:
            print("hit_tmp, ", list(hit_tmp.values()))
            min_t = min(list(hit_tmp.values()))
            print("mint,", min_t)
            hit.t = min_t
            index = list(hit_tmp.keys())[list(hit_tmp.values()).index(min_t)]
            hit.color = self.objects[index].color
            print("hit.t,hit.color,", hit.t, hit.color)
            return min_t

class Camera:
    def generateRay(x, y):
        pass


class OrthographicCamera(Camera):
    def __init__(self, data):
        self.center = np.array(data['orthocamera']['center'])
        self.dir = np.array(data['orthocamera']['direction']) * -1
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
    def __init__(self, t=0, color=(0, 0, 0)):
        self.t = t
        self.color = color


# normalization
def findNormalize(x, y, size):
    return ((x + 0.5) / size[0], (y + 0.5) / size[1])


def rayTracingColor(image, hit, g):
    pixel = image.load()
    # ray tracing for every pixel
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            x, y = findNormalize(i, j, SIZE)
            r = orthcam.generateRay(x, y)
            ray = Ray(r, orthcam.dir)
            t = g.intersect(ray, hit)
            # make control the t whether there is a hit
            if t != -1:
                # print("hit.color,",hit.color)
                pixel[i, j] = tuple(hit.color)
            else:
                pixel[i, j] = tuple(back_color)
    image.show()


def rayTracingDepth(image, hit, g):
    # pixels
    pixel = image.load()
    # ray tracing for every pixel
    near = 8
    far = 11.5
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            x, y = findNormalize(i, j, SIZE)
            r = orthcam.generateRay(x, y)
            ray = Ray(r, orthcam.dir)
            t = g.intersect(ray, hit)
            # make control the t whether there is a hit
            if t != -1:
                depth = abs(int(round((far - hit.t) / (far - near) * 255) - 1))
                hit.color = (depth, depth, depth)
                print("hit.color,", hit.color)
                pixel[i, j] = hit.color
            else:
                pixel[i, j] = tuple(back_color)
    image.show()


def makeGroup(group, data):
    for i in range(5):
        group.addSphere(Sphere(data, i))


if __name__ == '__main__':
    # read the json file
    with open('scene2.json') as f:
        data = json.load(f)

    SIZE = (100, 100)
    back_color = np.array(data['background']['color'])
    # objects
    orthcam = OrthographicCamera(data)
    groupSphere = Group()
    h = Hit()
    im = Image.new('RGB', SIZE, tuple(back_color))

    makeGroup(groupSphere, data)

    rayTracingColor(im, h, groupSphere)
    rayTracingDepth(im, h, groupSphere)
    print("OK")
