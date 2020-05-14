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
    def __init__(self,data,ind=0):
        self.radiusSphere = data['group'][ind]['sphere']['radius']
        self.centerSphere = data['group'][ind]['sphere']['center']
        self.color = tuple(np.array(data['group'][ind]['sphere']['color']))

    def intersect(self,ray,hit=None,tmin=0.001):
        oc=ray.origin-self.centerSphere
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
                t=t1
            t=t2
            hit.t = t
            h.color = self.color
            return t

class Group(Object3D):

    def __init__(self, object):
        self.objects=[]

    def addSphere(self, sphere):
        self.objects.append(sphere)

    def intersect(self,ray, hit, tmin=0):
            pass
class Camera:
    def generateRay(x, y):
        pass


class OrthographicCamera(Camera):
    def __init__(self,data):
        self.center=np.array(data['orthocamera']['center'])
        self.dir=np.array(data['orthocamera']['direction'])
        self.up=np.array(data['orthocamera']['up'])
        self.size=data['orthocamera']['size']

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


def rayTracingColor(image, hit, sphere, orthcamera):
    pixel = image.load()
    # ray tracing for every pixel
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            x, y = findNormalize(i, j, SIZE)
            r = orthcamera.generateRay(x, y)
            ray = Ray(r, orthcamera.dir)
            t = sphere.intersect(ray, hit)
            # make control the t whether there is a hit
            if t != -1:
                hit.color = s.color
                pixel[i, j] = tuple(hit.color)
            else:
                pixel[i, j] = tuple(back_color)
    image.save("scene1.jpg")


def rayTracingDepth(image, hit, sphere, orthcamera):
    # pixels
    pixel = image.load()
    # ray tracing for every pixel
    near = 9
    far = 11
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            x, y = findNormalize(i, j, SIZE)
            r = orthcamera.generateRay(x, y)
            ray = Ray(r, orthcamera.dir)
            t = sphere.intersect(ray, hit)
            # make control the t whether there is a hit
            if t != -1:
                depth = int(round((far - t) / (far - near) * 255) - 1)
                hit.color = (depth, depth, depth)
                pixel[i, j] = hit.color
            else:
                pixel[i, j] = tuple(back_color)
    image.save("scene1_depth.jpg")


if __name__ == '__main__':
    # read the json file
    with open('scene1.json') as f:
        data = json.load(f)

    SIZE = (250, 250)
    back_color = np.array(data['background']['color'])
    # objects
    orthcam = OrthographicCamera(data)
    s = Sphere(data)
    h = Hit()
    im = Image.new('RGB', SIZE, tuple(back_color))

    rayTracingColor(im, h, s, orthcam)
    rayTracingDepth(im, h, s, orthcam)
    print("OK")
