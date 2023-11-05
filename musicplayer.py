from picosynth import PicoSynth, Channel
from time import sleep
from collections import OrderedDict
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
        self.note = None
        self.arpRing = None
        self.iArpRing = 0

    def decode(self, noteRaw):
        if noteRaw == "":
            # no effect
            True
        elif noteRaw == "-":
            # stop sound
            self.note = None
            self.arpRing = None
            self.channel.trigger_attack()
        else:
            # The regex will capture:
            # (0) note
            # (1) Optional- modifier (a for arp)
            # (2) Number string
            noteDef = re.search("^(\wS?\d)(?::(a)(\w+))?$", noteRaw)
            noteDefMatch=noteDef.groups()
            note=noteDefMatch[0]
            
            self.note = None
            self.arpRing = None
            if noteDefMatch[1] == None:
                self.note = note
            elif noteDefMatch[1] == 'a': # We have an arp!
                baseNoteIndex=TONES_LIST.index(note)
                # Our arp will hit note 0, then whatever else we've specified, and then loop
                # Add the baseNote index to each of our arpRingOffsets
                self.arpRing = [TONES_LIST[baseNoteIndex]]
                for arpInc in noteDefMatch[2]:
                    # Fill the rest of the arp slots
                    self.arpRing += [TONES_LIST[baseNoteIndex+int("0x"+arpInc)]]
                self.iArpRing = 0
            self.channel.volume(self.volume)

    def playSlot(self, iSlot):
        if self.note:
            if iSlot == 0:
                self._triggerSound(self.note)
                self.note = None	# Notes just fire once
        elif self.arpRing != None:
            self._triggerSound(self.arpRing[self.iArpRing%len(self.arpRing)])
            self.iArpRing += 1

    def _triggerSound(self, tone):
        self.channel.frequency(TONES[tone])
        self.channel.trigger_attack()

class MusicPlayer:
    def __init__(self):
        self.iPattern = 0
        self.iRow = 0
        
        self.channels = [
            MusicChannel(0, {
                "waveforms": Channel.SINE | Channel.TRIANGLE,
                "attack": 0.1, "decay": 0.01, "sustain": 0.1, "release": 2,
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
        
        # :a(X+) Arpeggio (through hexidecimal values)
        phrases = {
            "empty": ["", "", "", "", "", "", "", ""],
            "lead1": ["C5:a47", "", "D5:a47", "", "G5:a47", "", "F5:a47", ""],
            "lead2": ["D4", "", "D5", "", "", "", "G4", ""],
            "lead3": ["E4:a37", "", "", "", "", "", "", ""],
            "lead4": ["C4:a47", "", "", "", "", "", "", "-"],
            "bass1": ["C2", "", "C1", "", "C2", "", "C3", ""],
            "bass2": ["D2", "", "G1", "", "C3", "", "G3", ""],
            "beats1": ["C3", "", "", "", "C3", "", "", ""],
            "beats2": ["", "", "C7", "", "C8", "", "", ""],
        }
              
        self.patterns=[]
        self.patterns.append([[],[],[]])
        
        self.patterns[0][0].extend(phrases["lead1"])
        self.patterns[0][0].extend(phrases["lead2"])
        self.patterns[0][0].extend(phrases["lead3"])
        self.patterns[0][0].extend(phrases["lead4"])

        self.patterns[0][1].extend(phrases["bass1"])
        self.patterns[0][1].extend(phrases["bass1"])
        self.patterns[0][1].extend(phrases["bass2"])
        self.patterns[0][1].extend(phrases["bass2"])
        
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["beats2"])
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["beats2"])
        
    def run(self, waitTime):
        arpsPerRow = 4
        synth.play()

        while True:
            for iCh in range(3):
                noteRaw = self.patterns[self.iPattern][iCh][self.iRow]
                self.channels[iCh].decode(noteRaw)

            for i in range(arpsPerRow):
                for iCh in range(3):
                    self.channels[iCh].playSlot(i)        
                sleep(waitTime/arpsPerRow)

            self.iRow += 1
            if self.iRow>=len(self.patterns[self.iPattern][0]):
                self.iRow=0
                self.iPattern=(self.iPattern+1)%len(self.patterns)
                
musicPlayer = MusicPlayer()
musicPlayer.run(.06)
