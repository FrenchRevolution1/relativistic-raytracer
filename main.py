import numpy as np
from PIL import Image
import vec_tool as vt
import sphere_function as sphere

def cam(time):
    return np.array([time, 0.0, 0.0, -1.0])

def lin_solve(a, b):
    if a == 0:
        return 'i'
    else:
        return -b/a

# Determine where the vector intersects the plane
def intersect(point, vector, n_E, d):
    if lin_solve(np.dot(vector, n_E), np.dot(point, n_E) - d) == 'i':
        if np.dot(point, n_E) > 0:
            return 'i'
        else:
            return -np.inf
    return lin_solve(np.dot(vector, n_E), np.dot(point, n_E) - d)

def inside(v, n_E):
    return np.dot(v, n_E) > 0

# Create a numpy array with all values zero
size = 400
x = 28
pixels = np.full((size, size, 3), (0, 0, 0), dtype=np.uint8)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Objects
obj_scl = vt.cube_scl()
obj_vct = vt.cube_vct()
plane_number = 6

#obj_vct = vt.rotate(obj_vct, 0.4)

# Boost
speed = -0.9
sp_vc = np.array([0, 0, speed, 0])
relativity = True
x = 24
obj_list = []

if relativity:
    obj_vct = vt.boosty(obj_vct, speed)
else:
    obj_vct = vt.gal_boost(obj_vct, sp_vc)

obj_scl = obj_scl + vt.translate(obj_vct, [x, 0, 0])


obj=(obj_vct, obj_scl) 
 

camera = cam(-12)
ray = np.ones(4)

camera = cam(24)

for i in range(size):
    if i%100 == 0:
        print(i)
    for j in range(size):
        ray[2] = (j/size - 0.5)/4
        ray[3] = (i/size - 0.5)/4
        ray[0] = - np.sqrt(ray[1]*ray[1] + ray[2]*ray[2] + ray[3]*ray[3])
        
        earliest = 1000
        latest = - 1000
        
        for l in range(plane_number):
            t = intersect(camera, ray, obj[0][l], obj[1][l])
            if t == 'i':
                break
                latest = earliest
            if inside(ray, obj[0][l]):
                if earliest > t:
                    earliest = t
                    
            else:
                if latest < t:
                    latest = t
                    if t >= 0:
                        pixels[i][j] = vt.color_vct(obj[0][l], np.array([-1, 0, 0]))
                    else:
                        pixels[i][j] = (0, 0, 0)
                    
        if latest > earliest:
            pixels[i][j] = (0, 0, 0)

# Convert the numpy array to an image
img = Image.fromarray(pixels)

# Save the image to a file
img.save(f'what{-speed, relativity}.png')
    
