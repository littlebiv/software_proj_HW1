/*
 * Full C implementation for K-means assignment.
 * Reads points from STDIN (CSV per line), runs k-means and prints centroids.
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define EPSILON 0.001

static void print_an_error_and_exit(void) {
    printf("An Error Has Occurred\n");
    exit(1);
}

static char *trim(char *s) {
    char *end;
    if (!s) return s;
    while (*s && (*s == ' ' || *s == '\t')) s++;
    if (*s == '\0') return s;
    end = s + strlen(s) - 1;
    while (end > s && (*end == ' ' || *end == '\t')) { *end = '\0'; end--; }
    return s;
}

int main(int argc, char **argv) {
    int K, iter;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    double **points = NULL;
    int N = 0;
    int dim = -1;
    char *endptr;
    int i, j;
    double **centroids;
    int *counts;
    double **sums;

    /* Validate argument count */
    if (argc < 2) {
        printf("Incorrect number of clusters!\n");
        return 1;
    }

    /* Parse and validate K */
    K = strtol(argv[1], &endptr, 10);
    if (*endptr != '\0' || K <= 1) {
        printf("Incorrect number of clusters!\n");
        return 1;
    }

    /* Parse and validate iter */
    iter = 400;
    if (argc >= 3) {
        iter = strtol(argv[2], &endptr, 10);
        if (*endptr != '\0' || iter <= 1 || iter >= 800) {
            printf("Incorrect maximum iteration!\n");
            return 1;
        }
    }

    /* Read points from STDIN */
    while ((read = getline(&line, &len, stdin)) != -1) {
        char *buf;
        char *tok;
        int count = 0;
        int idx;
        
        /* Remove trailing newline chars */
        while (read > 0 && (line[read-1] == '\n' || line[read-1] == '\r')) { 
            line[--read] = '\0'; 
        }
        if (read == 0) continue; /* Skip empty lines */
        
        buf = (char*)malloc(strlen(line) + 1);
        if (!buf) print_an_error_and_exit();
        strcpy(buf, line);
        
        tok = strtok(buf, ",");
        while (tok) {
            char *t = trim(tok);
            if (strlen(t) > 0) count++;
            tok = strtok(NULL, ",");
        }
        
        if (count == 0) { 
            free(buf); 
            continue; 
        }
        
        {
            double *vals = (double*)malloc(sizeof(double) * count);
            if (!vals) { 
                free(buf); 
                print_an_error_and_exit(); 
            }
            
            strcpy(buf, line);
            idx = 0;
            tok = strtok(buf, ",");
            while (tok) {
                char *t = trim(tok);
                if (strlen(t) == 0) { 
                    tok = strtok(NULL, ","); 
                    continue; 
                }
                {
                    char *end_val = NULL;
                    double v = strtod(t, &end_val);
                    if (end_val == t || *end_val != '\0') { 
                        free(buf); 
                        free(vals); 
                        print_an_error_and_exit(); 
                    }
                    vals[idx++] = v;
                }
                tok = strtok(NULL, ",");
            }
            free(buf);
            
            if (dim == -1) {
                dim = idx;
            } else if (idx != dim) { 
                free(vals); 
                print_an_error_and_exit(); 
            }
            
            {
                double **tmp = (double**)realloc(points, sizeof(double*) * (N+1));
                if (!tmp) { 
                    free(vals); 
                    print_an_error_and_exit(); 
                }
                points = tmp;
                points[N++] = vals;
            }
        }
    }
    
    if (line) free(line);

    if (N == 0) {
        print_an_error_and_exit();
    }

    /* Validate K < N after knowing N */
    if (K >= N) {
        for (i = 0; i < N; ++i) {
            free(points[i]);
        }
        free(points);
        printf("Incorrect number of clusters!\n");
        return 1;
    }

    /* Initialize centroids as first K points */
    centroids = (double**)malloc(sizeof(double*) * K);
    if (!centroids) print_an_error_and_exit();
    for (i = 0; i < K; ++i) {
        centroids[i] = (double*)malloc(sizeof(double) * dim);
        if (!centroids[i]) print_an_error_and_exit();
        for (j = 0; j < dim; ++j) {
            centroids[i][j] = points[i][j];
        }
    }

    /* Workspace for assignment sums */
    counts = (int*)malloc(sizeof(int) * K);
    sums = (double**)malloc(sizeof(double*) * K);
    if (!counts || !sums) print_an_error_and_exit();
    for (i = 0; i < K; ++i) {
        sums[i] = (double*)malloc(sizeof(double) * dim);
        if (!sums[i]) print_an_error_and_exit();
    }

    /* K-Means Loop */
    {
        double eps_sq = EPSILON * EPSILON;
        int it, p, c, d;
        for (it = 0; it < iter; ++it) {
            /* Zero sums and counts */
            for (i = 0; i < K; ++i) {
                counts[i] = 0;
                for (j = 0; j < dim; ++j) {
                    sums[i][j] = 0.0;
                }
            }
            
            /* Assign points to closest centroid */
            for (p = 0; p < N; ++p) {
                int best = 0;
                double best_d = 0.0;
                
                /* Compute squared distance to centroid 0 */
                for (d = 0; d < dim; ++d) {
                    double diff = points[p][d] - centroids[0][d];
                    best_d += diff * diff;
                }
                
                for (c = 1; c < K; ++c) {
                    double dist = 0.0;
                    for (d = 0; d < dim; ++d) {
                        double diff = points[p][d] - centroids[c][d];
                        dist += diff * diff;
                    }
                    if (dist < best_d) { 
                        best_d = dist; 
                        best = c; 
                    }
                }
                counts[best]++;
                for (d = 0; d < dim; ++d) {
                    sums[best][d] += points[p][d];
                }
            }

            /* Compute new centroids and check movement */
            {
                double max_move_sq = 0.0;
                for (c = 0; c < K; ++c) {
                    if (counts[c] > 0) {
                        double inv = 1.0 / counts[c];
                        double *newc = (double*)malloc(sizeof(double) * dim);
                        if (!newc) print_an_error_and_exit();
                        
                        for (d = 0; d < dim; ++d) {
                            newc[d] = sums[c][d] * inv;
                        }
                        
                        /* Compute squared movement */
                        {
                            double move_sq = 0.0;
                            for (d = 0; d < dim; ++d) {
                                double diff = newc[d] - centroids[c][d];
                                move_sq += diff * diff;
                            }
                            if (move_sq > max_move_sq) {
                                max_move_sq = move_sq;
                            }
                        }
                        for (d = 0; d < dim; ++d) {
                            centroids[c][d] = newc[d];
                        }
                        free(newc);
                    }
                }
                if (max_move_sq < eps_sq) break;
            }
        }
    }

    /* Print centroids */
    {
        int c, d;
        for (c = 0; c < K; ++c) {
            for (d = 0; d < dim; ++d) {
                if (d) printf(",");
                printf("%.4f", centroids[c][d]);
            }
            printf("\n");
        }
    }

    /* Free all memory */
    for (i = 0; i < K; ++i) free(centroids[i]);
    free(centroids);
    for (i = 0; i < K; ++i) free(sums[i]);
    free(sums);
    free(counts);

    for (i = 0; i < N; ++i) free(points[i]);
    free(points);

    return 0;
}