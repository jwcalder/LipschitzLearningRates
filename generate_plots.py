from utils import plotting
import matplotlib.pyplot as plt

#Star plots
plotting.make_plot('aronsson_star',legend_loc='lower left')
plotting.make_plot('aronsson_star_singular',legend_loc='lower left')
plotting.make_plot('aronsson_star_dilateBC',legend_loc='upper right')

#Square plot
plotting.make_plot('aronsson_square',legend_loc='upper right')

plt.show()
