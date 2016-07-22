# Always import whatever libraries you need before writing functions and r
# Last update: 07/21/16


import time
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

ccode = ['g', 'b', 'y', 'm', 'c', 'r']

class Behavioral_test(object):
    def __init__(self, dset, tflag):
        # time offset corrected. 
        # self.data can have multiple columns, but tflag is only one column.
        
        self.data = dset 
        self.tflag = tflag - tflag[0] 
        self.ds_total = None
        self.trial_phase = {} 
       
        
    def session_split(self, trial_name = None):
        # assume data is already corrected by the time offset. The result is saved in trial_phase  
        # take out the first column of behavior data. Assume that the tflag and tbehave are sharing unit
        t_behave = self.data[:,0] #
        t_idx = np.searchsorted(t_behave, self.tflag)
        nsta = 0 
        
        for idx in np.arange(1, len(t_idx)):
            nend = t_idx[idx]
            self.trial_phase[idx-1] = self.data[nsta:nend, :]
            nsta = nend 
            
        # updated self.trial_phase 
        
    
    def session_merge(self, tflag):
        # merge the counting data with the time flags. The time offset is corrected.
        # 
        
        NL = len(tflag)
        tflag = np.column_stack((tflag, np.zeros(NL)))
        ds_total = np.concatenate((self.data, tflag), axis  = 0)
        self.ds_total = ds_total[ds_total[:,0].argsort()] # self.ds_total
        self.flag = np.where(self.ds_total[:,1] == 0)[0]  # mark the flag position
        return self.ds_total
    
    
    def session_latency(self, ev = 1, offset = 1):
        
        NL = len(self.flag)-1 - offset
        latency = np.zeros([NL, 3])
        for ii in np.arange(NL): 
            nsta = self.flag[ii+offset]
            nend = self.flag[ii+1+offset]
            data_section = self.ds_total[nsta:nend]
            t0 = data_section[0,0] # the time offset of the trial
            event_mark = np.where(data_section[:,1] == ev)[0]
            if len(event_mark) == 0:
                print("This session does not have the required event.")
            else:
                latency[ii,0]=data_section[event_mark[0], 0] - t0
                latency[ii,1]=data_section[event_mark, 0].mean() - t0
                latency[ii,2]=data_section[event_mark, 0].std()
                
        return latency
    
    def latency_plot(self, fname, data, nphase = 4):
        fig_init = plt.figure()
        fig_mean = plt.figure()
        ax_init = fig_init.add_subplot(111)
        ax_mean = fig_mean.add_subplot(111)
        NR = data.shape[0]
        
        session_ind = np.arange(0, NR, nphase)
        ind = np.arange(len(session_ind))*(nphase+1)
        
        width = 1.0
        for iphase in np.arange(nphase):
            ax_init.bar(ind+iphase*width, data[session_ind + iphase, 0], color = ccode[iphase])
            ax_mean.bar(ind+iphase*width, data[session_ind + iphase, 1], color = ccode[iphase], yerr = data[session_ind + iphase, 2])
             
            ax_init.set_xticks(ind + 2.0*width)
            ax_mean.set_xticks(ind + 2.0*width)
#             ax.set_xticklabels(keylist, rotation = 0)
        path, ti=os.path.split(fname)
        
        fname_init = ti+'_init'
        fname_mean = ti+'_mean'     
        
        fig_init.savefig(path+'/'+fname_init)
        fig_mean.savefig(path+'/'+fname_mean)
        
        # calculate the latency of the sessions
        
    def interval_counting(self, intv = 5):
        # intv: the time base of counting 
        # output: the average plus/minus 
        
    
    
