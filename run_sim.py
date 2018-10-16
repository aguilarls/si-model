'''
Run simulations
'''

filePath = '/Users/pablodamasceno/Desktop/Raj_networks/SI_model/connectivity_matrices.mat'
conn_matrices = get_connectivity_matrices(filePath)

def run_simulation(brain_index, simulations = 1):
    all_simulation_snaps = []
    for simulation in range(simulations):
        new_brain = Brain(conn_matrices[brain_index])
        new_brain.infect_brain()
        all_simulation_snaps.append(new_brain.snapshot)
    return(all_simulation_snaps)

n_steps = 10000
all_simulation_snaps = run_simulation(1, n_steps)
all_simulation_snaps_arr = np.array(all_simulation_snaps)

all_H = []
for i in range(1,91,10):
    step = [all_simulation_snaps_arr[j][i] for j in range(n_steps)]
    step = np.array(step)
    all_H.append(np.sum(np.transpose(step), axis=1))


plt.plot(np.transpose(all_H))

def get_color_array():
    color = np.array([ 1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,
            3,  4,  4,  5,  5,  6,  6,  6,  6,  7,  7,  8,  8,  9,  9,  9,  9,
            9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 16,
           16, 16, 16, 17, 17, 18, 18, 19, 19, 19, 19, 20, 20, 21, 21, 22, 22,
           23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 29, 29, 29,
           29, 29, 29, 29, 29])


    new_color = [list(np.squeeze(np.random.rand(3,1)))]
    for i in range(1,90):
        if color[i] == color[i-1]:
            # print('yes')
            new_color.append(new_color[-1])
        else:
            # print('no')
            new_RGB = list(np.squeeze(np.random.rand(3,1)))
            new_color.append(new_RGB)
    return(new_color)

color = get_color_array()


for i in range(1,91,10):
    step = [all_simulation_snaps_arr[j][i] for j in range(n_steps)]
    step = np.array(step)
    histogram = np.sum(np.transpose(step), axis=1)
    plt.bar(np.arange(len(histogram)), histogram, color=color)
    plt.pause(0.05)
