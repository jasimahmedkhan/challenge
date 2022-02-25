import SendData
import numpy as np
import config
import AudioPlayer


# data = np.zeros((3, config.LENGTH))

# data[0, :] = 255

# senddata = SendData.SendData()

# senddata.send_data(data)


def test_cb(buffer):
    print(buffer)




if __name__ == '__main__':
    player = AudioPlayer.AudioPlayer("songs/MEDUZA - Tell It To My Heart.wav")
    player.open_stream(test_cb)