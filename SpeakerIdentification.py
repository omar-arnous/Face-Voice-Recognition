import os
import time
import pickle
import warnings
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture
from pydub import AudioSegment
import os
import wave
import ffmpeg

import sys
sys.path.append('C:\\ffmpeg\\bin')


warnings.filterwarnings("ignore")

class VoiceRecognition():
    def __init__(self, audio, name):
        # AudioSegment.from_file(audio, format='m4a')
        audio_file = ffmpeg.input(audio)
        self.audio = audio_file.export("audio", format='wav')
        self.name = name

    def register_audio(self):
        Recordframes = []
        start = 0
        end = 7000
        for count in range(5):
            Recordframes.append(self.audio[start:end])
            OUTPUT_FILENAME =  self.name + "-sample" + str(count) + ".wav"
            WAVE_OUTPUT_FILENAME = os.path.join("voice recognition\\training_set", OUTPUT_FILENAME)
            trainedfilelist = open("voice recognition\\training_set_addition.txt", 'a')
            trainedfilelist.write(OUTPUT_FILENAME + "\n")
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(1)
            waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(44100)
            waveFile.writeframes(b''.join(Recordframes))
            waveFile.close()
            start += 7000
            end += 7000
        self.train_model()


    def calculate_delta(self, array):
        rows, cols = array.shape
        print(rows)
        print(cols)
        deltas = np.zeros((rows, 20))
        N = 2
        for i in range(rows):
            index = []
            j = 1
            while j <= N:
                if i - j < 0:
                    first = 0
                else:
                    first = i - j
                if i + j > rows - 1:
                    second = rows - 1
                else:
                    second = i + j
                index.append((second, first))
                j += 1
            deltas[i] = (array[index[0][0]] - array[index[0][1]] + (2 * (array[index[1][0]] - array[index[1][1]]))) / 10
        return deltas


    def extract_features(self, audio, rate):
        mfcc_feature = mfcc.mfcc(audio, rate, 0.025, 0.01, 20, nfft=1200, appendEnergy=True)
        mfcc_feature = preprocessing.scale(mfcc_feature)
        print(mfcc_feature)
        delta = self.calculate_delta(mfcc_feature)
        combined = np.hstack((mfcc_feature, delta))
        return combined


    def train_model(self):
        source = "\\voice recognition\\training_set\\"
        dest = "\\voice recognition\\trained_models\\"
        train_file = "\\voice recognition\\training_set_addition.txt"
        file_paths = open(train_file, 'r')
        count = 1
        features = np.asarray(())
        for path in file_paths:
            path = path.strip()
            print(path)

            sr, audio = read(source + path)
            print(sr)
            vector = self.extract_features(audio, sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))

            if count == 5:
                gmm = GaussianMixture(n_components=6, max_iter=200, covariance_type='diag', n_init=3)
                gmm.fit(features)

                # dumping the trained gaussian model
                picklefile = path.split("-")[0] + ".gmm"
                pickle.dump(gmm, open(dest + picklefile, 'wb'))
                print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)
                features = np.asarray(())
                count = 0
            count = count + 1
        return 1


    def test_model(self):
        source = ".\\voice recognition\\testing_set\\"
        modelpath = "\\voice recognition\\trained_models\\"
        test_file = "\\voice recognition\\testing_set_addition.txt"
        file_paths = open(test_file, 'r')

        gmm_files = [os.path.join(modelpath, fname) for fname in
                    os.listdir(modelpath) if fname.endswith('.gmm')]

        # Load the Gaussian gender Models
        models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
        speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
                    in gmm_files]

        # Read the test directory and get the list of test audio files
        for path in file_paths:

            path = path.strip()
            print(path)
            sr, audio = read(source + path)
            vector = self.extract_features(audio, sr)

            log_likelihood = np.zeros(len(models))

            for i in range(len(models)):
                gmm = models[i]  # checking with each model one by one
                scores = np.array(gmm.score(vector))
                log_likelihood[i] = scores.sum()

            winner = np.argmax(log_likelihood)
            print("\t detected as - ", speakers[winner])
            return speakers[winner]
            time.sleep(1.0)

    # while True:
    #     choice = int(
    #         input("\n 1.Train Model \n 2.Test Model \n"))
    #     if choice == 1:
    #         train_model()
    #     elif choice == 2:
    #         test_model()
    #     elif choice > 2:
    #         exit()
