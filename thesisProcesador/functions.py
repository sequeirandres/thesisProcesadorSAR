# ---- all functions for radar fmcw sar ---

import  numpy as np
from scipy import signal
from scipy.io import wavfile
from parameters import*


def  loadParameter(pathfile):
    samplerate, data = wavfile.read(pathfile)
    times = np.arange(len(data))/float(samplerate)
    freq  = np.arange(0,samplerate/2-samplerate/NFFT,samplerate/NFFT )
    return  times, freq, samplerate 

def loadSignal(pathfile,CHANNEL_SIGNAL,CHANNEL_SYNC ):
    # Load data from pathFile
    samplerate, data = wavfile.read(pathfile)    
    # Señal y sicronismo normalizado  :
    signal = (data[:,CHANNEL_SIGNAL]/ np.amax(data[:,CHANNEL_SIGNAL]))
    sync_ = data[:,CHANNEL_SYNC]/np.amax(data[:,CHANNEL_SYNC])
    # Señal de sincronismo logico :
    sync = sync_ > NIVEL
    #sync = sync_
    return signal, sync

def loadSignalOrigin(pathfile,CHANNEL_SIGNAL,CHANNEL_SYNC ):
    # Load data from pathFile
    samplerate, data = wavfile.read(pathfile)    
    # Señal y sicronismo normalizado  :
    signal = (data[:,CHANNEL_SIGNAL]/ np.amax(data[:,CHANNEL_SIGNAL]))
    sync = data[:,CHANNEL_SYNC]/np.amax(data[:,CHANNEL_SYNC])
    # Señal de sincronismo logico :
    #sync = sync_ > NIVEL
    #sync = sync_
    return signal, sync

def InitIdex(sync):
    index = 0
    if(sync[0] == False) :
        while sync[index] != True : # saco todos los '0'
            index +=1 
    else:
        while sync[index] != False: # saco los '1' que me sobran 
            index +=1
        while sync[index] != True :  # saco los '0 ' que me sobran 
            index +=1
    return index

# cuts all signals from one signal and return array of N-signals
def cutsAllSignals(signals, sync):
    cutSignals = []
    counter = 0 
    index = InitIdex(sync)    # Init index with high puse ('1')

    while index < len(signals) - 800 :
        pulseSignal = []
        # add pulse 1 signas :
        while sync[index] == True :
            pulseSignal.append(signals[index])
            index +=1 
        # add puse 0 signals :
        while sync[index] ==False:
            pulseSignal.append(signals[index])
            index +=1 
        # ----
        if counter == 0 :
            size_of_signal = len(pulseSignal)
            pading = 0 
            counter +=1
        else :
            pading = len(pulseSignal)-size_of_signal

        if pading==0 :  # Caso que tiene la misma dimension 
            cutSignals.append( (pulseSignal) ) # add direct 
        else:
            if pading < 0 :  # Es mas chico y tenes que agregar ceros 
                cutSignals.append(  np.concatenate( ( pulseSignal , np.zeros(abs(pading)) ),axis=0  ))
            else :  # AUX es mas grande que el primero, hay que cortarlo 
                cutSignals.append((  (pulseSignal[0:size_of_signal] ) )) # add direct 

        # add to my list of cut signals 
        # print('size of pulse :', len(pulseSignal))
    return cutSignals  # return all signals

# --- Media of list of vectors ---- 
def mediaVector(signals):
    media = np.array(signals[0])
    for index in range(1,len(signals)):
        media = media + np.array(signals[index])
    return media/len(signals)

# --- remuve clutter   ----  to remuve cross talk ---- signal :
def clutterRemuve(signals):
    clutterless = []
    media =  np.array(mediaVector(signals))
    #print('len of media', len(media))
    for signal in signals:
        #print('len of signal', len(signal))
        clutterless.append( np.array(signal)-media) 
    return clutterless

def todB(signal):
    return 20*np.log10(signal)

def converter_to_dB(signals) :
    signals_in_dB = []
    for signal in signals:
        signals_in_dB.append(todB(signal))
    return signals_in_dB

# return the max value from a array of nsignals
def maximous(signals):
    maxValue = max(signals[0])
    for signal in signals :
        if maxValue < max(signal):
            maxValue = max(signal)
        else:
            pass
    return maxValue

#  --- gets fft of arrays vectors ---
def spectroSignal(signals,nfft):
    fftsignals = []
    phaseSignals = []
    for signal in signals:
        aux = ((np.fft.fft(signal, nfft)) )
        #print('Maximo : ', max(aux))
        #aux = aux/max(aux)
        STEP = 350
        fftsignals.append(abs( np.concatenate( (aux[int(nfft/2):int(nfft/2)+STEP] ,aux[0:int(nfft/2)-STEP] ),axis=0) )) ################################### here !!!
        #if np.real(aux[0:int(nfft/2)]) != 0:
        phaseSignals.append( np.arctan( np.imag(aux[0:int(nfft/2)])/np.real(aux[0:int(nfft/2)]) ))
        #else :
        #phaseSignals.append( np.pi/2 )
