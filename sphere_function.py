import numpy as np
import vec_tool as vt

def sphere_vct(n):
    base_list = []
    for i in range(n):
        base_list.append([np.cos(np.pi*(i+1)/(n+1) - np.pi/2), 0, np.sin(np.pi*(i+1)/(n+1) - np.pi/2)])
    vct_list = []
    for j in range(4*n):
        for i in range(n):
            vct_list.append(vt.stat_plane(base_list[i][0]*np.cos(2*np.pi*j/(4*n)), base_list[i][0]*np.sin(2*np.pi*j/(4*n)), base_list[i][2]))
    vct_list.append(vt.stat_plane(0, 0, 1))
    vct_list.append(vt.stat_plane(0, 0, -1))
    vct_list = np.array(vct_list)
    
    return vct_list
    
def sphere_scl(n):
    return np.ones(4*n*n+2)

