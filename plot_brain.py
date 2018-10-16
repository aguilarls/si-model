import matplotlib.pyplot as plt
import numpy as np
from nilearn import plotting

import pandas as pd
df = pd.read_csv('/Users/pablodamasceno/Desktop/Raj_networks/coordinates.csv')

color = df['group'].values[:90]

coords = [(df['X'][i],df['Y'][i],df['Z'][i]) for i in range(90)]
connec = np.array([[0]*90]*90)
# sizes  = np.array([100]*90)
sizes  = all_H[1]/5

sizes
filtered_sizes = [sizes[i] if sizes[i] > 350 else 50 for i in range(len(sizes))]
# filtered_sizes

plotting.plot_connectome(connec, coords,node_size=filtered_sizes,node_color=color,
                         display_mode='lyrz')





#
