from utils import plotting
import matplotlib.pyplot as plt


plotting.make_plot('aronsson_star',legend_loc='lower left')
plotting.make_plot('aronsson_star_dilateBC',legend_loc='upper right')
plotting.make_plot('aronsson_square',legend_loc='upper right')
#plotting.make_plot('aronsson_square_singular',legend_loc='upper right')


plt.show()
