import time
import sympy

import numpy as np
import matplotlib.pyplot as plt


def generateKeys(lower, upperBound):
    p = sympy.randprime(lower, upperBound)
    q = sympy.randprime(lower, upperBound)
    n = p*q
    return n, p, q


#initialize size of graph
size = 250
x = []
y = []
max_vals_y = [0]
min_vals_y = [0]
maxLim_y = .001
minLim_y = 0

max_vals_x = [0]
min_vals_x = [0]
maxLim_x = 1
minLim_x = 0

#initialize graph
plt.ion()
fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(111)
plt.xlabel('Log2(n) (# of bits)',fontsize=14)
plt.ylabel('Time (sec)',fontsize=14)
plt.title('Factor Time of N',fontsize=18)

x_vec = np.zeros(size)
y_val = [np.zeros(size)]
plt.show()
# plt.pause(1)

points, = ax.plot(x_vec,y_val[0],'-',alpha=0.8,marker='o',linestyle = 'None') 
lines = [points]

counter = 0
while (counter < size):
            
    n,p,q = generateKeys(1e2,10**(counter//100 + 5))
    print(counter)
    start = time.time()
    for i in range(3,n,2):
        if n%i == 0:
            print(n, i, n/i)
            break

    #calculate bit length and duration
    x = np.log2(n)
    y = (time.time() - start) + .0001
    counter +=1

    #publish new points
    fig.canvas.draw()
    fig.canvas.flush_events()

    for i in range(len(lines)):
        #shift values down
        y_val[i] = np.append(y_val[i][1:],0.0)
        x_vec = np.append(x_vec[1:],0.0)
        #assign new values
        y_val[i][-1] = y
        x_vec[-1] = x
        #update plot
        lines[i].set_ydata(y_val[i])
        lines[i].set_xdata(x_vec)

        #Assign new max/min values for data
        min_vals_y[i] = np.min(y_val[i])
        max_vals_y[i] = np.max(y_val[i])

        min_vals_x[i] = np.min(x_vec)
        max_vals_x[i] = np.max(x_vec)


        #assign new y-axis lims if applicable
        if (np.min(min_vals_y) < minLim_y) or np.min(min_vals_y) > minLim_y:
            minLim_y = np.min(min_vals_y)
            plt.ylim([minLim_y, maxLim_y])
        if (np.max(max_vals_y) < maxLim_y) or np.max(max_vals_y) > maxLim_y:
            maxLim_y = np.max(max_vals_y)
            plt.ylim([minLim_y, maxLim_y])

        if (np.min(min_vals_x) < minLim_x) or np.min(min_vals_x) > minLim_x:
            minLim_x = np.min(min_vals_x)
            plt.xlim([minLim_x, maxLim_x + 1])
        if (np.max(max_vals_x) < maxLim_x) or np.max(max_vals_x) > maxLim_x:
            maxLim_x = np.max(max_vals_x)
            plt.xlim([minLim_x, maxLim_x + 1])

#fit line of best fit
fig.canvas.draw()
fig.canvas.flush_events()
exp, offset = np.polyfit(x_vec, np.log2(y_val[0]),1)
xNew = np.linspace(0,60,59)
yNew = np.power(2,exp*xNew + offset)

#plot line of best fit
plt.ioff()
plt.plot(xNew, yNew)
plt.legend(['primes solves','predicted time'])
plt.show()


#Calculate Estimated Durations for given bit sizes
print(xNew, yNew)
print(np.polyfit(x_vec, np.log2(y_val[0]),1))
print("128 AOU", np.power(2,exp*128 + offset)/60/60/24/365/1/1.38e10)
print("256 AOU", np.power(2,exp*256 + offset)/60/60/24/365/1/1.38e10)
print("512 AOU", np.power(2,exp*512 + offset)/60/60/24/365/1/1.38e10)
print("1024 AOU", np.power(2,exp*1024 + offset)/60/60/24/365/1/1.38e10)