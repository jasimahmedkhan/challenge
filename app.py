import SendData
import numpy as np
import config
import AudioPlayer
import argparse

send_data = SendData.SendData()

""" 
This is the main function to be modified by you.

It receives three inputs:
    1. audio_buffer (np.ndarray with length 735): the raw audio data.
    2. frequency bins (np.ndarray with length 367): the bins in which the frequency spectrum is quantitized in.
    3. frequency (np.ndarray with length 367): the intensity of different frequencies in the currently played audio.

This function is being called, in the case of config.FPS == 60, 60 times a second. This means that it receives both the raw audio data & the present
frequencies in the audio data for only ~16.6ms of audio every time it is called. If you would modify config.FPS, this would change however.
"""
def audio_data_cb(audio_buffer: np.ndarray, frequency_bins: np.ndarray, frequency: np.ndarray) -> None:
    # Example of preparing the data to be displayed in the simulator -> this should turn every pixel in the simulator red
    data = np.zeros((3, config.LENGTH))
    data[0, :] = 255

    #input here functions to manipulate, analyze and convert the data and it to the simulator
    #data should be in the format [[RED,RED,RED...],[GREEN,GREEN...],[BLUE...]]
    send_data.send_data(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("song")
    args = parser.parse_args()

    #initialize the audio player
    player = AudioPlayer.AudioPlayer(args.song)

    #start the audio player with callback function as input
    player.open_stream(audio_data_cb)