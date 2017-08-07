"""
By Jonathan Lee in 2017.08

Originally referring to
<Melody Extraction from Polyphonic Music Signals using Pitch Contour Characteristics>
by Justin Salamon

"""

import librosa
from scipy import signal


def Sinusoid_extraction(data):
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
    data = signal.lfilter(b=Bb, a=Ab, x=signal.lfilter(b=By, a=Ay, x=data))
    print data

    # Spectral Transform: Short- Time Fourier Transform (STFT)
    data_stft = librosa.core.stft(y=data, hop_length=128, win_length=2048, n_fft=8192)

    # Frequency/Amplitude Correction
    

    return 0


if __name__ == "__main__":
    audio_path = raw_input("please enter the audio path:")

    print("Loading audio...")
    data, sr = librosa.load(audio_path)

    print ("Step 1:Sinusoid extraction")
    Sinusoid_extraction(data)
    librosa.output.write_wav('demo_result.wav', data, sr)