def session_split(dset, tflag, NI, n_offset = 1):
    # dset: dataset 
    # tflag: time flag
    # NI: Initially, how many larvae are on the positive side? 
    
    NL = len(tflag)-n_offset
    

    tflag = np.column_stack((tflag[n_offset:], np.zeros(NL)))
    dset[0,1] = NI
    ds_total = np.concatenate((dset, tflag), axis  = 0)
    ds_total = ds_total[ds_total[:,0].argsort()]
    flags = np.where(ds_total[:,1] == 0)[0] # the position of flags
    ds_total[:,1] = ds_total[:,1].cumsum()
    

    t0 = ds_total[0,0]
    ds_total[:,0] -= t0
    
    NSec = len(flags)
    print(NSec)
    gcount = np.zeros([NSec-n_offset, 2])


    for ii in np.arange(NSec-n_offset):
        nsta = flags[ii] # Find where the session begins
        nend = flags[ii+1] # Find where the session ends
        
        dsection = ds_total[nsta:nend+1] # Take out the session from the dataset
        tdiff = np.diff(dsection[:,0]) # Calculate how long does each state (between two events) last
        gcount[ii,0] = np.inner(tdiff, dsection[:-1, 1]) # Inner product!
        gcount[ii,1] = ds_total[nend,0]-ds_total[nsta,0] # calculate how long does each session last (in miliseconds)
        
    gcount[:,0]/=gcount[:,1]   
        
    return gcount
    
    




def plot_sessions(gcount, pname, keylist):
    LG = len(gcount)
    session_ind = np.arange(0, LG, 4)
    
    g_LED = gcount[session_ind, 0]
    g_FEED = gcount[session_ind+1, 0]
    g_POST = gcount[session_ind+2, 0]
    g_REST = gcount[session_ind+3, 0]
    
    ind = np.arange(len(g_LED))*5
    fig = plt.figure()
    ax = fig.add_subplot(111)
    width = 1.0
    recs1 = ax.bar(ind, g_LED, width, color = 'g')
    recs2 = ax.bar(ind+width, g_FEED, color = 'y')
    recs3 = ax.bar(ind+2*width, g_POST, color = 'b')
    recs4 = ax.bar(ind+3*width, g_REST, color = 'm')
    
    ax.set_xticks(ind + 2.0*width)
    ax.set_xticklabels(keylist, rotation = 0)
    
    ptitle=os.path.split(pname)[1]
    ax.set_title(ptitle)
    ax.set_ylim([0,14])
#     ax.legend((recs1[0], recs2[0], recs3[0]), ('LED', 'LED+para', 'Rest'))
    ax.legend((recs1[0], recs2[0], recs3[0], recs4[0]), ('LED', 'LED+para', 'Post-feeding', 'Rest'))
    plt.savefig(pname) # save the figure 



    

def session_ttest(gcount, nlist, nsess = 4 ):
    # n1: the session label
    # n2: the session label 
    # return: two matrices of t-values and p-values
    nl = len(nlist) # The length of sessions that 
    t_val = np.zeros([nl,nl])
    p_val = np.identity(nl)
    
    for ii in np.arange(nl):
        ni = nlist[ii]
        X1 = gcount[ni::nsess, 0]
        for jj in np.arange(ii):
            nj = nlist[jj]
            
            X2 = gcount[nj::nsess, 0]
            
            t_val[ii,jj], p_val[ii,jj] = stats.ttest_ind(X1, X2)
            t_val[jj,ii] = t_val[ii,jj]
            p_val[jj,ii] = p_val[ii,jj]
 
    return t_val, p_val


# def timing_stat():




def main():
    dph = '/home/sillycat/Documents/Zebrafish/Behavioral/Data/Behavior_test4/'
    #Please modify the data path above #

    dset_list = glob.glob(dph+'Jul*G*D*.npy')
    TF_list = glob.glob(dph + 'TF*G*D*.npy')
    
    dset_list.sort(key = os.path.getmtime) # sort the files based on modification time 
    TF_list.sort(key = os.path.getmtime)
    c_list = zip(dset_list, TF_list) # zip is a cool function in python! 
#     nlist = [0, 1, 2, 3]
    for ds_name, tf_name in c_list:
        dset = np.load(ds_name)
        tflag = np.load(tf_name)
        fig_name = dph+ 'plot_'+os.path.basename(tf_name)[3:-4]
#         print(fig_name)
#         gcount = session_split(dset, tflag, 3)

        BT = Behavioral_test(dset,tflag, 3)
        latency = BT.session_latency(1)
        BT.latency_plot(fig_name, latency)         

#         
if __name__ == '__main__':
    main()

# We will define more functions soon for other purposes, and all of these functions will make a python module! 