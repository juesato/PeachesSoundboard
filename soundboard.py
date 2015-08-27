import serial
import pygame.mixer
import pyaudio
import wave
import time
import datetime
import sys

# Recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

# Serial communication settings
# port = '/dev/ttyACM1'
port = sys.argv[1]
baud = 9600
ser = serial.Serial(port, baud)

pygame.mixer.init(48000, -16, 1, 1024)

# Pyaudio setup
pyAud = pyaudio.PyAudio()
stream = -1

# Which pins are which sounds?
LOOP_PIN = 0
sounds = { \
    1: pygame.mixer.Sound("sounds/Tom.wav"), \
    2: pygame.mixer.Sound("sounds/Snare.wav"), \
    3: pygame.mixer.Sound("sounds/HighHatShut.wav"), \
    4: pygame.mixer.Sound("sounds/HighHatOpen.wav") \
}

def saveRecording(start):
    frames = []
    elapsed_secs = time.time() - start
    print stream
    for i in range(0, int(RATE / CHUNK * elapsed_secs)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "saveRecording"
    stream.stop_stream()
    stream.close()
    # pyAud.terminate()

    print "term"
    filename = str(datetime.datetime.now()).split('.')[0]
    wf = wave.open('sounds/loop' + filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyAud.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def startRecording():
    print "startRecording"
    global stream
    stream = pyAud.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    return time.time()


while True:
    try:
        line = ser.readline()
        # print line
        if line[:4] == "play":
            print line
            number = int(line[4:].strip())
            if (number == LOOP_PIN):
                print "Recording loop..."
                start_time = startRecording()
            # print number
            else:
                sounds[number].play(loops=-1)
            # playingA = True
        else:
            if line[:4] == "stop":
                number = int(line[4:].strip())
                print number
                if number == LOOP_PIN:
                    print "before save"
                    looped = saveRecording(start_time)
                    print "Done recording. Looping..."
                    pygame.mixer.Sound('sounds/loop' + looped).play(loops=-1)
                else:
                    sounds[number].stop()
        # char = ser.read(size=1)
        # print char
    except Exception, e:
        print "Failed to read in the usual spot: ", e
        continue