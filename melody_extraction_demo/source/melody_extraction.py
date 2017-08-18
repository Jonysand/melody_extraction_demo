"""
By Jonathan Lee in 2017.08

Originally referring to
<Melody Extraction from Polyphonic Music Signals using Pitch Contour Characteristics>
by Justin Salamon

"""

import librosa
from scipy import signal
import numpy as np
import math


# to find proper N(FFT window size)
def find_proper_2n(N):
    i = 1

    while True:
        if (math.pow(2, i) - N) <= N <= (math.pow(2, i + 1) - N):
            break
        else:
            i += 1

    N = math.pow(2, i + 1)

    return N


def Sinusoid_extraction(data, sr):
    # Equal Loudness Filtering
    # Following parameters from "http://replaygain.hydrogenaud.io/proposal/equal_loudness.html"
    Ay = [1.00000000000000,
          -3.47845948550071,
          6.36317777566148,
          -8.54751527471874,
          9.47693607801280,
          -8.81498681370155,
          6.85401540936998,
          -4.39470996079559,
          2.19611684890774,
          -0.75104302451432,
          0.13149317958808]
    By = [0.05418656406430,
          -0.02911007808948,
          -0.00848709379851,
          -0.00851165645469,
          -0.00834990904936,
          0.02245293253339,
          -0.02596338512915,
          0.01624864962975,
          -0.00240879051584,
          0.00674613682247,
          -0.00187763777362]
    Ab = [1.00000000000000,
          -1.96977855582618,
          0.97022847566350]
    Bb = [0.98500175787242,
          -1.97000351574484,
          0.98500175787242]
    data_lfiltered = signal.lfilter(b=Bb, a=Ab, x=signal.lfilter(b=By, a=Ay, x=data))

    # F the spectral resolution
    # T the sample time distance, usually <= 1/2fh, fh the highest frequency component
    # N the fft window size, better power of 2
    # F = 1 / (len(data) / sr)
    fh = 22050
    # T = 1 / (2 * fh)
    # N = 1 / (F * T)
    N = (len(data) / sr) * 2 * fh
    N = int(find_proper_2n(N))
    # print N

    # Frequency/Amplitude Correction; Short- Time Fourier Transform (STFT)
    # data_stft = librosa.core.stft(y=data, n_fft=N)
    data_if, data_stft = librosa.ifgram(y=data, hop_length=128, win_length=2048, n_fft=8192)

    return data_lfiltered, data_stft, data_if


# Given a frequency f in Hz, its corresponding bin B(f) is calculated as:
def B(f):
    b = int((1200 * math.log(f / 55, 2)) / 10 + 1)
    return b


# Given a bin n, its corresponding frequency f in Hz is calculated as:
def F(n):
    i = (n - 1) / 120
    f = 55 * math.pow(2, i)
    return f


def Salience_Function(data_if, sr):
    # Nh the number of harmonics considered
    Nh = 20
    # S the input time frequency magnitude representation
    S = np.abs(data_if)
    freqs = librosa.core.fft_frequencies(sr)
    print (freqs.shape)

    # with parameters following:
    # alpha = 0.8; beta = 1; Nh = 20; gamma >= 40 dB

    # harms the harmonics to include in salience computation
    harms = []
    for i in range(Nh):
        harms.append(i + 1)

    # calculate weights
    weights = []
    for h in range(1, Nh + 1):
        for n in range(600):
            i = n + 1
            sigma = abs(B(F(n) / h) - n) / 10
            if sigma <= 1:
                break;
        g = math.cos(sigma * math.pi / 2) * math.cos(sigma * math.pi / 2) * math.pow(0.8, h - 1)
        weights.append(g)

    #data_sal = 0
    data_sal = librosa.salience(S, freqs, harms, weights, fill_value=0)

    return data_sal


if __name__ == "__main__":
    # audio_path = raw_input("please enter the audio path:")
    audio_path = "../data/demo.wav"

    print("Loading audio...")
    data, sr = librosa.load(audio_path)
    # for the sample here, tp=2s,sr=22050

    print ("Step 1:Sinusoid Extraction")
    data_lfiltered, data_stft, data_if = Sinusoid_extraction(data, sr)
    print (data_stft.shape)

    print ("Step 2:Salience Function Computation")
    data_sal = Salience_Function(data_if, sr)
