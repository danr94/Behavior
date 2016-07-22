# Created by Dan on 07/21/2016, dumb test of different functions 

from Behavior import Behavioral_test
import glob
import os
import numpy as np
import matplotlib.pyplot as plt 



def main():
    dph = '/home/sillycat/Documents/Zebrafish/Behavioral/Data/Behavior_test6/'
    #Please modify the data path above #


    dset_list = glob.glob(dph+'D1*l.csv')
    TF_list = glob.glob(dph + 'TF*G*D1*l.npy')
    
    dset_list.sort(key = os.path.getmtime) # sort the files based on modification time 
    TF_list.sort(key = os.path.getmtime)
    c_list = zip(dset_list, TF_list) # zip is a cool function in python! 
#     nlist = [0, 1, 2, 3]
    for ds_name, tf_name in c_list:
        dset = np.genfromtxt(ds_name,delimiter = ',', skip_header =1)
        dset[:,0]-=dset[0,0]
        dset[:,0]/=29.98
        tflag = np.load(tf_name)
        tflag-=tflag[0]
        tflag/=1000.
        fig_name = dph+ 'plot_'+os.path.basename(tf_name)[3:-4]
        print(ds_name)
        print(tf_name)
#         print(fig_name)

        BT = Behavioral_test(dset,tflag)
        BT.session_split()
        phase_stat = BT.phase_average()
        fig_1 = BT.phase_barplot([1,2,4], phase_name=['LED', 'LED+para', 'off'], n_col = 0)
        fig_1.savefig(fig_name+'_pos')
        fig_2 = BT.phase_barplot([1,2,4], phase_name=['LED', 'LED+para', 'off'], n_col = 1)
        fig_2.savefig(fig_name+'_neg')
        
        plt.clf()  
        
        fig_0, ax_0 = plt.subplots(figsize = (8,4))
        ax_0.errorbar(np.arange(BT.n_trial)*3, phase_stat[:, 0], yerr = phase_stat[:,1], color = 'g', linewidth=2)
        ax_0.errorbar(np.arange(BT.n_trial)*3+1, phase_stat[:,2], yerr = phase_stat[:,3], color = 'b', linewidth=2)
        ax_0.set_xticks(np.arange(BT.n_trial, step=3)*3+1.5)
        ax_0.set_xticklabels(np.arange(BT.n_trial, step=3)+1)
        ax_0.set_ylim([0,9])
        ax_0.legend(['+', '-'], fontsize = 12)
        
        fig_0.savefig(fig_name+'_all')
        
        plt.clf()
        
        
        fig_0, ax_0 = plt.subplots(figsize = (8,4))
        ax_0.plot(BT.data[:,1], color = 'g', linewidth=2)
        ax_0.plot(BT.data[:,2], color = 'b', linewidth=2)
#         ax_0.set_xticks(np.arange(BT.n_trial, step=3)*3+1.5)
#         ax_0.set_xticklabels(np.arange(BT.n_trial, step=3)+1)
        ax_0.set_ylim([0,8])
        ax_0.legend(['+', '-'], fontsize = 12)
        
        fig_0.savefig(fig_name+'_raw')

        
        #         latency = BT.session_latency(1)
#         BT.latency_plot(fig_name, latency)         



if __name__ == '__main__':
    main()
