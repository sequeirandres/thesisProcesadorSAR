
# ---- class radarSar.py --------

class radarFmcwSar(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        print('loading')
        loadUi("SarGuiApp.ui",self)    # Cargas las configuraciones del diseño ! todos los atributos !
        #self.setStyleSheet("background-color: grey")
        #loadUi("SarGuiApp.ui",self)    # Cargas las configuraciones del diseño ! todos los atributos !
        # Imagenes 
        #self.ImgPencilColor =  mpimg.imread('imag/pencilColor.png')
        #self.ImgPencil =  mpimg.imread('imag/pencil2.png')
        #self.ImgObject = mpimg.imread('imag/objetos.png')
        #self.Max_col_pencil =  len(self.ImgPencil[1,:,1])  # Columnas for Pencil
        #self.Max_fil_pencil =  len(self.ImgPencil[:,1,1])  # Columnas for Pencil
        #self.Max_col_Object =  len(self.ImgObject[1,:,1])  # Columnas for Pencil
        #self.Max_fil_Object =  len(self.ImgObject[:,1,1])  # Columnas for Pencil
        #self.index = 0 
        #self.listIndex = np.arange(0,self.Max_col_Object-self.Max_col_pencil , 50 )
        #self.initQtplot()   
        self.InitMenu()  
        #self.loadParameters()
        #self.setParameters()
        self.setWindowTitle("Procesador SAR")
        self.setWindowIcon(QIcon('Icono_python.ico')) 
        self.Button_Exit.setIcon(QIcon('icono_exit.ico'))
        self.Button_Exit.clicked.connect(self.AppSarProccessExit)
        self.Button_OpenFile.clicked.connect(self.OpenDirectory)
        self.Button_OpenFile.setIcon(QIcon('icon_openWaveFile2.ico')) 
        self.Button_ProcessRMA.clicked.connect(self.AppRunRMA)
        self.Button_Detection.setIcon(QIcon('tensorflow.ico') )
        self.Button_ProcessRMA.setIcon(QIcon('icono_play.ico')) 
        self.Button_RecordFiles.clicked.connect(self.AppSarRecordFile)
        self.Button_RecordFiles.setIcon(QIcon('icono_record.ico'))
        self.Button_Detection.clicked.connect(self.AppDetection)
        #self.radio_plot_module.clicked.connect( self.radarPlotModule )
        #self.radio_plot_phase.clicked.connect( self.radarPlotPhase )
        #self.addToolBar(NavigationToolbar(self.PlotWidgetImage.canvas, self))
        #self.addToolBar(NavigationToolbar(self.PlotWidgetImageSar.canvas, self))
        #self.label_target.setText('0.0 [m]')
        #self.horizontalScrollBar.valueChanged['int'].connect(self.moveTarget)   # Muevo la barra de distancia
        #self.PlotWidgetTX.canvas.plot.subplots_adjust(left=0.05, bottom=0.150, right=0.995, top=0.9, wspace=0.2, hspace=0.2)
        #self.windowsToolConfig = windowConfigurations()
        self.progressBar.setValue(0)
        self.fileToProccess = 'none'
        self.remuveAcople.clicked.connect(self.AcopleRemuve)
        print('Runing Radar SAR')
    
    def AcopleRemuve(self):
        if self.remuveAcople.isChecked():
            print('Antena sin acople ')
            self.remuveAcople.setText('sin acople')
        else :
            print('Antena con acople')
            self.remuveAcople.setText('con acople')

    def InitMenu(self):
        print('Init Menu')
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        #editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        #searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        
        # ----- Atributos para Menu de menu ----
        fileMenu_Option_Record = QAction('Record Data', self)
        fileMenu_Option_Open = QAction('Open Folder',self)
        fileMenu_Option_Run = QAction('Run',self)
        fileMenu_Option_Detect = QAction('Detect',self)
        fileMenu_Option_Exit = QAction('Exit',self)

        fileMenu.addAction(fileMenu_Option_Record)
        fileMenu.addAction(fileMenu_Option_Open)
        fileMenu.addAction(fileMenu_Option_Run)
        fileMenu.addAction(fileMenu_Option_Detect)
        fileMenu.addAction(fileMenu_Option_Exit)
       
        fileMenu_Option_Record.triggered.connect(self.AppSarRecordFile)    # Cerrar la aplicacion
        fileMenu_Option_Open.triggered.connect(self.OpenDirectory)
        fileMenu_Option_Run.triggered.connect(self.AppRunRMA)
        fileMenu_Option_Exit.triggered.connect(self.AppSarProccessExit)

        # ---- Atributos para Menu de View ----
        viewMenu_Option_Imag_mod = QAction('Plot Sar Module',self)
        viewMenu_Option_Imag_phase = QAction('Plot Sar Phase',self)
        viewMenu_Option_plot_data = QAction('Plot file .wav',self)
        viewMenu_Option_plot_data_fft = QAction('Plot fft file .wav', self)

        viewMenu.addAction(viewMenu_Option_Imag_mod)
        viewMenu.addAction(viewMenu_Option_Imag_phase)
        viewMenu.addAction(viewMenu_Option_plot_data)
        viewMenu.addAction(viewMenu_Option_plot_data_fft)

        viewMenu_Option_plot_data.triggered.connect(self.plotFileData)
        viewMenu_Option_plot_data_fft.triggered.connect(self.plotFFtFileData)
        viewMenu_Option_Imag_mod.triggered.connect(self.plotSarModule)
        viewMenu_Option_Imag_phase.triggered.connect(self.plotSarPhase)

        # --- Atributos para Menu de Tools ---
        toolsMenu_Option_plataform = QAction('Plataform', self)
        toolsMenu.addAction(toolsMenu_Option_plataform)
        toolsMenu_Option_plataform.triggered.connect(self.runPlataform)

    def OpenDirectory(self):
        #directoryPath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', ' ', QtWidgets.QFileDialog.ShowDirsOnly)
        pathFileName  = QtWidgets.QFileDialog.getOpenFileName(None,  " Data file name", '.', "*.wav")
        if (pathFileName) :
            #print('you file name is :' , pathFileName[0])
            self.fileToProccess =  pathFileName[0]
            print('your file .wav to proccess : ',self.fileToProccess )
            self.label_NameDirectory.setText(self.fileToProccess)
        else :
            print('No file selected')
            self.label_NameDirectory.setText('No file selected')
            self.fileToProccess = 'none'

# ---------------------  load signal and process RMA algorithm ---------------------
    def AppRunRMA(self):
        self.progressBar.setValue(0)
        print('running RMA algorithm ... ')
        if self.fileToProccess == 'none':
            print('no file to process')
        else :
            # 1er - load signals and sync :
            signal, sync = loadSignal(self.fileToProccess,CHANNEL_SIGNAL,CHANNEL_SYNC)
            # 2do - cut signal in N-signals with sync
            nsignals = cutsAllSignals(signal, sync)
            print('cuts all signals')
            #3ro - remuve the clutters and crosstalks 
            if self.remuveAcople.isChecked():
                nsignals = clutterRemuve(nsignals)
                print('Remuve Acople')
            else:
                print('No Remuve Acople')
            #4to - get FFT module and phase 
            fftModule, fftPhase = spectroSignal(nsignals,NFFT)
            # 5to make graphics
            #fftModuledB = converter_to_dB(fftModule)
            print('Imagen SAR ... done')
            self.imagSarModule = fftModule
        
            # ajustar acimut
            self.acimut = np.arange(0,5,5/len(self.imagSarModule))

            # ajustar range
            self.range =  np.arange(0,10,10/len(self.imagSarModule[0]))
    
            #self.imagSarPhase =  fftPhase
            # plot module image sar :
            self.AppSarGraphicsModule()
            # plot phase imagen sar :
            #self.AppSarGraphicsPhase()
            self.Zphase = np.transpose(fftPhase)
            self.progressBar.setValue(100)
    
# ---------------------------- graphics -----------------------------
    def AppSarGraphicsModule(self):
        #self.distance = self.freq*FREQ_TO_DISTANCE
        #self.COL , self.FIL = np.meshgrid( np.arange(0,len(self.imagSarModule),1) ,self.distance)
        self.Zmodule = np.transpose(self.imagSarModule)
        self.ZmoduledB = converter_to_dB(self.Zmodule)
        self.PlotWidgetModule.canvas.axes.clear()
        #self.PlotWidgetModule.canvas.axes.contourf( self.COL, self.FIL, self.Zmodule  ,cmap= plt.cm.nipy_spectral)
        self.PlotWidgetModule.canvas.axes.contourf( self.acimut,self.range,self.Zmodule  ,cmap= plt.cm.jet)
        self.PlotWidgetModule.canvas.axes.set_ylim(0,4)
        self.PlotWidgetModule.canvas.draw()

    def AppSarGraphicsPhase(self):
        #self.COL , self.FIL = np.meshgrid( np.arange(0,len(self.imagSarPhase),1) ,self.distance)
        self.Zphase = np.transpose(self.imagSarPhase)
        self.PlotWidgetPhase.canvas.axes.clear()
        #self.PlotWidgetPhase.canvas.axes.contourf( self.COL, self.FIL, self.Zphase  ,cmap= plt.cm.nipy_spectral)
        self.PlotWidgetPhase.canvas.axes.contourf( self.Zphase  ,cmap= plt.cm.jet)
        self.PlotWidgetPhase.canvas.axes.set_ylim(0,200)
        self.PlotWidgetPhase.canvas.draw()

# ----------------- to exit -----------------
    def AppSarProccessExit(self):
        self.close()

# -------------- to record files wav ---------
    def AppSarRecordFile(self):
        print('APP TO RECORD FILES')
        self.recApp = AppRecord(self)  # Pointer to AppSarProccess
        self.recApp.show()

# -------- export module imagen sar -----
    def plotSarModule(self):
        #print('Imag Sar Module')
        FONTSIZE = 18
        plt.figure('Image SAR')
        #self.Zmodule = converter_to_dB(self.Zmodule)
        plt.contourf(self.acimut, self.range ,self.Zmodule  ,cmap= plt.cm.jet)
        plt.ylabel('Range [m]',fontsize=FONTSIZE)
        plt.xlabel('Acimut [m]',fontsize=FONTSIZE)
        plt.title('Imagen de Apertura Sintética',fontsize=FONTSIZE)
        plt.xticks(fontsize=FONTSIZE)
        plt.yticks(fontsize=FONTSIZE)
        plt.ylim(0,3)
        plt.colorbar()
        #plt.contourf( self.COL, self.FIL, self.Zmodule  ,cmap= plt.cm.nipy_spectral)
        plt.show()

# ------ export phase imagen sar ---------
    def plotSarPhase(self):
        print('Imag sar Phase')
        plt.figure('Imagen sar Phase')
        plt.contourf( self.ZmoduledB  ,labels=[-40,-20,-10,-6,-3,0],cmap= plt.cm.jet)
        plt.colorbar()
        plt.show()

# -------- plot imag varias -----------------
    def plotFileData(self):
        pathFileName  = QtWidgets.QFileDialog.getOpenFileName(None,  " Data File", '.', "*.wav")
        print('Data File :' , pathFileName[0])
        signal, sync = loadSignalOrigin (pathFileName[0],CHANNEL_SIGNAL,CHANNEL_SYNC)
        time, freq, samplerate  = loadParameter(pathFileName[0])
        
        plt.figure('signal')
        plt.plot(time,signal,'k', linewidth=1.5)
        plt.grid(True)
        plt.ylabel('Amplitud')
        plt.xlabel('Tiempo')

        plt.figure('File .wav')
        
        plt.subplot(311)
        plt.title('Signal y Sync ')
        plt.plot(time[9000:20000],signal[9000:20000],'k', linewidth=1.5)
        #plt.legend(['signal'])
        plt.ylabel('Amplitud')
        plt.ylim(-0.75,0.75)
        plt.xlim(0.2470,0.444)
        plt.grid(True)

        plt.subplot(312)
        plt.plot(time[9000:20000],sync[9000:20000],'k', linewidth=1.5)
        #plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        #plt.legend(['sync'])
        plt.ylim(-0.75,0.75)
        plt.xlim(0.2470,0.444)
        plt.grid(True)

        vco_ = 10*np.ones(5) 

        plt.subplot(313)
        plt.plot(vco_)
        plt.ylabel('Amplitud')
        plt.ylim(0,5)
        plt.xlim(0.2470,0.444)
        plt.grid(True)
        
        # ----------------------------------------------------------
        plt.figure('split signal')
        plt.subplot(161)
        N = 1050
        jj = 1 
        plt.plot(time[8050+N*(jj-1):8050+N*jj],signal[8050+N*(jj-1):8050+N*jj],'k', linewidth=1.5)
        #plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud')
        #plt.legend(['sync'])
        #plt.ylim(-0.75,0.75)
        #plt.xlim(0.2470,0.444)
        plt.grid(True)
        
        plt.subplot(162)
        jj = 2
        plt.plot(time[8050+N*(jj-1):8050+N*jj],signal[8050+N*(jj-1):8050+N*jj],'k', linewidth=1.5)
        #plt.xlabel('Tiempo [s]')
        #plt.ylabel('Amplitud')
        #plt.legend(['sync'])
        #plt.ylim(-0.75,0.75)
        #plt.xlim(0.2470,0.444)
        plt.grid(True)


        plt.subplot(163)
        jj=3
        plt.plot(time[8050+N*(jj-1):8050+N*jj],signal[8050+N*(jj-1):8050+N*jj],'k', linewidth=1.5)
        #plt.xlabel('Tiempo [s]')
        #plt.ylabel('Amplitud')
        #plt.legend(['sync'])
        #plt.ylim(-0.75,0.75)
        #plt.xlim(0.2470,0.444)
        plt.grid(True)


        plt.subplot(164)
        jj = 4
        plt.plot(time[8050+N*(jj-1):8050+N*jj],signal[8050+N*(jj-1):8050+N*jj],'k', linewidth=1.5)
        plt.grid(True)

        plt.subplot(165)
        jj = 5
        plt.plot(time[8050+N*(jj-1):8050+N*jj],signal[8050+N*(jj-1):8050+N*jj],'k', linewidth=1.5)
        plt.grid(True)

        plt.subplot(166)
        jj = 6
        plt.plot(time[8050+N*(jj-1):8050+N*jj],signal[8050+N*(jj-1):8050+N*jj],'k', linewidth=1.5)
        plt.grid(True)

        plt.show()

    def plotFFtFileData(self):
        pathFileName  = QtWidgets.QFileDialog.getOpenFileName(None,  " Data File", '.', "*.wav")
        print('Data File :' , pathFileName[0])
        signal, sync = loadSignalOrigin (pathFileName[0],CHANNEL_SIGNAL,CHANNEL_SYNC)
        time, freq, samplerate  = loadParameter(pathFileName[0])
        #Signalprocess = cutsAllSignals(signal, sync,MODE_PROCCESS)
        #fftsignalModule, fftsignalPhase = spectralSignal(Signalprocess ,samplerate)

        plt.figure('Matriz - raw data ')
        plt.subplot(411)
        plt.plot(time[9000:10000],signal[9000:10000],'b', linewidth=1.5)
        plt.grid(True)
        
        plt.subplot(412)
        plt.plot(time[10000:11000],signal[10000:11000],'b', linewidth=1.5)
        plt.grid(True)
        
        plt.subplot(413)
        plt.plot(time[11000:12000],signal[11000:12000],'b', linewidth=1.5)
        plt.grid(True)

        plt.subplot(414)
        plt.plot(time[12000:13000],signal[12000:13000],'b', linewidth=1.5)
        plt.grid(True)
        
        plt.show()


    def runPlataform(self):
        print('run control of plataform')
        self.pltfm = Plataform()
        self.pltfm.show()


    def AppDetection(self):
        print('detection of objects from Imagen SAR')
