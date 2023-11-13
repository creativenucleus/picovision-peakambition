phrases = {
    "empty": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "intro1": ["C5:a5", "", "", "", "", "", "", "", "", "", "", "", "", "DS4:a4", "", ""],
    "intro2": ["AS4:a5", "", "", "", "", "", "", "", "", "", "", "", "", "F4:a9", "", ""],
    "intro3": ["G4:a7", "", "", "", "", "", "", "", "", "", "", "", "", "C4:aa", "", ""],
    "intro4": ["G4:a5", "", "", "", "", "", "", "", "", "", "", "", "", "AS4:a9", "", ""],
    "lead1": ["C5:a37a", "", "", "", "", "", "", "", "C5:a25a", "", "", "", "", "", "", ""],
    "lead2": ["C5:a37a", "", "", "", "", "", "", ""],
    "bass1": ["C2", "", "", "", "", "C2", "", "", "-", "", "", "", "", "", "", ""],
    "bass2a": ["AS1", "", "", "", "", "AS1", "", "", "-", "", "", "", "", "", "", ""],
    "bass2b": ["F2", "", "", "", "", "F2", "", "", "-", "", "", "", "", "", "", ""],
    "bassx": ["C2", "", "C3", "", "C2", "", "C4", ""],
    "bassy": ["F2", "", "F3", "", "DS1", "", "DS2", ""],
    "bass3": ["C3:v12", "", "", "DS2", "", "", "F2", ""],
    "beats1": ["C7", "", "", "", "C7:l3", "", "C7:l1", "", "C7", "", "", "", "C7:l3", "", "C7:l1", ""],
    "beats3": ["C3", "", "", "", "C3", "", "", ""],
    "beats2": ["", "", "C7", "-", "C8", "", "", ""],
}

# Each pattern is 64 rows in length
patternDefs = {
    "empty": ["empty", "empty", "empty", "empty"],
    "intro1": ["intro1", "empty", "empty", "empty"],
    "intro2": ["intro2", "empty", "empty", "empty"],
    "intro3": ["intro3", "empty", "empty", "empty"],
    "intro4": ["intro4", "empty", "empty", "empty"],
    "bass1": ["bass1", "bass1", "bass1", "bass1"],
    "bass2": ["bass2a", "bass2a", "bass2b", "bass2b"],
    "beats1": ["beats1", "beats1", "beats1", "beats1"],
    "lead1": ["lead1", "lead1", "lead1", "lead1"]
}

patterns = [
    ["intro1", "bass1", "beats1", "lead1"],
    ["intro2", "bass2", "beats1", "lead1"],
    ["intro3", "bass1", "beats1", "lead1"],
    ["intro4", "bass2", "beats1", "lead1"],
]

def assemblePatterns():
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
    return patternsOut
    
tune = {
    "rowInterval": 0.07,
    "stepsPerRow": 3,
    "patterns": assemblePatterns()
}

# For test - comment out for demo...
"""
from jtruk_music_player import MusicPlayer
import jtruk_thread_vars

jtruk_thread_vars.MUSIC_IN_ACTION = "play"
musicPlayer = MusicPlayer(tune)
musicPlayer.play()
"""