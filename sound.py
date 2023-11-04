# This basic example shows how you can use PicoSynth to play simple tones.
# It doesn't do anything with the display.

from picosynth import PicoSynth, Channel
import time

VOLUME = 1

# this handy list converts notes into frequencies
TONES = {
    "B0": 31,
    "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62,
    "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123,
    "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247,
    "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494,
    "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
    "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
    "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
    "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
}

TRACKS = {
    0: [
        ["C4", "C2", "C7"],
        ["", "", ""],
        ["F4", "C3", ""],
        ["", "", ""],
        ["G4", "C2", "C8"],
        ["", "", ""],
        ["C3", "C3", "C8"],
        ["", "", ""],
    ],
}

IROW=0
ITRACK=0

synth = PicoSynth()

CHANNELS={}

# create a new noise channel
CHANNELS[0] = synth.channel(0)
# change these details to modify the sound
# waveforms you can use are NOISE, SQUARE, SAW, TRIANGLE, SINE, or WAVE
# you can combine more than one, like this: waveforms=Channel.SQUARE | Channel.SAW,
CHANNELS[0].configure(
    waveforms=Channel.SAW | Channel.TRIANGLE,
    attack=0.1,
    decay=0.1,
    sustain=0.1,
    release=2,
    volume=VOLUME
)

CHANNELS[1] = synth.channel(1)
CHANNELS[1].configure(
    waveforms=Channel.SINE,
    attack=0.1,
    decay=0.1,
    sustain=0.1,
    release=0.1,
    volume=VOLUME
)

CHANNELS[2] = synth.channel(2)
CHANNELS[2].configure(
    waveforms=Channel.NOISE,
    attack=0.0,
    decay=0.1,
    sustain=0.0,
    release=0.0,
    volume=VOLUME
)

# for more details on what attack, decay, sustain and release mean, see:
# https://en.wikipedia.org/wiki/Synthesizer#ADSR_envelope

synth.play()

while True:
    for chan in range(3):
        note=TRACKS[ITRACK][IROW][chan]
        if note != "":
            CHANNELS[chan].frequency(TONES[note])
            CHANNELS[chan].trigger_attack()
    
    IROW += 1
    if IROW>=len(TRACKS[ITRACK]):
        IROW=0
        ITRACK=(ITRACK+1)%len(TRACKS)
    
    time.sleep(0.05)
