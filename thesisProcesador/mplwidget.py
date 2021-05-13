# ------------------------------------------------------------
# -------------------- dinamicGraphics.py --------------------
# ------------------------------------------------------------

from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())  # Le da las propiedades de ser un grafico para plotear  ..
        
        vertical_layout = QVBoxLayout()        # Define donde va a ir la grafica 
        vertical_layout.addWidget(self.canvas)  # Inserta la gráfica dentro del recuadro 
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)    # Le agrega un Ploteo !
        self.canvas.axes.figure.subplots_adjust(left=0.085, bottom=0.150, right=0.995, top=0.950, wspace=0.2, hspace=0.2)
        #matplotlib.pyplot.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
        self.setLayout(vertical_layout)
        self.canvas.axes.grid(True)  
        # grid()