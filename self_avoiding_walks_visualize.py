'''
Eric Fischer
UID: 303 759 361
emfischer712@ucla.edu

Visualization file
'''
import matplotlib.pyplot as plt
import pickle
plt.close('all')

# a) Plot K against m in a log-log plot and monitor whether the Sequential Importance Sampling
# (SIS) process has converged.

with open('design_1_saws.pkl', 'rb') as f:
    estimated_SAWs = pickle.load(f)
if not estimated_SAWs:
    with open('design_1_saws.txt') as f:
        records = f.readlines()
    records = [x.strip().split() for x in records]
    estimated_SAWs = [float(record[0]) for record in records]
    f_handler = open("design_1_saws.pkl", "wb")
    pickle.dump(estimated_SAWs, f_handler)

with open('design_2_saws.pkl', 'rb') as f:
    estimated_SAWs2 = pickle.load(f)
if not estimated_SAWs2:
    with open('design_2_saws.txt') as f:
        records = f.readlines()
    records = [x.strip().split() for x in records]
    estimated_SAWs2 = [float(record[0]) for record in records]
    f_handler = open("design_2_saws.pkl", "wb")
    pickle.dump(estimated_SAWs2, f_handler)

with open('design_3_saws.pkl', 'rb') as f:
    estimated_SAWs3 = pickle.load(f)
if not estimated_SAWs3:
    with open('design_3_saws.txt') as f:
        records = f.readlines()
    records = [x.strip().split() for x in records]
    estimated_SAWs3 = [float(record[0]) for record in records]
    f_handler = open("design_3_saws.pkl", "wb")
    pickle.dump(estimated_SAWs3, f_handler)

fig = plt.figure()
plt.plot(estimated_SAWs, color='green')
plt.plot(estimated_SAWs2, color='blue')
plt.plot(estimated_SAWs3, color='red')
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.xlabel('M samples')
plt.ylabel('Estimated number of SAW')
plt.title('Estimated Number of Self-Avoiding Walks for M Samples')
plt.legend(['Design 1', 'Design 2', 'Design 3'])
fig.savefig('2a.png', dpi=300)
plt.show()

# c) For each experiment in a) and b), plot the distribution of the lengths N of the SAWs
# in a histogram (think: do you need to weight the SAWs in calculating the histogram?).

# with open('design_1_saws.txt') as f:
#     records = f.readlines()
# records = [x.strip().split() for x in records]
# n_steps = [int(record[1]) for record in records]
# weights = [float(record[2]) for record in records]
# f_handler = open("design_1_nsteps.pkl", "wb")
# pickle.dump(n_steps, f_handler)
# f_handler = open("design_1_weights.pkl", "wb")
# pickle.dump(weights, f_handler)
with open('design_1_nsteps.pkl', 'rb') as f:
    n_steps = pickle.load(f)
with open('design_1_weights.pkl', 'rb') as f:
    weights = pickle.load(f)

# with open('design_2_saws.txt') as f:
#     records = f.readlines()
# records = [x.strip().split() for x in records]
# n_steps2 = [int(record[1]) for record in records]
# weights2 = [float(record[2]) for record in records]
# f_handler = open("design_2_nsteps.pkl", "wb")
# pickle.dump(n_steps2, f_handler)
# f_handler = open("design_2_weights.pkl", "wb")
# pickle.dump(weights2, f_handler)
with open('design_2_nsteps.pkl', 'rb') as f:
    n_steps2 = pickle.load(f)
with open('design_2_weights.pkl', 'rb') as f:
    weights2 = pickle.load(f)

# with open('design_3_saws.txt') as f:
#     records = f.readlines()
# records = [x.strip().split() for x in records]
# n_steps3 = [int(record[1]) for record in records]
# weights3 = [float(record[2]) for record in records]
# f_handler = open("design_3_nsteps.pkl", "wb")
# pickle.dump(n_steps3, f_handler)
# f_handler = open("design_3_weights.pkl", "wb")
# pickle.dump(weights3, f_handler)
with open('design_3_nsteps.pkl', 'rb') as f:
    n_steps3 = pickle.load(f)
with open('design_3_weights.pkl', 'rb') as f:
    weights3 = pickle.load(f)

