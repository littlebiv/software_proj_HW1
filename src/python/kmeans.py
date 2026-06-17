import sys
import math

EPSILON = 0.001

def main():
    argv = sys.argv[1:]
    
    # --- Parse Arguments (Fail Fast) ---
    if len(argv) < 1:
        print("Incorrect number of clusters!")
        sys.exit(1)
        
    try:
        K = int(argv[0])
        if K <= 1:
            print("Incorrect number of clusters!")
            sys.exit(1)
    except ValueError:
        print("Incorrect number of clusters!")
        sys.exit(1)
        
    if len(argv) >= 2:
        try:
            iters = int(argv[1])
            if not (1 < iters < 800):
                print("Incorrect maximum iteration!")
                sys.exit(1)
        except ValueError:
            print("Incorrect maximum iteration!")
            sys.exit(1)
    else:
        iters = 400

    # --- Read Input Efficiently ---
    points = []
    for line in sys.stdin:
        line = line.strip()
        if not line: 
            continue
        parts = line.split(',')
        try:
            nums = [float(x) for x in parts]
        except ValueError:
            print("An Error Has Occurred")
            sys.exit(1)
        points.append(nums)
        
    N = len(points)
    if N == 0:
        print("An Error Has Occurred")
        sys.exit(1)
        
    if K >= N:
        print("Incorrect number of clusters!")
        sys.exit(1)
        
    dim = len(points[0])
    for p in points:
        if len(p) != dim:
            print("An Error Has Occurred")
            sys.exit(1)

    # --- K-Means Algorithm ---
    # Init centroids as first K points (copy)
    centroids = [points[i][:] for i in range(K)]
    
    for _ in range(iters):
        clusters = [[] for _ in range(K)]
        
        # Assign step: using squared distance for efficiency
        for p in points:
            best = 0
            best_d = sum((a - b) ** 2 for a, b in zip(p, centroids[0]))
            for i in range(1, K):
                d = sum((a - b) ** 2 for a, b in zip(p, centroids[i]))
                if d < best_d:
                    best_d = d
                    best = i
            clusters[best].append(p)
            
        # Update step
        moved = 0.0
        new_centroids = []
        for i in range(K):
            if clusters[i]:
                mean = [0.0] * dim
                cluster_size = len(clusters[i])
                for p in clusters[i]:
                    for j in range(dim):
                        mean[j] += p[j]
                mean = [x / cluster_size for x in mean]
            else:
                # If empty cluster, keep previous centroid
                mean = centroids[i]
            
            new_centroids.append(mean)
            
            # Check convergence using true Euclidean distance
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(mean, centroids[i])))
            if dist > moved:
                moved = dist
                
        centroids = new_centroids
        if moved < EPSILON:
            break
            
    # --- Print Output ---
    for c in centroids:
        print(','.join([f"{x:.4f}" for x in c]))

if __name__ == '__main__':
    main()