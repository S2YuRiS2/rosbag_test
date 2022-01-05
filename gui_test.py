import sys
from PyQt5.QtWidgets import *
from rosbag import rosbag_main
from multiprocessing import Process
import time
import os
import signal
import rospy

class MyApp(QMainWindow):
    # write=[]
    def __init__(self):
        super().__init__()
        self.initUI()
        self.write = Process(target=rosbag_main.record_cmd, args=[['-a']])
        self.play = Process(target=rosbag_main.play_cmd,args=[['--pause']])

        os.system('cd{}'.format(os.getcwd()))
        output=os.popen('%d').read()
        print(output)




    def initUI(self):
        bagrecord_button=QAction('Bag_Record',self)
        bagrecord_button.setShortcut('Ctrl+R')
        bagrecord_button.triggered.connect(self.recorder)
        bagsave_button=QAction('Bag_Save',self)
        bagsave_button.setShortcut('Ctrl+S')
        bagsave_button.triggered.connect(self.recoder_save)
        # bagplay
        bagquit_button=QAction('Bag_Quite',self)
        bagquit_button.setShortcut('Ctrl+Q')
        bagquit_button.triggered.connect(self.recorder_quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        bagmenu1 = menubar.addMenu('&Record')
        bagmenu2 = menubar.addMenu('&Save')
        bagmenu3 = menubar.addMenu('&Quite')
        bagmenu1.addAction(bagrecord_button)
        bagmenu2.addAction(bagsave_button)
        bagmenu3.addAction(bagquit_button)

        self.setWindowTitle("ROSBag Test")
        self.setGeometry(1500,400,500,400)
        self.show()


    def recorder(self):
        self.write.start()
        # self.write.join()
        print(self.write)
        print('rosbag_recorder')

    def recoder_save(self):
        self.write.terminate()
        # self.write.close()
        print('rosbag_save')

    def bag_play(self):
        self.play.start()

    def recorder_quit(self):
        print('quit..')
        qApp.quit()


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MyApp()
    sys.exit(app.exec_())