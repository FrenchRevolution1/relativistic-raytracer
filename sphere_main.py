import numpy as np
from PIL import Image
import vec_tool as vt
import sphere_function as sphere

def cam(time):
    return np.array([time, 0.0, 0.0, 0.0])

def lin_solve(a, b):
    if a == 0:
        return False
    else:
        return -b/a

# Determine where the vector intersects the plane
def intersect(point, vector, n_E, d):
    return lin_solve(np.dot(vector, n_E), np.dot(point, n_E) - d)

def inside(v, n_E):
    return np.dot(v, n_E) >= 0

# Create a numpy array with all values zero
n = 7
size = 301
x = 12
pixels = np.full((size, size, 3), (0, 0, 0), dtype=np.uint8)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Objects
obj_scl = sphere.sphere_scl(n)
obj_vct = sphere.sphere_vct(n)

#obj_vct = vt.rotate(obj_vct, 0.2)

# Boost
speed = -0.9
sp_vc = np.array([0, 0, speed, 0])
relativity = True

if relativity:
    obj_vct = vt.boosty(obj_vct, speed)
else:
    obj_vct = vt.gal_boost(obj_vct, sp_vc)

obj_scl = obj_scl + vt.translate(obj_vct, [x, 0, 0])

# Create camera and rays.
camera = cam(0)
ray = np.ones(4)

for m in range(1):
    camera = cam(x)
    # Iterate through all pixels
    for i in range(size):
        if i%100 == 0:
            print(i)
        for j in range(size):
            ray[2] = (j/size - 0.5)/4
            ray[3] = (i/size - 0.5)/4
            ray[0] = - np.sqrt(ray[1]*ray[1] + ray[2]*ray[2] + ray[3]*ray[3])
            
            earliest = 1000
            latest = - 1000
            
            for l in range(4*n*n+2):
                t = intersect(camera, ray, obj_vct[l], obj_scl[l])
                if inside(ray, obj_vct[l]):
                    if earliest > t:
                        earliest = t
                        
                else:
                    if latest < t:
                        latest = t
                        if t >= 0:
                            pixels[i][j] = vt.color_sphere(obj_vct[l])
                        else:
                            pixels[i][j] = (0, 0, 0)
                        
            if latest > earliest:
                pixels[i][j] = (0, 0, 0)

    # Convert the numpy array to an image
    img = Image.fromarray(pixels)

    # Save the image to a file
    img.save(f'output{-speed, relativity}.png')
    
    print(m)