# **-- tener la fase del sistema nfes que se au :
    maxValue =  maximous(fftsignals)
    # Normalize 
    fftsignals = fftsignals/maxValue
        
    return fftsignals, phaseSignals

def padingSignal(signal, ceroPadding) :
    # --- Padding -----
    padingSignal = np.pad(signal, ceroPadding )
    return padingSignal 

def  spectralSignal(signal,freqSampling):
    # DFT cut signal and mean , todas las muetras.
    fftSignal =  np.fft.fft(signal , NFFT)   
    fftsignalPhase = np.arctan(  np.imag(fftSignal[1:int(NFFT/2)]) /  np.real(fftSignal[1:int(NFFT/2)])  ) 
    fftsignalModule = abs(fftSignal[1:int(NFFT/2)] )
    return fftsignalModule,fftsignalPhase


def RMA(sif, pulse_period=20e-3, freq_range=None, Rs=9.0):
  
  if freq_range is None:
    freq_range = [2260e6, 2590e6] # Values from MIT

  N, M = len(sif), len(sif[0])

  # construct Kr axis
  delta_x = feet2meters(2/12.0) # Assuming 2 inch antenna spacing between frames.
  bandwidth = freq_range[1] - freq_range[0]
  center_freq = bandwidth/2 + freq_range[0]
  Kr = numpy.linspace(((4*PI/C)*(center_freq - bandwidth/2)), ((4*PI/C)*(center_freq + bandwidth/2)), M)

  # smooth data with hanning window
  sif *= numpy.hanning(M)

  '''STEP 1: Cross-range FFT, turns S(x_n, w(t)) into S(Kx, Kr)'''
  # Add padding if we have less than this number of crossrange samples:
  # (requires numpy 1.7 or above)
  rows = (max(2048, len(sif)) - len(sif)) / 2
  try:
    sif_padded = numpy.pad(sif, [[rows, rows], [0, 0]], 'constant', constant_values=0)
  except Exception, e:
    print "You need to be using numpy 1.7 or higher because of the numpy.pad() function."
    print "If this is a problem, you can try to implement padding yourself. Check the"
    print "README for where to find cansar.py which may help you."
    raise e
  # N may have changed now.
  N = len(sif_padded)

  # construct Kx axis
  Kx = numpy.linspace(-PI/delta_x, PI/delta_x, N)

  freqs = numpy.fft.fft(sif_padded, axis=0) # note fft is along cross-range!
  S = numpy.fft.fftshift(freqs, axes=(0,)) # shifts 0-freq components to center of spectrum

  '''
  STEP 2: Matched filter
  The overlapping range samples provide a curved, parabolic view of an object in the scene. This
  geometry is captured by S(Kx, Kr). Given a range center Rs, the matched filter perfectly
  corrects the range curvature of objects at Rs, partially other objects (under-compsensating
  those close to the range center and overcompensating those far away).
  '''
  Krr, Kxx = numpy.meshgrid(Kr, Kx)
  phi_mf = Rs * numpy.sqrt(Krr**2 - Kxx**2)
  # Remark: it seems that eq 10.8 is actually phi_mf(Kx, Kr) = -Rs*Kr + Rs*sqrt(Kr^2 - Kx^2)
  # Thus the MIT code appears wrong. To conform to the text, uncomment the following line:
  #phi_mf -= Rs * Krr
  # However it is left commented by default because all it seems to do is shift everything downrange
  # closer to the radar by Rs with no noticeable improvement in picture quality. If you do
  # uncomment it, consider just subtracting Krr instead of Krr multiplied with Rs.
  S_mf = S * numpy.exp(1j*phi_mf)

  '''
  STEP 3: Stolt interpolation
  Compensates range curvature of all other scatterers by warping the signal data.
  '''

  kstart, kstop = 73, 108.5 # match MIT's matlab -- why are these values chosen?
  Ky_even = numpy.linspace(kstart, kstop, 1024)

  Ky = numpy.sqrt(Krr**2 - Kxx**2) # same as phi_mf but without the Rs factor.
  try:
    S_st = numpy.zeros((len(Ky), len(Ky_even)), dtype=numpy.complex128)
  except:
    S_st = numpy.zeros((len(Ky), len(Ky_even)), dtype=numpy.complex)
  # if we implement an interpolation-free method of stolt interpolation,
  # we can get rid of this for loop...
  for i in xrange(len(Ky)):
    interp_fn = scipy.interpolate.interp1d(Ky[i], S_mf[i], bounds_error=False, fill_value=0)
    S_st[i] = interp_fn(Ky_even)

  # Apply hanning window again with 1+
  window = 1.0 + numpy.hanning(len(Ky_even))
  S_st *= window

  '''
  STEP 4: Inverse FFT, construct image
  '''

  ifft_len = [len(S_st), len(S_st[0])] # if memory allows, multiply both
  # elements by 4 for perhaps a somewhat better image. Probably only viable on 64-bit Pythons.
  S_img = numpy.fliplr(numpy.rot90(numpy.fft.ifft2(S_st, ifft_len)))

  return {'Py_S_image': S_img, 'S_st_shape': S_st.shape, 'Ky_len': len(Ky), 'delta_x': delta_x, 'kstart': kstart, 'kstop': kstop}

