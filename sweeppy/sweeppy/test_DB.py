from sweeppy import Sweep
import numpy as np
import matplotlib.pyplot as plt

class myDBSCAN():
    
    cluster_label = 0
    
    def __init__(self, data_x, data_y, eps, min_samples):
        self.data_x = data_x
        self.data_y = data_y
        self.data_XY = np.array([data_x, data_y])
        self.eps = eps
        self.min_samples = min_samples
        self.labels = [0]*len(data_x)
        
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
    sweep.set_motor_speed(3)            #모터속도 설정
    sweep.set_sample_rate(1000)         #샘플레이트 설정
    speed = sweep.get_motor_speed()
    rate  = sweep.get_sample_rate()
    ready = sweep.get_motor_ready()
    print("Moter speed is " + str(speed))
    print("Sample rate is " + str(rate))
    print("Is device ready? --> " + str(ready))
    sweep.start_scanning()

    for scan in sweep.get_scans():

        # first  index  []  scan_count, 
        # second index  []  sample_count,
        # third  index  []  angle, distance, strength
        # print(scan[0][0][0])

        X = []
        Y = []

        plot_count += 1
        print(plot_count)

        for i in range(len(scan)):
            for j in range(len(scan[0])):
                # angle.append(scan[i][j][0])
                # distance.append(scan[i][j][1])
                      
                # Get X,Y value 
                X.append(np.cos(np.deg2rad(scan[i][j][0]/1000)) * scan[i][j][1])
                Y.append(np.sin(np.deg2rad(scan[i][j][0]/1000)) * scan[i][j][1])

        lidar_cluster = myDBSCAN(X, Y, eps=25, min_samples=3)
        labels = lidar_cluster.run_dbscan()
        
        np_labels = np.array(labels)
        np_X = np.array(X)
        np_Y = np.array(Y)

        # labels = i 인 점들의 인덱스를 전부 모아서 dataX[인덱스]의 평균, dataY[인덱스]의 평균

        colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'olive', 'fuchsia', 'purple', 'midnightblue', 'darkorange', 'lightpink', 'stategray', 'azure']
                
        if (plot_count == 2):
            plt.clf()
            plt.axis([-300, 300, -250, 250])
            noise_clusters = np.unique(np_labels)
            clusters = np.delete(noise_clusters, np.where(noise_clusters == -1))
            for i in clusters:
                indices = np.where(labels == i)
                X_cluster = np_X[indices]
                Y_cluster = np_Y[indices]
                X_center = np.median(X_cluster)
                Y_center = np.median(Y_cluster)
                plt.scatter(X_center, Y_center, color = 'r', marker='^', s=250)
                plt.scatter(X_cluster, Y_cluster, color=colors[i%13], s = 10)
            plt.pause(0.1)
            plot_count = 0

    plt.show()