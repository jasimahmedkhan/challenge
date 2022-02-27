import pyaudio
import wave
import config
import numpy as np

class AudioPlayer:
    def __init__(self, filename: str):
        self.__filename = filename
        self.__wf = wave.open(filename)
        self.__chunk = int(self.__wf.getframerate() / config.FPS)

        self.__p = pyaudio.PyAudio()

    def convert_stereo_to_mono(self, y):
        left = np.array([el for i, el in enumerate(y) if i % 2 == 0])
        right = np.array([el for i, el in enumerate(y) if i % 2 != 0])
        return right + left / 2

    def fft_analysis(self, data: np.ndarray)-> np.ndarray:
        # Normalize samples between 0 and 1
        y = data / 2.0 ** 15

        N = len(y)
        N_zeros = 2 ** int(np.ceil(np.log2(N))) - N
        # Pad with zeros until the next power of two
        y_padded = np.pad(y, (0, N_zeros), mode='constant')
        ys = np.abs(np.fft.rfft(y_padded)[:N // 2])
        xs = np.fft.rfftfreq(len(y_padded), 1.0 / self.__wf.getframerate())[:N // 2]

        return xs, ys

    def open_stream(self, audio_buffer_callback: callable):

        stream = self.__p.open(format=self.__p.get_format_from_width(
            self.__wf.getsampwidth()),
            channels=self.__wf.getnchannels(),
            rate=self.__wf.getframerate(),
            output=True)

        data = self.__wf.readframes(self.__chunk)
        print(f"now playing {self.__filename}")

        # we will grap some audio data from the audio file and use it to
        # 1. write the data to a PyAudio stream, so you can hear the audio on the speakers
        # 2. analyze the data using FFT in order to obtain the frequencies present in the sound
        # 3. send both this data to the audio_buffer_callback
        while len(data) > 0:
            stream.write(data)

            data = self.__wf.readframes(self.__chunk)
            y = np.frombuffer(data, dtype=np.int16)

            if self.__wf.getnchannels() == 2:
                y = self.convert_stereo_to_mono(y)

            frequency_bins, frequency = self.fft_analysis(y)
            audio_buffer_callback(y, frequency_bins, frequency)

        # close the audio stream
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        self.__p.terminate()