# Based off of example from cansar.py, previously just called out to
# a reduced Matlab/Octave script.
def plot_img(sar_img_data):
  '''Creates the 2D SAR image and saves it as sar_img_data['outfilename'], default sar_image.png.'''
  # Extract S_image, S_st_shape, Ky_len, delta_x, kstart, kstop, Rs, cr1, cr2, dr1, dr2 
  # from sar_img_data
  S_image = sar_img_data['Py_S_image']
  for k, v in sar_img_data.iteritems():
    if k != 'Py_S_image':
      exec('%s=%s' % (k, repr(v)))
  bw = C*(kstop-kstart)/(4*PI)
  max_range = (C*S_st_shape[1]/(2*bw))*1/0.3048

  # data truncation
  dr_index1 = int(round((dr1/max_range)*S_image.shape[0]))
  dr_index2 = int(round((dr2/max_range)*S_image.shape[0]))
  cr_index1 = int(round(S_image.shape[1] * (
    (cr1+Ky_len*delta_x/(2*0.3048)) / (Ky_len*delta_x/0.3048) )))
  cr_index2 = int(round(S_image.shape[1] * (
    (cr2+Ky_len*delta_x/(2*0.3048)) / (Ky_len*delta_x/0.3048) )))

  trunc_image = S_image[dr_index1:dr_index2, cr_index1:cr_index2]
  downrange = numpy.linspace(-1*dr1, -1*dr2, trunc_image.shape[0]) + Rs
  crossrange = numpy.linspace(cr1, cr2, trunc_image.shape[1])

  for i in xrange(0, trunc_image.shape[1]):
    trunc_image[:,i] = (trunc_image[:,i]).transpose() * (abs(downrange*0.3048))**(3/2.0)
  trunc_image = 20 * numpy.log10(abs(trunc_image))

  pylab.figure()
  pylab.pcolormesh(crossrange, downrange, trunc_image, edgecolors='None')
  pylab.plt.gca().invert_yaxis()
  pylab.colorbar()
  pylab.clim([numpy.max(trunc_image)-40, numpy.max(trunc_image)-0])
  pylab.title('Final image')
  pylab.ylabel('Downrange (ft)')
  pylab.xlabel('Crossrange (ft)')
  pylab.axis('equal')
  # Note 'retina' density is about 300, but will increase time of plotting.
  pylab.savefig(sar_img_data['outfilename'], bbox_inches='tight', dpi=200)

def make_sar_image(setup_data):
  '''Gets the frames from an input file, performs the RMA on the SAR data,
  and saves to an output image.'''
  filename = setup_data['filename']

  sif = get_sar_frames(*open_wave(filename), pulse_period=MOD_PULSE_PERIOD)

  if setup_data['bgsub']:
    sif_bg = get_sar_frames(*open_wave(setup_data['bgsub']), pulse_period=MOD_PULSE_PERIOD)
    for i in range(len(sif)):
      if i < len(sif_bg):
        sif[i] -= sif_bg[i]

  Rs = setup_data['Rs']
  freq_range = VCO_FREQ_RANGE
  prefix = filename.split('/')[-1].split('-')[0].lower()
  if prefix == 'mit':
    freq_range = None

  sar_img_data = RMA(sif, pulse_period=MOD_PULSE_PERIOD, freq_range=freq_range, Rs=feet2meters(Rs))

  sar_img_data['outfilename'] = setup_data['outfilename']
  sar_img_data['Rs'] = Rs
  sar_img_data['cr1'] = setup_data['cr1']
  sar_img_data['cr2'] = setup_data['cr2']
  sar_img_data['dr1'] = setup_data['dr1'] + Rs
  sar_img_data['dr2'] = setup_data['dr2'] + Rs

  plot_img(sar_img_data)