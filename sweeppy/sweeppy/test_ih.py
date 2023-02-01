from sweeppy import Sweep
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, degrees, radians, sqrt

def dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def DBSCAN(data, eps, min_pts):
    clusters = []
    visited = set()
    #i에는 데이터 넘버, pt에는 (X,Y)
    for i, pt in enumerate(data):
        if i in visited:
            continue
        visited.add(i)
        #j에는 데이터 넘버, n에는 (X,Y)
        #pt와 n과의 거리가 eps보다 작거나 같으면 j가 이웃데이터
        neighbors = [j for j, n in enumerate(data) if dist(pt, n) <= eps]
        if len(neighbors) < min_pts:
            continue
        cluster = set(neighbors)
        num = 0
        for compclu in clusters:
            if bool(compclu & cluster) == False: # 새로운 클러스터가 기존의 클러스터와 중복되는 요소없으면 추가 
                continue
            elif bool(compclu & cluster) == True: # 새로운 클러스터가 기존의 클러스터와 중복된다면
                if len(compclu) < len(cluster): # 하지만 새로운 클러스터가 기존 클러스터보다 크기가 크면 기존꺼 삭제
                    clusters.remove(compclu)
                    continue #num 유지
                num+=1 # 그렇지 않다면 num 1증가
        if num == 0: # 기존 요소들과 중복되는 요소가 하나도 없는 클러스터라면 추가
            clusters.append(cluster)

        for neighbor in neighbors:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            new_neighbors = [j for j, n in enumerate(data) if dist(data[neighbor], n) <= eps]
            if len(new_neighbors) >= min_pts:
                cluster.update(new_neighbors)
       
    return clusters

#def centor_of_cluster(cluster):

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
    dataXY_temp = []
    dataXY = []
    for scan in sweep.get_scans():
    #for scan in itertools.islice(sweep.get_scans(), 1):

        dataXY = [[200, 0]]
        dataX = [200]
        dataY = [0]

        plot_count += 1
        #print(plot_count)

        for data in scan[0]:
            X= data[1] * cos(radians(data[0])/1000)
            Y= data[1] * sin(radians(data[0])/1000)

            dataX.append(X)
            dataY.append(Y)
            #print (X)
            #print (Y)
            
            dataXY_temp.append(X)
            dataXY_temp.append(Y)
            
            dataXY.append(dataXY_temp)
            dataXY_temp = []
        #print(dataXY[0])
        
        if (plot_count == 5):
            plt.clf()
            plt.scatter(dataX,dataY, marker = '.', color = 'b', s = 200)
            plt.axis([-300, 300, -250, 250])
            plt.pause(0.1)
            plot_count = 0

        #dataXY.append([200,0])
        clusters = DBSCAN(dataXY,20,2)
        #print(dataXY)
        #print(str(dataXY[0]) + " " + str(clusters))
        print(clusters)