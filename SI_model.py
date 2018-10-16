#################
#  Simulate simple disease propagation using a SI model in real brain networks
#  Connectivity matrices from https://doi.org/10.1371/journal.pone.0014832
#  Pablo F. Damasceno Aug 2019
#
################

from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt

def get_connectivity_matrices(filePath):
    '''
    Load a .mat file with connectivity matrices
    '''
    from pathlib import Path
    my_file = Path(filePath)
    if my_file.is_file():
        healthy_14 = loadmat(my_file)['S']
        conn_matrices = np.transpose(healthy_14)
        return(conn_matrices)
    else:
        raise(FileNotFoundError('Path to file is correct??'))

class Brain():
    '''
    Parent class for the connectivities of one patient's brain, composed of:
        conn_matrix (arr)    : connectivity matrix
        infected_indices (set) : indices of infected nodes
        num_nodes (int)      : number of nodes
        nodes (Nodes)        : nodes present in the network
        snapshot (arr)       : array of 0/1 on whether nodes are infected
    '''
    def __init__(self, conn_matrix):
        self.conn_matrix        = conn_matrix
        self.infected_indices   = set()
        self.num_nodes          = len(conn_matrix)                              # num regions in Atlas (here = nodes)
        self.nodes              = [Node(conn_matrix[n]) for n in range(self.num_nodes)]
        self.snapshot           = []                                            # array of infected nodes (as a function of time)

        # index nodes
        for n in range(self.num_nodes):
            self.nodes[n].index = n

    def choose_infected_node(self):
        '''
        output: index of a randomly selected infected node in the brain
        '''
        if len(self.infected_indices) == 0: #sanity check for list size
            raise ValueError("List of infected nodes is empty.")
        else:
            random_infected_index   = np.random.choice(list(self.infected_indices))
            return(random_infected_index)

    def infect_node(self, node_index):
        '''
        modify status of a node to 'infected'
        '''
        node                    = self.nodes[node_index]
        node.is_infected        = True
        self.infected_indices.add(node_index)

    def update_neighbors_of_infected_node(self, infected_node_index):
        '''
        remove infected_node_index from susceptb_neighbors set for all neighbors of infected_node
        add infected_node_index to infected_neighbors set for all neighbors of infected_node
        '''
        node = self.nodes[infected_node_index]
        for n in node.neighbor_indices:
            neigh_node = self.nodes[n]
            neigh_node.susceptb_neighbors.remove(infected_node_index)
            neigh_node.infected_neighbors.add(infected_node_index)

    def create_snapshot(self, append_snapshot = True):
        '''
        input: bool(append_snapshot) : if true, output is appended to 'snapshot' variable
        output: array of bools (snapshot) counting whether or not each node is infected
        '''
        brain_snapshot = [int(node.is_infected) for node in self.nodes]
        if append_snapshot == True:
             self.snapshot.append(brain_snapshot)
        else:
            return(brain_snapshot)

    def infect_brain(self):
        '''
        begin infection: choose random node and infect it
        while brain can still be infected:
            1. choose random infected node (as long it has susceptible neighbors) <- slow
            2. choose one random susceptible neighbor and infect it
            3. update_neighbors_of_infected_node
            4. create_snapshot
        '''
        atlas_size = self.num_nodes
        self.create_snapshot()

        first_infected_node_index = np.random.randint(atlas_size)
        first_infected_node       = self.nodes[first_infected_node_index]

        self.infect_node(first_infected_node_index)
        self.update_neighbors_of_infected_node(first_infected_node_index)
        self.create_snapshot()

        infected_node = first_infected_node
        while len(self.infected_indices) < atlas_size:      # brain can still be infected
            infected_node_index = self.choose_infected_node()
            infected_node       = self.nodes[infected_node_index]

            while infected_node.susceptb_neighbors == set(): # there are no susceptible neighbors
                infected_node_index = self.choose_infected_node() # choose another infected node
                infected_node       = self.nodes[infected_node_index]

            neighbor_to_infect_index = infected_node.pick_suscept_neighbor_index()
            # print("infected node is ", infected_node.index, " neighbor to infect is ", neighbor_to_infect_index)
            self.infect_node(neighbor_to_infect_index)
            self.update_neighbors_of_infected_node(neighbor_to_infect_index)
            self.create_snapshot()

    def print_configuration(self, snapshot_index):
        '''
        '''
        plt.xticks(np.arange(0, self.num_nodes, step=1))
        plt.ylim(0,1)
        plt.imshow(self.snapshot[snapshot_index], interpolation='nearest')
        plt.show()

class Node:
    '''
    Class for a given node in one brain network. Objects composed of:
        index (int)             : atlas number for this region / node
        is_infected (bool)      :
        neighbor_indices (set)  : indices of all neighboring nodes
        neighbor_probabs (arr)  : normalized vector of connectivity weights
        neighbor_weights (arr)  : vector of connectivity weights
        susceptb_neighbors (set):
        infected_neighbors (set):
    '''
    def __init__(self, connect_vector):
        self.index                  = None
        self.is_infected            = False
        self.neighbor_indices       = {i for i in np.nonzero(connect_vector)[0]}
        self.neighbor_probabs       = connect_vector / np.sum(connect_vector)
        self.neighbor_weights       = connect_vector
        self.susceptb_neighbors     = self.neighbor_indices.copy() #need shallow copy, not a reference!
        self.infected_neighbors     = set()

    def pick_suscept_neighbor_index(self):
        if len(self.susceptb_neighbors) == 0:
            raise ValueError("List of susceptible nodes is empty.")
        else:
            random_suscept_neighbor_index = np.random.choice(list(self.susceptb_neighbors))
            return(random_suscept_neighbor_index)
