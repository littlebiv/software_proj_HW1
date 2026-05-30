
EPSILON = 0.001

def main(args, K, max_iters=400):
    checks(K, max_iters, args)
    centroids = []
    for i in range(K):
        centroids.append(args[i])
    for k in range(max_iters):

        cluster = []
        for i in range(K):
            cluster.append([])
        for i in range(len(args)): #assign points to sections by centroids
            min = MAX_INTEGER
            index = 0
            for j in range(K):
                if (dist(args[i], centroids[j])<min):
                    min = dist(args[i], centroids[j])
                    index = j
            cluster[index].append(args[i])
        centroids_new = []
        for i in range(K): #calculate new multi dimentional centroids
            centroids_new.append([])
            for j in range(len(args[0])):
                centroids_new[i].append(0)
            if len(cluster[i]) == 0:
                centroids_new[i] = centroids[i][:]
            else:
                for j in range(len(cluster[i])):
                    for k in range(len(args[0])):
                        centroids_new[i][k] += cluster[i][j][k]
                for j in range(len(args[0])):
                    centroids_new[i][j] /= len(cluster[i])
        diffs = []
        for i in range(K):
            diffs.append(dist(centroids[i], centroids_new[i]))
        if max(diffs) < EPSILON:
            return centroids_new
        centroids = centroids_new
    return centroids


def dist(p1, p2):
    sum = 0
    for i in range(len(p1)):
        sum += (p1[i] - p2[i]) ** 2
    return sum ** 0.5


MAX_INTEGER = 99999999999

def checks(k, max_iters, args):
    if (len(args) <= k or k <= 0):
        print("Incorrect number of clusters!")
        exit(1)
    if (max_iters <= 0 or max_iters > 800):
        print("Incorrect number of iterations!")
        exit(1)
    for i in range(len(args)):
        if (len(args[i]) != len(args[0])):
            print("Incorrect number of dimensions!")
            exit(1)
        for j in range(len(args[i])):
            if (not isinstance(args[i][j], int) and not isinstance(args[i][j], float)):
                print("Incorrect data type!")
                exit(1)

def test():
    args = [[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]]
    K = 2
    print(main(args, K))
if __name__ == "__main__":    
    test()