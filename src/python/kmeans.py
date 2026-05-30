#!/usr/bin/env python3
import sys
import math

EPSILON = 0.001

def parse_args(argv, N):
    # argv: program args excluding program name
    if len(argv) < 1:
        print("Incorrect number of clusters!")
        sys.exit(1)
    try:
        K = int(argv[0])
    except Exception:
        print("Incorrect number of clusters!")
        sys.exit(1)
    # iter optional
    if len(argv) >= 2:
        try:
            iters = int(argv[1])
        except Exception:
            print("Incorrect maximum iteration!")
            sys.exit(1)
    else:
        iters = 400
    # validate
    if not (1 < K < N):
        print("Incorrect number of clusters!")
        sys.exit(1)
    if not (1 < iters < 800):
        print("Incorrect maximum iteration!")
        sys.exit(1)
    return K, iters

def read_input():
    data = sys.stdin.read().strip().splitlines()
    points = []
    for line in data:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(',') if p.strip()!='']
        try:
            nums = [float(x) for x in parts]
        except Exception:
            print("An Error Has Occurred")
            sys.exit(1)
        points.append(nums)
    if not points:
        print("An Error Has Occurred")
        sys.exit(1)
    dim = len(points[0])
    for p in points:
        if len(p) != dim:
            print("An Error Has Occurred")
            sys.exit(1)
    return points

def euclidean(a, b):
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))

def kmeans(points, K, max_iter):
    N = len(points)
    dim = len(points[0])
    # init centroids as first K points (copy)
    centroids = [points[i][:] for i in range(K)]
    for iteration in range(max_iter):
        clusters = [[] for _ in range(K)]
        # assign
        for p in points:
            best = 0
            best_d = euclidean(p, centroids[0])
            for i in range(1, K):
                d = euclidean(p, centroids[i])
                if d < best_d:
                    best_d = d
                    best = i
            clusters[best].append(p)
        # update
        moved = 0.0
        new_centroids = []
        for i in range(K):
            if clusters[i]:
                mean = [0.0]*dim
                for p in clusters[i]:
                    for j in range(dim):
                        mean[j] += p[j]
                mean = [x/len(clusters[i]) for x in mean]
            else:
                # if empty cluster, keep previous centroid
                mean = centroids[i]
            new_centroids.append(mean)
            moved = max(moved, euclidean(mean, centroids[i]))
        centroids = new_centroids
        if moved < EPSILON:
            break
    return centroids

def print_centroids(centroids):
    for c in centroids:
        print(','.join(['{:.4f}'.format(x) for x in c]))

def main():
    points = read_input()
    N = len(points)
    K, iters = parse_args(sys.argv[1:], N)
    centroids = kmeans(points, K, iters)
    print_centroids(centroids)

if __name__ == '__main__':
    main()
