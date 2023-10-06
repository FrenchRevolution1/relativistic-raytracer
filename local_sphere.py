import numpy as np
from PIL import Image
import vec_tool as vt
import sphere_function as sphere
import time

def cam(t):
    return np.array([t, 0.0, 0.0, 0.0])

def lin_solve(a, b):
    if a == 0:
        return False
    else:
        return -b/a

# Determine where the vector intersects the plane
def intersect(point, vector, n_E, d):
    return lin_solve(np.dot(vector, n_E), np.dot(point, n_E) - d)

def inside(v, n_E, d=0):
    return np.dot(v, n_E)-d <= 0

# Create a numpy array with all values zero
size = 101
x = 10
pixels = np.full((size, size, 3), (0, 0, 0), dtype=np.uint8)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Objects
n = 8
obj_scl = sphere.sphere_scl(n)
obj_vct = sphere.sphere_vct(n)

obj_scl = obj_scl + vt.translate(obj_vct, [x, 0, 0])

# Boost
speed = -0.0
obj_vct = vt.boosty(obj_vct, speed)

# Create camera and rays.
camera = cam(0)
ray = np.ones(4)

for m in range(1):
    start_time = time.time()
    camera = cam(0)
    # Iterate through all pixels
    for i in range(size):
        if i%100 == 0:
            pass
            #print(i)
        for j in range(size):
            ray[2] = (j/size - 0.5)/2
            ray[3] = (i/size - 0.5)/2
            ray[0] = - np.sqrt(ray[1]*ray[1] + ray[2]*ray[2] + ray[3]*ray[3])
            
            best = 100000
            
            for l in range(4*n*n+2):
                t = intersect(camera, ray, obj_vct[l], obj_scl[l])
                point = camera + t*ray
                if not inside(ray, obj_vct[l]):
                    pass         
                else:
                    if t < best and t >= 0:
                        on_face = True
                        for r in range(4*n*n + 2):
                            if r != l:
                                if not inside(point, obj_vct[r], obj_scl[r]):
                                    on_face = False
                                    break
                        
                        if on_face:
                            best = t
                            pixels[i][j] = vt.color_vct(obj_vct[l], np.array([0, 0, 1]))
    
    end_time = time.time()
    
    # Convert the numpy array to an image
    img = Image.fromarray(pixels)

    # Save the image to a file
    img.save(f'sphere-loc-{n}.png')
    
    print(end_time-start_time)