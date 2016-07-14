import time
import os.path
import sys
import serial
from arduino import Arduino
# from pump_control import PumpControl


from PyQt4 import QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# import Canvas
# import ilastik
# from Canvas import Qt4MplCanvas
cc_list = ['g', 'r', 'b', 'm', 'g', 'r', 'b', 'm', 'g', 'r', 'b', 'm', 'g', 'r', 'b']



class Behave_module(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Behave_module, self).__init__(parent)
        self.ard = Arduino('/dev/ttyACM0')
        self.initUI()
        self.Data_plus=np.array([0,0])
        self.Data_minus=np.array([0,0])
        self.count_plus = 0
        self.count_minus = 0
        self.start_time= 0
        self.sessions = -1 # number of sessions
        self.secnames = {} # dictionary:
        self.Dat_set = {} # The whole data set 
        
        
        

    def initUI(self):
#         layout = QtGui.QlayoutLayout()
#         layout.setSpacing(3)
        # Add button for '+'
        grid = QtGui.QGridLayout()
        grid.setSpacing(15)
        
        
        self.fsave='test.npy'
        self.figure1=plt.figure()
        self.figure2=plt.figure()
        self.lbl_file = QtGui.QLabel('File name:')
        self.qle_file = QtGui.QLineEdit(self)
        self.lbl_sess = QtGui.QLabel('Session name:')
        self.qle_sess = QtGui.QLineEdit(self)
        self.sessions = -1
        self.secnames = {} # empty secnames
        self.Dat_set = {} # empty buffer for data
        
        

        # set file names and session names

        self.fnamebtn =QtGui.QPushButton('Set data file name', self)
        self.fnamebtn.setCheckable(True)
        self.fnamebtn.clicked.connect(self.click_file)      
    
        self.adsbtn = QtGui.QPushButton('Add session', self)
        self.adsbtn.setCheckable(True)
        self.adsbtn.clicked.connect(self.add_session)
        
        # ----------------Add buttons for operations -------------------------
        
        # add button for 'New'
        self.newbtn = QtGui.QPushButton('New Experiment', self)
        self.newbtn.setCheckable(True)
        self.newbtn.clicked.connect(self.click_new)

        # Add button for 'Add session'
    
        # Add button for 'Complete'
        self.compbtn = QtGui.QPushButton('Complete', self)
        self.compbtn.setCheckable(True)
        self.compbtn.clicked.connect(self.click_complete)


        # Add button for 'Start '
        self.startbtn = QtGui.QPushButton('Start!', self)
        self.startbtn.setCheckable(True)
        self.startbtn.clicked.connect(self.click_start)      
        
        # Add button for '+'
        self.plusbtn = QtGui.QPushButton('+',self)
        self.plusbtn.setCheckable(True)
        self.plusbtn.clicked.connect(self.click_plus)      
        
        
        # Add button for '-' 
        self.minusbtn = QtGui.QPushButton('-',self)
        self.minusbtn.setCheckable(True)
        self.minusbtn.clicked.connect(self.click_minus)     

        # Add button for 'Stop'
        self.stopbtn = QtGui.QPushButton('Stop',self)
        self.stopbtn.setCheckable(True)
        self.stopbtn.clicked.connect(self.click_stop)     
        
        self.blinkbtn = QtGui.QPushButton('Blink!', self)
        self.blinkbtn.setCheckable(True)
        self.blinkbtn.clicked.connect(self.click_blink)
        
        
        # Add text frames and plot frames
        self.canvas_plus=FigureCanvas(self.figure1)
        self.canvas_minus=FigureCanvas(self.figure2)
        
        # design the layout 
        grid.addWidget(self.lbl_file, 1, 0)
        grid.addWidget(self.qle_file, 1, 1, 1, 3)
        grid.addWidget(self.fnamebtn, 1, 4)
        grid.addWidget(self.lbl_sess, 2, 0)
        grid.addWidget(self.qle_sess, 2, 1, 1, 3)
        
        ibuttons = 3
        grid.addWidget(self.newbtn, ibuttons, 0)
        grid.addWidget(self.adsbtn, ibuttons, 1)
        grid.addWidget(self.compbtn, ibuttons, 2)
        grid.addWidget(self.blinkbtn, ibuttons, 3)
        ibuttons = ibuttons + 1
        
        grid.addWidget(self.startbtn, ibuttons, 0)
        grid.addWidget(self.plusbtn, ibuttons, 1)
        grid.addWidget(self.minusbtn, ibuttons, 2)
        grid.addWidget(self.stopbtn, ibuttons, 3)
        
        
        grid.addWidget(self.canvas_plus, ibuttons + 1, 0, 3, 8)
        grid.addWidget(self.canvas_minus, ibuttons + 4, 0, 3, 8)
        self.mapper = QtCore.QSignalMapper(self)
        self.setLayout(grid)
