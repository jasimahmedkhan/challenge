import pyaudio
import wave
import sys


class AudioPlayer:
    def __init__(self, filename: str):
        self.__chunk = 1024

        self.__wf = wave.open(filename)

        self.__p = pyaudio.PyAudio()

    def open_stream(self, audio_buffer_callback):

        stream = self.__p.open(format=self.__p.get_format_from_width(
            self.__wf.getsampwidth()),
            channels=self.__wf.getnchannels(),
            rate=self.__wf.getframerate(),
            output=True)

        data = self.__wf.readframes(self.__chunk)

        # play stream (3)
        while len(data) > 0:
            stream.write(data)
            data = self.__wf.readframes(self.__chunk)
            audio_buffer_callback(data)
        # while True:
        #     buffer = stream.read(self.__chunk)

        #     audio_buffer_callback(buffer)
        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
