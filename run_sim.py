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
