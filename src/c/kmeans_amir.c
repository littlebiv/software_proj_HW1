#include <math.h>

int main (int[] args, int K, int iter) {
    int[] *centroids = new int[K];
    int round = 0;
    for (int i=0; i<K; i++){
        centroids[i] = args[i];
    }
    for (int i=K; i<args.length; i++){
        round++;
        if (i == iter) break;
        centroids = calc(args[i], centroids, K, round);
    }
}


int dist (int[] p1; int[] p2) {
    int sum_sq = 0;
    for (int i=0; i<p1.length; i++){
        sum_sq += Math.pow(p1[i]-p2[2], 2);
    }
    return Math.sqrt(sum_sq);
}

int[] calc(int[] num, int[] centroids, int K, int round){
    int min = Math.MAX_NUMBER;
    int index = -1;
    for (int i=0; i<K; i++){
        int temp = dist(num, centroids[i]);
        if (temp<min){
            min = temp;
            index = i;
        }
    }
    centroids[index] = update(centroids[index], num, round);
    return centroids;
}

int[] update(int[] old_centroid, int[] new_point, int round){
    // Implementation for updating centroid
    int[] new_centroid = new int[old_centroid.length];
    for (int i=0; i<old_centroid.length; i++){
        new_centroid[i] = (old_centroid[i]*(round-1) + new_point[i]) / round;
    }
    return new_centroid;
}
