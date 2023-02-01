from sweeppy import Sweep
import numpy as np

with Sweep('/dev/ttyUSB0') as sweep:
    sweep.start_scanning()
    # for scan in sweep.get_scans():
    #     print('{}\n'.format(scan))
    #angle = []
    #distance = []
    X = []
    Y = []
    for scan in sweep.get_scans():
        for i in range(len(scan)):
            for j in range(len(scan[0])):
                for _ in range(3):
                    X.append(np.cos(np.deg2rad(scan[i][j][0]/1000)) * scan[i][j][1])
                    Y.append(np.sin(np.deg2rad(scan[i][j][0]/1000)) * scan[i][j][1])
    print(X,Y)
