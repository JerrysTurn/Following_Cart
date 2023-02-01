#print(__doc__)


#todo:
#todo : only take moving centroids in consideration 


# Cluster centroid detection
import numpy as np
from sklearn.cluster import KMeans

# Lidar 
from sweeppy import Sweep
import itertools
import sys
from math import cos, sin, degrees, radians 





# ===========================================================================
# Cluster centroids detection, trajectory, return the coordinates for the gibal
# ===========================================================================

def get_cluster_centroid (dataXY,plot_position,titre):
    result = []
    # kmeans = KMeans(n_clusters=10, random_state=0).fit(dataXY)
    kmeans = KMeans().fit(dataXY) 
    centroids = kmeans.cluster_centers_
    labels =  kmeans.labels_
    n_points_by_cluster = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
    #plt.subplot(plot_position)
    dataX, dataY = zip(*dataXY)
    #plt.scatter(dataX, dataY, c=labels.astype(np.float))
    #plt.title(titre)
    
    
    # for each centroids of clusters found we take only >=3 points and < 7 
    for index, (key, value) in enumerate(centroids):
        if len(n_points_by_cluster[index]) >= 3 and len(n_points_by_cluster[index]) < 30:
            #plt.scatter(centroids[index][0],centroids[index][1],color='red')  
            #plt.scatter(centroids[index][0]+30,centroids[index][1],color='yellow')
            result.append(centroids[index])
    return result





# ===========================================================================
# LIDAR data
# ===========================================================================
# on recpere la data du scan 
with Sweep('/dev/ttyUSB0') as sweep:    
    sweep.set_motor_speed(5) 
    sweep.set_sample_rate(1000) 
    speed = sweep.get_motor_speed()
    rate  = sweep.get_sample_rate()
    ready = sweep.get_motor_ready()
    print(speed)
    print(rate)
    print(ready)
    sweep.start_scanning()
    dataXY_temp = []
    dataXY = []
    centroids_history = []
    for scan in sweep.get_scans():
    #for scan in itertools.islice(sweep.get_scans(), 3):
        #print('{}\n'.format(scan))
        dataXY = []
        for data in scan[0]:
            X= data[1] * cos(radians(data[0])/1000)
            Y= data[1] * sin(radians(data[0])/1000)
            #print (X)
            #print (Y)
            dataXY_temp.append(X)
            dataXY_temp.append(Y)
            dataXY.append(dataXY_temp)
            dataXY_temp = []
        #print(dataXY)
        #print(' ')
        centroids_t0 = get_cluster_centroid(dataXY,221,'t0')
        print (centroids_t0)
        print(' ')
        # append  et pop 
        centroids_history.append(centroids_t0)
        #si centroids_history > 10 => centroids_history.pop(0)
        print (centroids_history)
        
        # if (x-xc)**2+(y-yc)**2 < r**2:
        #     return 1
        # else:
        #     return 0

















