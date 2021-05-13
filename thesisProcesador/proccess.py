# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#
#  Title: Procesador de señales de un radar FMCW SAR.
#  Code :  main.py  
#  Author: Sequeira Andres
#  gitHub: https://github.com/sequeirandres/
#  Repositorio: https://github.com/sequeirandres/thesisProcesador
#
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon 
import matplotlib.pyplot as plt                 
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from scipy import signal
from scipy.io import wavfile
import numpy as np
import sys
import os ,shutil

#  --- own codes ---
from parameters import*
from RecordApp import AppRecord  
from plataforma import Plataform 
from radarFmcwClass import*
from functions import*
from radarSar import radarFmcwSar


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rcsmain = radarFmcwSar()
    rcsmain.show()
    app.exec_()