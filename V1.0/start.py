import sys
import os
sys.path.append(os.path.abspath(os.getcwd()))

from Core.CoreModule import *
from GUI.GUI import GUI

if __name__ == '__main__':

    core = Core()
    gui = GUI(core.getParamObj(),core)
    core.run()
    core.shutdown()