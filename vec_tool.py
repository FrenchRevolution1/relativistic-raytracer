import numpy

def stat_plane(x, y, z):
    return [float(0), float(x), float(y), float(z)]

def cube_vct():
    return numpy.array([stat_plane(-1, 0, 0), stat_plane(1, 0, 0), stat_plane(0, 1, 0), stat_plane(0, -1, 0), stat_plane(0, 0, 1), stat_plane(0, 0, -1)])

def cube_scl():
    return numpy.array([1, 1, 1, 1, 1, 1])

def plane_vct():
    return numpy.array([stat_plane(0, 0, -1), stat_plane(1, 0, 0), stat_plane(-1, 0, 0), stat_plane(0, 1, 0), stat_plane(0, -1, 0)])

def plane_scl():
    return numpy.array([0, 1, 1, 1, 1])

def row_vct():
    return numpy.array([stat_plane(-1, 0, 0), stat_plane(1, 0, 0), stat_plane(0, 1, 0), stat_plane(0, -1, 0)])

def row_scl():
    return numpy.array([1, 1, 1, 1])

def translate(obj_vct, v):
    new_scl = []
    for element in obj_vct:
        new_scl.append(numpy.dot(element, numpy.array(stat_plane(v[0], v[1], v[2]))))
    return numpy.array(new_scl)

def gamma(v):
    return 1/(numpy.sqrt(1-v*v))

def boost(obj_vct, v):
    new_vct = []
    for element in obj_vct:
        new_vct.append([gamma(v)*(element[0] - (v * element[1])), gamma(v)*(element[1] - v * element[0]), element[2], element[3]])
    return numpy.array(new_vct)

def boosty(obj_vct, v):
    new_vct = []
    for element in obj_vct:
        new_vct.append([gamma(v)*(element[0] - (v * element[2])), element[1], gamma(v)*(element[2]-v*element[0]), element[3]])
    return numpy.array(new_vct)

def gal_boost(obj_vct, v):
    new_vct = []
    for element in obj_vct:
        new_vct.append([-numpy.dot(v, element), element[1], element[2], element[3]])
    return numpy.array(new_vct)

def color_vct(v, s):
    c = numpy.dot(numpy.array([v[1], v[2], v[3]]), s)
    norm = numpy.linalg.norm(v)*numpy.linalg.norm(s)
    c = c/norm
    return (0, 0, 150+c*100)

def color_sphere(v):
    a = v[2]/(numpy.sqrt(v[1]*v[1]+v[2]*v[2]))
    return ((1-0.7*numpy.abs(v[3]))*(255+a*255)//2, (1-0.7*numpy.abs(v[3]))*(255-a*255)//2, 0)

def rotate(obj_vct, rad):
    new_vct = []
    for element in obj_vct:
        new_vct.append([element[0], numpy.cos(rad)*element[1]+numpy.sin(rad)*element[3], element[2], element[3]*numpy.cos(rad)-element[1]*numpy.sin(rad)])
    return numpy.array(new_vct)