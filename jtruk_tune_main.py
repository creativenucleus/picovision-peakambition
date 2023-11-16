def getTune():
    phrases = {
        "": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        "x1": ["C5:a5:lf", "", "", "", "", "", "", "", "", "", "", "", "", "DS4:a4", "", ""],
        "x2": ["AS4:a5:lf", "", "", "", "", "", "", "", "", "", "", "", "", "F4:a9", "", ""],
        "x3": ["G4:a7:lf", "", "", "", "", "", "", "", "", "", "", "", "", "C4:aa", "", ""],
        "x4": ["G4:a5:lf", "", "", "", "", "", "", "", "", "", "", "", "", "AS4:a9", "", ""],
        
        "lead1": ["C5:a37a:l6", "", "", "", "", "", "", "", "C5:a25a", "", "", "", "", "", "", ""],
        "lead1b": ["C5:a5ac:l6", "", "", "", "", "", "", "", "C5:a37a", "", "", "", "", "", "", ""],

        "bass1": ["C2:lf", "", "", "", "", "C2", "", "", "-", "", "", "", "", "", "", ""],
        "bass2a": ["AS1:lf", "", "", "", "", "AS1", "", "", "-", "", "", "", "", "", "", ""],
        "bass2b": ["F2:lf", "", "", "", "", "F2", "", "", "-", "", "", "", "", "", "", ""],
        
        "beats1": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "A3:a3f:l8", ""],
        "beats2": ["", "", "", "", "", "", "A3:a3f:l8", "", "C8", "", "", "", "", "", "A3:a3f:l8", ""],
        "beats2a": ["A3:a3f:l8", "", "", "", "", "", "A3:a3f:l8", "", "", "", "", "", "", "", "C8", ""],
        "beats2b": ["A3:a3f:l8", "", "C8", "", "", "", "A3:a3f:l8", "", "-", "C8", "", "C8", "", "", "C8", ""],
        "beats3": ["C7:l8", "", "", "", "", "C7:l3", "", "C7:l1", "", "C7", "", "", "", "C7:l3", "", "C7:l1", ""],
        
        "beatsx": ["C7:l8", "", "", "", "C7:l3", "", "C7:l1", "", "C7", "", "", "", "C7:l3", "", "C7:l1", ""],

        "beatsxx2": ["", "", "C7", "-", "C8", "", "", ""],
        "beatsxx3": ["C3", "", "", "", "C3", "", "", ""],

        "bassx": ["C2", "", "C3", "", "C2", "", "C4", "", "C2", "", "C3", "", "C2", "", "C4", ""],
        "bassy": ["F2", "", "F3", "", "DS1", "", "DS2", "", "F2", "", "F3", "", "DS1", "", "DS2", ""],
        "bass3": ["C3:v12", "", "", "DS2", "", "", "F2", "", "C3:v12", "", "", "DS2", "", "", "F2", ""],
        
        "intro1": ["C6:a5:v36:l0", ":l1", ":l5", ":l4", "", ":l3", "", ":l2", "", "", "", "", "", "", "", ":l1"],
        "intro2": ["DS5:a4:v36:l0", ":l2", ":l5", ":l4", "", ":l3", "", ":l2", "", "", "", "", "", "", "", ":l1"],
        "intro3": ["AS5:a5:v36:l0", ":l2", ":l5", ":l4", "", ":l3", "", ":l2", "", "", "", "", "", "", "", ":l1"],
        "intro4": ["F5:a9:v36:l0", ":l2", ":l5", ":l4", "", ":l3", "", ":l2", "", "", "", "", "", "", "", ":l1"],
    }

    # Each pattern is 64 rows in length
    patternDefs = {
        "": ["", "", "", ""],
        "intro1a": ["intro1", "", "intro2", ""],
        "intro1b": ["intro2", "", "intro3", ""],
        "intro2a": ["intro3", "", "intro4", ""],
        "intro2b": ["intro4", "", "intro1", ""],
        "bass1": ["bass1", "bass1", "bass1", "bass1"],
        "bass2": ["bass2a", "bass2a", "bass2b", "bass2b"],
        "beats1": ["beats1", "beats1", "beats1", "beats1"],
        "beats2": ["beats2", "beats2", "beats2a", "beats2b"],
        "lead1": ["lead1", "lead1", "lead1", "lead1"],
        "lead2": ["lead1", "lead1", "lead1", "lead1b"]
    }

    patterns = [
        ["", "", "", "intro1a"],
        ["", "", "", "intro2a"],
        ["", "", "", "intro1a"],
        ["", "", "", "intro2a"],
        ["", "intro1b", "", "intro1a"],
        ["", "intro2b", "", "intro2a"],
        ["", "intro1b", "", "intro1a"],
        ["", "intro2b", "", "intro2a"],
        ["", "bass1", "", "intro1a"],
        ["", "bass2", "", "intro2a"],
        ["", "bass1", "", "intro1a"],
        ["", "bass2", "", "intro2a"],
        ["", "bass1", "beats1", "intro1a"],
        ["", "bass2", "beats1", "intro2a"],
        ["", "bass1", "beats2", ""],
        ["", "bass2", "beats2", ""],
        ["", "bass1", "beats2", "lead1"],
        ["", "bass2", "beats2", "lead2"],
        ["", "bass1", "beats2", "lead1"],
        ["", "bass2", "beats2", "lead2"],
        ["intro1a", "bass1", "", ""],
        ["intro2a", "bass2", "", ""],
        ["", "bass1", "", ""],
        ["", "bass2", "", ""],
    ]

    patternsOut = []
    for pattern in patterns:
        patternBuild = []
        for patternDefID in pattern:
            # There's a patternDefID for each channel
            channelNotes = []
            patternDef = patternDefs[patternDefID]
            for phraseID in patternDef:
                phrase = phrases[phraseID]
                for note in phrase:
                    channelNotes.append(note)
            patternBuild.append(channelNotes)
        patternsOut.append(patternBuild)

    del patterns
    del patternDefs
    del phrases

    return {
        "rowInterval": 0.05,
        "stepsPerRow": 2,
        "patterns": patternsOut
    }

# For test - comment out for demo...
"""
from jtruk_music_player import MusicPlayer
import pa_shared_vars as shared_vars

shared_vars.MUSIC_IN_ACTION = "play"
musicPlayer = MusicPlayer(getTune())
musicPlayer.play()
"""