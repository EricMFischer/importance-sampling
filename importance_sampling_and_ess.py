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
import matplotlib.pyplot as plt
plt.close('all')

def radius(x, y):
    return np.sqrt(x**2 + y**2)

def expected_theta(dist_vals, x, y):
    return np.mean(dist_vals * radius(x, y))

def trial_density(x, y, sd=1):
    return sd**2 * np.exp(2 * (x + y - 2))

def trial_density_2(x, y, sd):
    return sd**2 * np.exp((-15/(2*sd**2))*(x**2+y**2) + 2*(x+y-2))

def estimate_effective_sample_size(n_samples, trial_density):
    return n_samples / (1 + np.var(trial_density, ddof=1))

n = sorted(np.round(np.power(10, np.arange(0.2, 7.2, 0.2))).astype(int))
print('n: ', n)

n_theta = 35
theta_1 = np.zeros(n_theta)
theta_2 = np.zeros(n_theta)
theta_3 = np.zeros(n_theta)
ess_2 = np.zeros(n_theta)
ess_3 = np.zeros(n_theta)

for i in range(n_theta):
    # sample directly from pi(x,y)
    x_1 = np.random.normal(loc=2, size=n[i])
    y_1 = np.random.normal(loc=2, size=n[i])
    theta_1[i] = expected_theta(1, x_1, y_1)

    # sample from g(x,y) with sd = 1
    sd = 1
    x_2 = np.random.normal(size=n[i])
    y_2 = np.random.normal(size=n[i])
    g_2 = sd**2 * trial_density(x_2, y_2, sd)
    theta_2[i] = expected_theta(g_2, x_2, y_2)
    ess_2[i] = estimate_effective_sample_size(n[i], g_2)

    # sample from g(x,y) with sd = 4
    sd = 4
    x_3 = np.random.normal(scale=sd, size=n[i])
    y_3 = np.random.normal(scale=sd, size=n[i])
    g_3 = trial_density_2(x_3, y_3, sd)
    theta_3[i] = expected_theta(g_3, x_3, y_3)
    ess_3[i] = estimate_effective_sample_size(n[i], g_3)

print('theta_1:', theta_1)
print('theta_2:', theta_2)
print('theta_3:', theta_3)
print('ess_2:', ess_2)
print('ess_3:', ess_3)

# a) plot theta_1, theta_2, theta_3 over n (log scale for n) in one figure
fig = plt.figure()
plt.plot(n, theta_1, color='green')
plt.plot(n, theta_2, color='blue')
plt.plot(n, theta_3, color='red')
plt.xscale('log')
plt.grid()
plt.xlabel('n samples')
plt.ylabel(r'$\theta$')
plt.title(r'$\theta$ over n samples')
plt.legend(['theta 1', 'theta 2', 'theta 3'])
fig.savefig('1a.png', dpi=300)
plt.show()



# b) estimate the "effective sample size" for each alternative (since the samples from alternative
# 1 are all "effective" samples of size 1 as they are drawn directly from the target distribution,
# we use ess*(n1) = n1 as the truth and compare the ess for alternative 2 and 3--i.e. the true
# ess*(n2) and ess*(n3) are the numbers when the estimated errors reach the same level as in
# alternative 1)

theta = theta_1[-1]

def calc_error(x, y, trial_density=1):
    return abs(expected_theta(trial_density, x, y) - theta)

# error drawing directly from pi(x, y)
vals = list(range(1, int(10e3))) + list(range(int(10e3), int(10e5), int(10e3)))
error_1 = np.zeros(len(vals))
for i in range(len(vals)):
    errors_1 = []
    for j in range(50):
        x_1 = np.random.normal(loc=2, size=vals[i])
        y_1 = np.random.normal(loc=2, size=vals[i])
        errors_1.append(calc_error(x_1, y_1))

    error_1[i] = np.mean(errors_1)
print('error_1:', error_1)

# errors for 1st and 2nd trial densities
error_2 = np.zeros(n_theta)
error_3 = np.zeros(n_theta)
for i in range(n_theta):
    errors_2 = []
    errors_3 = []
    for j in range(100):
        x_2 = np.random.normal(size = n[i])
        y_2 = np.random.normal(size = n[i])
        g_2 = trial_density(x_2, y_2, 1)
        errors_2.append(calc_error(x_2, y_2, g_2))

        x_3 = np.random.normal(scale=4, size=n[i])
        y_3 = np.random.normal(scale=4, size=n[i])
        g_3 = trial_density_2(x_3, y_3, 4)
        errors_3.append(calc_error(x_3, y_3, g_3))

    error_2[i] = np.mean(errors_2)
    error_3[i] = np.mean(errors_3)
print('error_2:', error_2)
print('error_3:', error_3)

# estimated effective sample sizes for 1st and 2nd trial densities
def calc_effective_sample_size_estimate(trial_density_errors):
    ess = np.zeros(n_theta)
    for i in range(n_theta):
        indices = np.where(error_1 <= trial_density_errors[i])
        ess[i] = vals[np.min(indices)]
    return ess

ess_2_estimate = calc_effective_sample_size_estimate(error_2)
ess_3_estimate = calc_effective_sample_size_estimate(error_3)
print('ess_2_estimate:', ess_2_estimate)
print('ess_3_estimate:', ess_3_estimate)



# Alternative 2 ess*(n) and ess(n)
fig = plt.figure()
plt.plot(n, ess_2_estimate) # ess*
plt.plot(n, ess_2) # ess
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.xlabel('n samples')
plt.ylabel('ess')
plt.title('Alternative 2 - ess*(n) and ess(n) over n samples')
plt.legend(['ess*(n)', 'ess(n)'])
fig.savefig('1d.png', dpi=300)
plt.show()

# Alternative 3 ess*(n) and ess(n)
fig = plt.figure()
plt.plot(n, ess_3_estimate) # ess*
plt.plot(n, ess_3) # ess
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.xlabel('n samples')
plt.ylabel('ess')
plt.title('Alternative 3 - ess*(n) and ess(n) over n samples')
plt.legend(['ess*(n)', 'ess(n)'])
fig.savefig('1e.png', dpi=300)
plt.show()

# Plot of ess(n2) over ess*(n2) and ess(n3) over ess*(n3)
fig = plt.figure()
indices = np.argsort(ess_2_estimate)
plt.plot(ess_2_estimate[indices], ess_2[indices])
plt.grid()
plt.xlabel('ess*(n)')
plt.ylabel('ess(n)')
plt.title('Alternative 2 - ess(n) over ess*(n)')
fig.savefig('1b.png', dpi=300)
plt.show()

fig = plt.figure()
indices = np.argsort(ess_3_estimate)
plt.plot(ess_3_estimate[indices], ess_3[indices])
plt.grid()
plt.xlabel('ess*(n)')
plt.ylabel('ess(n)')
plt.title('Alternative 3 - ess(n) over ess*(n)')
fig.savefig('1c.png', dpi=300)
plt.show()
