from network_drawer import NetworkDrawer


filename = 'links.csv'
N = 7      # Number of players per group
NG = 4     # Number of unique groups
NP = 2     # Total number of periods (including trials)
show_trials = False

NetworkDrawer(filename, N, NG, NP, show_trials).draw_in_image_files()
