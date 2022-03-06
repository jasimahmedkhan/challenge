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


def sample_song(random, frequency, data):
    ## Sampling values based on frequency of the song or randomness to create the visualization
    if random:
        # Sampling based on random values between 0 to 100 where shape of the array is (3, 100)
        indices = np.random.randint(100, size=(3, 100))
        data[0, indices[0, :]] = 255
        data[1, indices[1, :]] = 255
        data[2, indices[2, :]] = 255
    else:
        # Sampling based on intensity of frequencey values where, we select 300 values and later normalize values based on thresholding. 
        values = np.random.choice(frequency, 300, replace=False)
        red = values[:100]
        green = values[100:200]
        blue = values[200:300]
        red = np.where(red > np.average(red), 255, 0).astype(float)
        green = np.where(green > np.average(green), 255, 0).astype(float)
        blue = np.where(blue > np.average(blue), 255, 0).astype(float)
        data[0, :] = red
        data[1, :] = green
        data[2, :] = blue
    
    return data


def audio_data_cb(audio_buffer: np.ndarray, frequency_bins: np.ndarray, frequency: np.ndarray) -> None:
    # Example of preparing the data to be displayed in the simulator -> this should turn every pixel in the simulator red
    data = np.zeros((3, config.LENGTH))
    # data[0, ::5] = 255
    # data[1, :] = 255
    # data[2, :] = 255
    # print("data = ", data)
        
    # print("data length = ", data.shape)
    
    #input here functions to manipulate, analyze and convert the data and it to the simulator
    # select random = 0 for creating values based on frequency of the song
    # select random = 1 for creating random values for visualization
    random = 0
    data = sample_song(random=random, frequency=frequency, data=data)
    
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