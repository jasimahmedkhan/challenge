import pyaudio
import wave
import sys
import numpy as np

class AudioPlayer:
    def __init__(self, filename: str):
        self.__chunk = 1024
        self.__filename = filename

        self.__wf = wave.open(filename)

        self.__p = pyaudio.PyAudio()

    def fft_analysis(self, data: np.ndarray)-> np.ndarray:
        # Normalize samples between 0 and 1
        y = data / 2.0 ** 15

        N = len(y)
        N_zeros = 2 ** int(np.ceil(np.log2(N))) - N
        # Pad with zeros until the next power of two
        y_padded = np.pad(y, (0, N_zeros), mode='constant')
        ys = np.abs(np.fft.rfft(y_padded)[:N // 2])

        return ys

    def open_stream(self, audio_buffer_callback: callable):

        stream = self.__p.open(format=self.__p.get_format_from_width(
            self.__wf.getsampwidth()),
            channels=self.__wf.getnchannels(),
            rate=self.__wf.getframerate(),
            output=True)

        data = self.__wf.readframes(self.__chunk)
        print(f"now playing {self.__filename}")

        # play stream (3)
        while len(data) > 0:
            stream.write(data)
            y = np.frombuffer(data, dtype=np.int16)

            data = self.__wf.readframes(self.__chunk)
            fft = self.fft_analysis(y)
            audio_buffer_callback(data,fft)

        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
