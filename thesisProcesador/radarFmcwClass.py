# this is all class from radar fmcw

from credentials import*

# -----------------------  class  -------------------------------------

class Transmisor():
    def __init__(self, fo , Bw):
        self.fo  = fo 
        self.Bw = Bw

class Receptor():
    def __init__(self,snr):
        self.snr = snr

class Process():
    def __init__(self,fs,nfft):   
        self.fs = fs 
        self.nfft  = nfft 

class Medium():
    def __init__(self,vprop ):
        self.vprop = vprop

class Riel():
    def __init__(self,stepAcimut):
        self.stepAcimut = stepAcimut

class Target():
    def __init__(self) :
        self.object = 1

class Radition():
    def __init__(self):
        self.patron = 1

class Result():
    def __init__(self):
        self.result =   1 


# ---------------------- class plataform -----------------------------
class PlataformSar():
    def __init__(self):
        self.speed = 30     # % of speed
        self.distance = 500 # distance in cm
        self.credencial_SSID = SSID_ACCESSPOINT
        self.credencial_pass = SSID_PASS

# ------------------------ class radar -------------------------------

class Radar():
    def __init__(self):
        self.transmisor = Transmisor(F0,BW)
        self.receptor = Receptor(SNR)
        self.medium = Medium(VPROP)
        self.riel = Riel(STEP_ACIMUT)


