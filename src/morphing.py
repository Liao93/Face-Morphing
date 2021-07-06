import cv2
import numpy as np

def wrap_image(src_img, ls_1, ls_wrap):
    result_img = np.zeros_like(src_img)
    for y in range(result_img.shape[0]):#189
        for x in range(result_img.shape[1]):#255
            x_sum = 0
            y_sum = 0
            weight_sum = 0 
            for l, l2 in zip(ls_wrap, ls_1):
                (x2, y2, w) = compute_x2_y2(l, l2, x, y)
                x_sum = x_sum + w*x2
                y_sum = y_sum + w*y2
                weight_sum = weight_sum + w
            (new_x, new_y) = (x_sum/weight_sum, y_sum/weight_sum)
            result_img[y][x] = get_color(new_x, -new_y, src_img)
    return result_img.astype(np.uint8)

def compute_x2_y2(l, l2, x, y, a=1, b=1.0, p=0.5):
    point_p = (l[0][0], -l[0][1])
    point_q = (l[1][0], -l[1][1])
    point_p_2 = (l2[0][0], -l2[0][1])
    point_q_2 = (l2[1][0], -l2[1][1])
    point_x = (x, -y)
    vec_px = vec(point_p, point_x)
    vec_pq = vec(point_p, point_q)
    vec_pq_2 = vec(point_p_2, point_q_2)
    per_vec_pq = perpendicular(vec_pq)
    per_vec_pq_2 = perpendicular(vec_pq_2)
    u = dot(vec_px, vec_pq) / length_2(vec_pq)
    v = dot(vec_px, per_vec_pq) / length(vec_pq)
    x_2 = point_p_2[0] + u*vec_pq_2[0] + v*per_vec_pq_2[0]/length(vec_pq_2)
    y_2 = point_p_2[1] + u*vec_pq_2[1] + v*per_vec_pq_2[1]/length(vec_pq_2)

    if u<0:
        dist = length(vec(point_p_2, (x_2, y_2)))
    elif u>1:
        dist = length(vec(point_q_2, (x_2, y_2)))
    else:
        dist = abs(v)

    w = ( (length(vec_pq_2))**p / (a+dist) ) ** b

    return (x_2, y_2, w) 

def get_color(x, y, src_img):
    i = int(x//1.0)
    j = int(y//1.0)
    if x<0:
        if y<0:
            return src_img[0][0]
        elif y>src_img.shape[0]-1:
            return src_img[src_img.shape[0]-1][0]
        else:
            return src_img[j][0]
    elif x>src_img.shape[1]-1:
        if y<0:
            return src_img[0][src_img.shape[1]-1]
        elif y>src_img.shape[0]-1:
            return src_img[src_img.shape[0]-1][src_img.shape[1]-1]
        else:
            return src_img[j][src_img.shape[1]-1]
    elif y<0 or y>src_img.shape[0]-1:
        if y<0:
            return src_img[0][i]
        elif y>src_img.shape[0]-1:
            return src_img[src_img.shape[0]-1][i]
    else:
        #i = int(x//1.0)
        #j = int(y//1.0)
        a = x-i
        b = y-j
        if i == src_img.shape[1]-1 and j == src_img.shape[0]-1:
            return src_img[j][i]
        elif j == src_img.shape[0]-1:
            return (1.0-a)*src_img[j][i] + (a)*src_img[j][i+1]
        elif i == src_img.shape[1]-1:
            return (1.0-b)*src_img[j][i] + (b)*src_img[j+1][i]
        else:
            f1 = (1.0-a)*src_img[j][i] + (a)*src_img[j][i+1]
            f2 = (1.0-a)*src_img[j+1][i] + (a)*src_img[j+1][i+1]
            return (1.0-b)*f1 + (b)*f2

def vec(p0, p1):
    return (p1[0]-p0[0], p1[1]-p0[1])

def perpendicular(v0):
    return (v0[1], -v0[0])

def dot(v0, v1):
    return (v0[0]*v1[0] + v0[1]*v1[1])

def length(v):
    return ((v[0]**2 + v[1]**2)**0.5)

def length_2(v):
    return (v[0]**2 + v[1]**2)