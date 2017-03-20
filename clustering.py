from random import randint
from math import sin, cos, radians
from numpy import linspace
from numpy.random import normal
from math import sqrt, exp


def get_cluster(num_of_points, d, X, Y):
    points = []
    norm = normal(0, d, num_of_points)
    for i, k in enumerate(linspace(0, 360, num_of_points)):
        x = X + norm[i] * cos(radians(k))
        y = Y + norm[i] * sin(radians(k))
        points.append((x, y))

    return points


def euclid_distance(point_a, point_b):
    x0, y0 = point_a
    x1, y1 = point_b
    print("euclid")
    return sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

def schematic_distance(point_a, point_b):
    print("schematic")
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

def potential(alpha, dist_fn, point_a, point_b):
    return exp(-alpha * dist_fn(point_a, point_b))


def calc_potential(points, dist_fn, alpha):
    pis = []
    for pi in points:
        pk_sum = 0
        for pk in points:
            if pi != pk:
                pot = potential(alpha, dist_fn, pi, pk)
                pk_sum += pot
        pis.append((pi, pk_sum))
    return pis


def sort_by_potential(points):
    return sorted(points, key=lambda x: x[1], reverse=True)


def sub_cluster_potential(points, beta, dist_fn):
    ps = []
    cluster_point, cluster_potential = points[0]
    for p, pot in points[1:]:
        new_potential = pot - cluster_potential * potential(beta, dist_fn, cluster_point, p)
        ps.append((p, new_potential))
    return ps


def calc_avg_dist(points, dist_fn):
    dist_sum = 0
    checked = []
    for p1 in points:
        for p2 in points:
            if p1 != p2 and (p1, p2) not in checked and (p2, p1) not in checked:
                dist_sum += dist_fn(p1, p2)
                checked.append((p1, p2))
    return dist_sum / len(points)


def clusterize(cluster_centers, points, dist_fn):
        clusters = dict()
        for cc in cluster_centers:
            if cc not in clusters:
                clusters[cc] = []
        for point in points:
            dists = []
            for cluster in cluster_centers:
                dist = dist_fn(cluster, point)
                dists.append((cluster, dist))
            c = min(dists, key=lambda x: x[1])
            clusters[c[0]].append(point)
        return clusters



if __name__ == '__main__':
    pass