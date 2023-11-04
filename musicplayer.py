from picosynth import PicoSynth, Channel
from time import sleep

synth = PicoSynth()

class MusicPlayer:
    def __init__(self):
        self.volume = 1
        # this handy list converts notes into frequencies
        # (Thanks Gagetoid)
        self.tones = {
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
        
        phrases = {
            "empty": ["", "", "", "", "", "", "", ""],
            "lead1": ["C4", "", "F4", "", "G4", "", "C3", ""],
            "lead2": ["D4", "", "E4", "", "A4", "", "D3", ""],
            "bass1": ["C2", "", "C3", "", "C2", "", "C3", ""],
            "bass2": ["G2", "", "G3", "", "G2", "", "G3", ""],
            "beats1": ["C7", "", "", "", "C8", "", "C8", ""],
        }
              
        self.patterns=[]
        self.patterns.append([[],[],[]])
        self.patterns[0][0].extend(phrases["bass1"])
        self.patterns[0][0].extend(phrases["bass1"])
        self.patterns[0][0].extend(phrases["bass2"])
        self.patterns[0][0].extend(phrases["bass2"])
        self.patterns[0][0].extend(phrases["bass1"])
        self.patterns[0][0].extend(phrases["bass1"])
        self.patterns[0][0].extend(phrases["bass2"])
        self.patterns[0][0].extend(phrases["bass2"])
        self.patterns[0][1].extend(phrases["empty"])
        self.patterns[0][1].extend(phrases["empty"])
        self.patterns[0][1].extend(phrases["empty"])
        self.patterns[0][1].extend(phrases["empty"])
        self.patterns[0][1].extend(phrases["lead1"])
        self.patterns[0][1].extend(phrases["lead2"])
        self.patterns[0][1].extend(phrases["lead1"])
        self.patterns[0][1].extend(phrases["lead2"])
        self.patterns[0][2].extend(phrases["empty"])
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["empty"])
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["beats1"])
        self.patterns[0][2].extend(phrases["beats1"])
        
        self.iPattern=0
        self.iRow=0
        self.channels={}
        self.channels[0] = synth.channel(0)
        # change these details to modify the sound
        # waveforms you can use are NOISE, SQUARE, SAW, TRIANGLE, SINE, or WAVE
        # you can combine more than one, like this: waveforms=Channel.SQUARE | Channel.SAW,
        self.channels[0].configure(
            waveforms=Channel.SAW | Channel.TRIANGLE,
            attack=0.1,
            decay=0.1,
            sustain=0.1,
            release=2,
            volume=self.volume
        )

        self.channels[1] = synth.channel(1)
        self.channels[1].configure(
            waveforms=Channel.SINE,
            attack=0.1,
            decay=0.1,
            sustain=0.1,
            release=0.1,
            volume=self.volume
        )

        self.channels[2] = synth.channel(2)
        self.channels[2].configure(
            waveforms=Channel.NOISE,
            attack=0.0,
            decay=0.1,
            sustain=0.0,
            release=0.0,
            volume=self.volume
        )

    def run(self, waitTime):
        synth.play()

        while True:
            for chan in range(3):
                note=self.patterns[self.iPattern][chan][self.iRow]
                if note != "":
                    self.channels[chan].frequency(self.tones[note])
                    self.channels[chan].trigger_attack()
            
            self.iRow += 1
            if self.iRow>=len(self.patterns[self.iPattern][chan]):
                self.iRow=0
                self.iPattern=(self.iPattern+1)%len(self.patterns)
            sleep(waitTime)