#         self.setGeometry(300,300,480,390)
        self.setWindowTitle('Behavioral Module')
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint) # always on top
        
        self.show()
        
    def click_start(self):
        print("Started! :)")
        self.Data_plus=np.array([0,0])
        self.Data_minus=np.array([0,0])
        self.startbtn.setChecked(1)
        millis = int(round(time.time() * 1000))
        self.count_plus =0
        self.count_minus = 0 
        self.startbtn.setChecked(0)
        self.start_time=millis

    
    def click_plus(self):
        self.plusbtn.setChecked(1)
        millis = int(round(time.time() * 1000)) - self.start_time
        self.count_plus = self.count_plus +1
        self.Data_plus = np.vstack((self.Data_plus, [millis, 1]))
        self.plusbtn.setChecked(0)
        self.plot_update(self.canvas_plus, self.Data_plus)
        print('+', self.count_plus)
        
        
    def click_minus(self):
        self.minusbtn.setChecked(1)
        millis = int(round(time.time() * 1000)) - self.start_time
        self.count_minus = self.count_minus + 1
        self.Data_minus = np.vstack((self.Data_minus, [millis, 1]))
        self.minusbtn.setChecked(0)
        self.plot_update(self.canvas_minus, self.Data_minus)
        print('-', self.count_minus)

    def click_stop(self):
        self.stopbtn.setChecked(1)
        self.stopbtn.setChecked(0)
#        
        secs = (int(round(time.time() * 1000)) - self.start_time)/1000.
        print("Stopping time:", secs, "seconds")
        
        key_plus =self.secnames[self.sessions]+'_plus'
#         print(key_plus)
#         key_plus=self.secnames[self.sessions]+'_plus'
        key_minus= self.secnames[self.sessions] + '_minus'
        self.Dat_set[key_plus] = self.Data_plus
        self.Dat_set[key_minus] = self.Data_minus
        # save the npz file
        
    def save_data(self, dph):
        print(self.Dat_set.keys)
        np.savez(dph,**self.Dat_set)
        print("Data saved as:"+str(self.fsave))

# --------------- The block below identifies names of the experiment and its sessions -----------------        
        
    def click_file(self):
        # the EditLine value]
        self.fnamebtn.setChecked(1)
        self.fsave = self.qle_file.text()
        print(self.fsave)
        self.fnamebtn.setChecked(0)
    
    def click_new(self):
        self.newbtn.setChecked(1)
        self.Dat_set.clear()
        # reduce to the initial status
        self.secnames={}
        self.sessions = -1 
        print("New experiment initialized under file name:", str(self.fsave))
        self.newbtn.setChecked(0)
        # Initialize a session

    def click_blink(self, prd = 200):
        self.blinkbtn.setChecked(1)
        self.ard.setHigh(13)
        time.sleep(prd/1000.)
        
        self.blinkbtn.setChecked(0)
        
    
    def add_session(self):
        # add a session
        self.sessions = self.sessions + 1
        self.Data_plus=[]
        self.Data_minus=[]
        self.adsbtn.setChecked(1)
        self.secnames[self.sessions] = str(self.qle_sess.text())
        print(self.secnames[self.sessions])
        self.adsbtn.setChecked(0)
                
        
    
        
    def click_complete(self):
        # All the sessions in a whole experiment is completed
        Data_path='../Data/'+str(self.fsave)
        if(os.path.isfile(Data_path+'.npz') is False):
            self.save_data(Data_path)
        else:
            print("File already exists.")
            
        self.Dat_set.clear() # clear the buffer of the Dataset 
       
    def plot_update(self,Canv,Dat):
        fig=Canv.figure
        fig.clf()
        ax = fig.add_subplot(111)
#         ax.hold(False)
        ax.vlines(Dat[:,0]/1000., [0], Dat[:,1], colors = cc_list[self.sessions])
        ax.set_ylim([0,1.1])
        
        Canv.draw()
    
        
    def shutdown(self):
#         self.test_variable(0)
        # save the data for future use 
#         np.save(self.fsave, self.Data)

        self.ard.close()        
        print "Finished!"
    # The end of definition of behavioral module
        
def main():
    app=QtGui.QApplication(sys.argv)
    ex1 = Behave_module()
#     ex2 = PumpControl()
    ret = app.exec_()
    ex1.shutdown()
    
    sys.exit(ret)

if __name__ == '__main__':
    main()
