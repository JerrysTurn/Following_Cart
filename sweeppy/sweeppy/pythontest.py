#import numpy as np

#data = np.array([[1,2], [3,4], [5,6], [7,8], [9,10]]) # 5x2
#n = data.shape[0] #5
#k_dist = np.zeros(n) # [0,0,0,0,0]
#for i in range(n):
#        point = data[i]
#        distances = np.linalg.norm(data - point, axis=1)
#        
#        distances = np.sort(distances)
#        
#        k_dist[i] = distances[3]
#        print(distances[3])

data = [1,2,3,4]
for i in range(len(data)):
        print(i)
