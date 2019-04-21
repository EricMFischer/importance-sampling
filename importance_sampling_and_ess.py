'''
Eric Fischer
UID: 303 759 361
emfischer712@ucla.edu

Importance sampling and effective number of samples.
Here we will compare the effectiveness of 3 alternative reference probabilities used in
importance sampling:
1) sampling directly from pi(x,y) (since the 2 dims are independent, we can sample x and y
from the 1d marginal Gaussians)
2) sampling from g(x,y) with standard deviation = 1
3) sampling from g(x,y) with standard deviation = 4
'''

import numpy as np
import math
import matplotlib.pyplot as plt
plt.close('all')

'''
Graph notes
plt.xlabel (r’$\rho$')
plt.ylabel (r’fraction$\leq\rho$’)
plt.legend(['x', 'y'])
plt.grid()
plt.title('Newton')
plt.plot(N, r)
plt.savefig(’P6d.png’, dpi=300)
plt.semilogy(grad_norm)
'''

def pi(x, y):
    return 1/(2*math.pi) * np.exp(-0.5*((x-2)**2 + (y-2)**2))

def g(x, y, sd):
    return 1/(2*math.pi*sd**2) * np.exp(-1/(2*sd**2)*(x**2 + y**2))

# sample directly from pi(x,y)
theta1 = None
n1 = 100 # number of samples

# sample from g(x,y) with standard deviation = 1
theta2 = None

# sample from g(x,y) with standard deviation = 4
theta3 = None

# a) plot theta_1, theta_2, theta_3 over n (log scale for n) in one figure

# b) estimate the "effective sample size" for each alternative (since the samples from alternative
# 1 are all "effective" samples of size 1 as they are drawn directly from the target distribution,
# we use ess*(n1) = n1 as the truth and compare the ess for alternative 2 and 3--i.e. the true
# ess*(n2) and ess*(n3) are the numbers when the estimated errors reach the same level as in
# alternative 1)
# plot ess(n2) over ess*(n2) and ess(n3) over ess*(n3) and discuss the results
plot = None
