from picosynth import PicoSynth, Channel
from time import sleep
from collections import OrderedDict
from math import pow, sin, pi
from jtruk_music_track import track
import re

synth = PicoSynth()

# this handy list converts notes into frequencies
# (Thanks Gagetoid)
TONES = OrderedDict({
    "B0": 31,
    "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62,
    "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123,
    "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247,
    "C4": 262, "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494,
    "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988,
    "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
    "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
    "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
})

TONES_LIST=list(TONES)

class MusicChannel:
    def __init__(self, chIndex, conf):
        self.volume = conf['volume']
        self.channel = synth.channel(chIndex)

        # waveforms you can use are NOISE, SQUARE, SAW, TRIANGLE, SINE, or WAVE
        # you can combine more than one, like this: waveforms=Channel.SQUARE | Channel.SAW,
        self.channel.configure(**conf)
        
        # We'll either have none for both of these, or a note, or an arpRing list
        self.baseFreq = None
        self.triggerAttack = False
        self.triggerRelease = False
        
        self.iStep = 0
        self.arpRing = None

        self.vibratoAmp = None
        self.nVibrato = None

    def decode(self, noteRaw):
        cellSplit = noteRaw.split(":")
        note = cellSplit[0]
        
        clearEffects = False
        if note == "-":
            # stop sound
            self.triggerRelease = True
            clearEffects = True

        elif note != "":
            self.baseFreq = TONES[note]
            self.triggerAttack = True
            clearEffects = True
        
        if clearEffects:
            self.arpRing = None
            self.vibratoAmp = None
        
        for iPart in range(1, len(cellSplit)):
            # The regex will capture:
            # (0) note (optional)
            # (1) Optional- modifier (a for arp)
            # (2) Number string
            noteCtrl = re.search("^(\w)(\w+)?$", cellSplit[iPart])
            noteCtrlMatch=noteCtrl.groups()
            if noteCtrlMatch[0] == 'a':
                # Arp
                self.arpRing = [0]
                for arpOffset in noteCtrlMatch[1]:	# Fill the rest of the arp slots
                    self.arpRing += [int("0x"+arpOffset)]
            elif noteCtrlMatch[0] == 'v':
                # Vibrato
                self.vibratoAmp = int("0x"+noteCtrlMatch[1][0])
                self.nVibrato = int("0x"+noteCtrlMatch[1][1])
            elif noteCtrlMatch[0] == 'l':
                # Loudness (v is taken!)
                self.volume = int("0x"+noteCtrlMatch[1][0])/15.0
            
    def playSlot(self, iSlot):
        freq = self.baseFreq

        # Effects
        if self.arpRing != None:
            arpOffset = self.arpRing[self.iStep%len(self.arpRing)]
            freq *= pow(1.0595, arpOffset)

        if self.vibratoAmp != None and self.nVibrato >= 1:
            freqAmp = (self.vibratoAmp/15)*(.0595 * freq)
            # Not sure if +1 is right, or if it should be +2
            freq += sin(pi*2*self.iStep/(self.nVibrato+1))*freqAmp

        self.channel.frequency(int(freq))
        self.channel.volume(self.volume)

        if self.triggerAttack:
            self.channel.trigger_attack()
            self.triggerAttack = False
        if self.triggerRelease:
            self.channel.trigger_release()
            self.triggerRelease = False

        self.iStep += 1


# C4		Start note (attack) e.g. C, 4th Octave
#  -		Stop note (release)
# :a(xyz+)	Arpeggio (through hexidecimal values)
# :l(x)		Loudness (0-15) - beware clicks if this is changed mid-note play!
# :v(xy)	Vibrato (depth, speed)

class MusicPlayer:
    def __init__(self, patterns, rowTime, stepsPerRow):
        self.patterns = patterns
        self.rowTime = rowTime
        self.stepsPerRow = stepsPerRow

        self.iPattern = 0
        self.iRow = 0
                
        self.channels = [
            MusicChannel(0, {
                "waveforms": Channel.SINE | Channel.TRIANGLE,
                "attack": 0.1, "decay": 0.01, "sustain": 0.1, "release": .2,
                "volume": .6
            }), MusicChannel(1, {
                "waveforms": Channel.SINE,
                "attack": 0.1, "decay": 0.1, "sustain": 0.1, "release": 0.1,
                "volume": 1
            }), MusicChannel(2, {
                "waveforms": Channel.NOISE,
                "attack": 0.0, "decay": 0.1, "sustain": 0.0, "release": 0,
                "volume": .5
            })
        ]
        
    # rowTime is the time step between rows
    # stepsPerRow affects arp and vibrato
    def play(self):
        nChannels = len(self.patterns[0])
        synth.play()

        while True:
            for iCh in range(nChannels):
                cellRaw = self.patterns[self.iPattern][iCh][self.iRow]
                self.channels[iCh].decode(cellRaw)

            for i in range(self.stepsPerRow):
                for iCh in range(nChannels):
                    self.channels[iCh].playSlot(i)        
                sleep(self.rowTime/self.stepsPerRow)

            self.iRow += 1
            if self.iRow>=len(self.patterns[self.iPattern][0]):
                self.iRow=0
                self.iPattern=(self.iPattern+1)%len(self.patterns)

# musicPlayer = MusicPlayer(track, .06, 3)
# musicPlayer.play()
