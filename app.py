import SendData
import numpy as np
import config
import AudioPlayer

send_data = SendData.SendData()


def audio_data_cb(audio_buffer,fft):
    #Example: send data to the simulator 
    #Simulator should be fully red
    data = np.zeros((3, config.LENGTH))
    data[0,:]=255
    

    #input here functions to manipulate, analyze and convert the data and it to the simulator
    #data should be in the format [[RED,RED,RED...],[GREEN,GREEN...],[BLUE...]]


    send_data.send_data(data)


if __name__ == '__main__':
    #initialize the audio player
    player = AudioPlayer.AudioPlayer("songs/MEDUZA - Tell It To My Heart.wav")

    #start the audio player with callback function as input
    player.open_stream(audio_data_cb)

    #play second song
    player = AudioPlayer.AudioPlayer("songs/MEDUZA - Tell It To My Heart.wav")
    player.open_stream(audio_data_cb)
