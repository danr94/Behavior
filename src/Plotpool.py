import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.pyplot.Figure as Figure




def Fig_grooming(font_size = 16):
    font = {'family':'normal',
        'size': font_size
        }
    mpl.rc('font', **font)
    mngr = plt.get_current_fig_manager()
    mngr.window.move()