# with open('design_4_saws.txt') as f:
#     records = f.readlines()
# records = [x.strip().split() for x in records]
# weights4 = [float(record[1]) for record in records]
# with open('design_4_steps.txt') as f:
#     records = f.readlines()
# records = [x.strip() for x in records]
# n_steps4 = [int(record[1]) for record in records]
# f_handler = open("design_4_weights.pkl", "wb")
# pickle.dump(weights4, f_handler)
# f_handler = open("design_4_nsteps.pkl", "wb")
# pickle.dump(n_steps4, f_handler)
with open('design_4_nsteps.pkl', 'rb') as f:
    n_steps4 = pickle.load(f)
with open('design_4_weights.pkl', 'rb') as f:
    weights4 = pickle.load(f)

fig = plt.figure()
plt.hist(n_steps, bins=120, weights=weights, alpha=0.5, label='Design 1', color='green')
plt.hist(n_steps2, bins=120, weights=weights2, alpha=0.5, label='Design 2', color='blue')
plt.hist(n_steps3, bins=120, weights=weights3, alpha=0.5, label='Design 3', color='red')
plt.hist(n_steps4, bins=120, weights=weights4, alpha=0.5, label='Design 4', color='purple')
plt.grid()
plt.xlabel('SAW length')
plt.ylabel('Count')
plt.title('Distribution of SAW Lengths for 3 Designs')
plt.legend(['Design 1', 'Design 2', 'Design 3', 'Design 4'])
fig.savefig('2c_histogram.png', dpi=300)
plt.show()

# Also, visualize (print) the longest SAW found.
with open('design_1_longest_path.txt') as f:
    records = f.readlines()
records = [x.strip().split() for x in records]
path_hist = [[int(record[0]), int(record[1])] for record in records]
f_handler = open("design_1_longest_path.pkl", "wb")
pickle.dump(path_hist, f_handler)

with open('design_2_longest_path.txt') as f:
    records = f.readlines()
records = [x.strip().split() for x in records]
path_hist2 = [[int(record[0]), int(record[1])] for record in records]
f_handler = open("design_2_longest_path.pkl", "wb")
pickle.dump(path_hist2, f_handler)

with open('design_3_longest_path.txt') as f:
    records = f.readlines()
records = [x.strip().split() for x in records]
path_hist3 = [[int(record[0]), int(record[1])] for record in records]
f_handler = open("design_3_longest_path.pkl", "wb")
pickle.dump(path_hist3, f_handler)

with open('design_4_longest_path.txt') as f:
    records = f.readlines()
records = [x.strip().split() for x in records]
path_hist4 = [[int(record[0]), int(record[1])] for record in records]
f_handler = open("design_4_longest_path.pkl", "wb")
pickle.dump(path_hist4, f_handler)

fig = plt.figure()
x = [coordinate[0] for coordinate in path_hist]
y = [coordinate[1] for coordinate in path_hist]
plt.plot(x, y, color='green')
plt.xticks(x)
plt.grid()
plt.title('Design 1 - ' + str(len(x)) + ' Steps')
fig.savefig('2_path1.png', dpi=300)
plt.show()

fig = plt.figure()
x = [coordinate[0] for coordinate in path_hist2]
y = [coordinate[1] for coordinate in path_hist2]
plt.plot(x, y, color='blue')
plt.xticks(x)
plt.grid()
plt.title('Design 2 - ' + str(len(x)) + ' Steps')
fig.savefig('2_path2.png', dpi=300)
plt.show()

fig = plt.figure()
x = [coordinate[0] for coordinate in path_hist3]
y = [coordinate[1] for coordinate in path_hist3]
plt.plot(x, y, color='red')
plt.xticks(x)
plt.grid()
plt.title('Design 3 - ' + str(len(x)) + ' Steps')
fig.savefig('2_path3.png', dpi=300)
plt.show()

fig = plt.figure()
x = [coordinate[0] for coordinate in path_hist4]
y = [coordinate[1] for coordinate in path_hist4]
plt.plot(x, y, color='purple')
plt.xticks(x)
plt.grid()
plt.title('Design 4 - ' + str(len(x)) + ' Steps')
fig.savefig('2_path4.png', dpi=300)
plt.show()
