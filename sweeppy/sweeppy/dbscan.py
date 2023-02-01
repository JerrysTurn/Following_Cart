from sweeppy import Sweep
import numpy as np
import matplotlib.pyplot as plt
import time

#sec = 0

class myDBSCAN():
    
    cluster_label = 0
    
    def __init__(self, data_x, data_y, eps, min_samples):
        self.data_x = data_x
        self.data_y = data_y
        self.data_XY = np.array([data_x, data_y])
        self.eps = eps
        self.min_samples = min_samples
        self.labels = [0]*len(data_x)

    def adaptive_eps(lidar_data):
        n = lidar_data.shape[0]
        distances = np.zeros(n)
        for i in range(n):
            point = lidar_data[i]
            diff = lidar_data - point
            dist = np.linalg.norm(diff, axis=1)
            dist[i] = np.inf
            nearest_neighbor_dist = np.min(dist)
            distances[i] = nearest_neighbor_dist
        eps = np.max(distances)
        return eps    

    def k_distance(data, k):

        n = data.shape[0]
        k_dist = np.zeros(n)
        for i in range(n):
            point = data[i]
            distances = np.linalg.norm(data - point, axis=1)
            distances = np.sort(distances)
            k_dist[i] = distances[k] * 0.75
        return k_dist

    # INPUT : x_values, y_values nparray
    def run_dbscan(self):
        
        for point in range(len(self.data_x)):
            
            # pass if already checked
            if not (self.labels[point] == 0):
                continue
            
            # Find all of P's neighboring point
            neighbors = self.get_neighbors(point)
            
            # if len below min_samples, this point is noise
            # it can be border point!! but it will be covered by griowCluster func
            if len(neighbors) < self.min_samples:
                self.labels[point] = -1
            else:
                self.cluster_label += 1
                self.growCluster(point, neighbors)
                
        return self.labels
            
    # OUTPUT - POINT INDEX
    # [[1,3,5,7], [2,4,6,8]...] 
    
    def test_print(self):
        print(self.data_XY)
        print(self.labels)
        print(self.eps)
        print(self.min_samples)
        
    def get_neighbors(self, point):
        neighbors = []
        
        for point_next in range(len(self.data_x)):
            
            # distance threshold below neighbor
            # not-squared for fast calculation
            if abs(self.data_x[point] - self.data_x[point_next]) + abs(self.data_y[point] - self.data_y[point_next]) < self.eps:
                neighbors.append(point_next)
        
        return neighbors
    
    def growCluster(self, point, neighbors):
        self.labels[point] = self.cluster_label
        
        i = 0
        while i < len(neighbors):
            
            # get next point from queue
            point_next = neighbors[i]
            
            # noise or border => border point check
            if self.labels[point_next] == -1:
                self.labels[point_next] = self.cluster_label
            
            elif self.labels[point_next] == 0:
                self.labels[point_next] = self.cluster_label
                
                # Find all neighbors of Pn
                point_next_neighbors = self.get_neighbors(point_next)
                
                if len(point_next_neighbors) >= self.min_samples:
                    neighbors = neighbors + point_next_neighbors
            i += 1

plot_count = 0

with Sweep('/dev/ttyUSB0') as sweep:
    sweep.start_scanning()

    for scan in sweep.get_scans():
        
        # scan은 Scan(samples=[Sample(angle, distance, signal_strength), ...])
        # scan의 index
        # first  index  []  scan_count (=> len은 1로 고정)
        # second index  []  sample_count,
        # third  index  []  angle, distance, strength

        X = []; Y = []

        plot_count += 1

        for i in range(len(scan[0])):
                
            # angle : scan[0][i][0]
            # distance : scan[0][i][1]
                      
            # Get X,Y value 
            X.append(np.cos(np.deg2rad(scan[0][i][0]/1000)) * scan[0][i][1])
            Y.append(np.sin(np.deg2rad(scan[0][i][0]/1000)) * scan[0][i][1])

        data_XY = []
        sort_XY = []
        for i in range(len(X)):
            data_XY.append(X[i])
            data_XY.append(Y[i])
            sort_XY.append(list(data_XY))
            data_XY = []
        #print(sort_XY)
        np_sort_XY = np.array(sort_XY)
        my_eps = myDBSCAN.adaptive_eps(np_sort_XY)
        print(my_eps)

        #lidar_cluster = myDBSCAN(X, Y, eps=25, min_samples=2)
        #labels = lidar_cluster.run_dbscan()
        lidar_cluster_labels = myDBSCAN(X, Y, eps=my_eps, min_samples=4).run_dbscan()
        np_labels = np.array(lidar_cluster_labels)

        #print(" start scanning !!")

        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'olive', 'fuchsia', 'purple', 'midnightblue', 'darkorange', 'lightpink', 'stategray', 'azure']
        
        # if (plot_count == 2):
            
        #     noise_clusters = np.unique(np_labels)
        #     clusters = np.delete(noise_clusters, np.where(noise_clusters == -1))

        #     sort_X_Y= []
        #     for i in clusters:
        #         indices = np.where(lidar_cluster_labels == i)
        #         X_cluster = np.array(X)[indices]; Y_cluster = np.array(Y)[indices]
        #         X_center = np.median(X_cluster); Y_center = np.median(Y_cluster)
        #         sort_X_Y.append(abs(X_center)+abs(Y_center))
            

        #     min_X_Y = min(sort_X_Y)
        #     print(min_X_Y)
        #     plot_count = 0

    #sec = sec + 1
    #time.sleep(1)
        if (plot_count == 2):
                plt.clf()
                plt.axis([-300, 300, -250, 250])
                
                noise_clusters = np.unique(np_labels)
                clusters = np.delete(noise_clusters, np.where(noise_clusters == -1))

                for i in clusters:
                    indices = np.where(lidar_cluster_labels == i)
                    X_cluster = np.array(X)[indices]; Y_cluster = np.array(Y)[indices]
                    X_center = np.median(X_cluster); Y_center = np.median(Y_cluster)
                    plt.scatter(X_center, Y_center, color = 'r', marker='^', s=250)
                    plt.scatter(X_cluster, Y_cluster, color=colors[i%13], s = 3)
                plt.pause(0.1)
                plot_count = 0
    plt.show()