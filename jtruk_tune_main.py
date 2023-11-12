patterns = []

phrases = {
    "empty": ["", "", "", "", "", "", "", ""],
    "lead1": ["C5:a37", "", "D5:a47", "", "G5:a47", "", "F5:a47", ""],
    "lead2": ["D4", "", "D5", "", "", "", "G4", ""],
    "lead3": ["E4:a37", "", "", "", "", "", "", ""],
    "lead4": ["C4:v47", "", "", "", "", "", "", "-"],
    "bass1": ["C2", "", "C1", "", "C2", "", "C3", ""],
    "bass2": ["D2", "", "G1", "", "C3", "", "G3", ""],
    "beats1": ["C3", "", "", "", "C3", "", "", ""],
    "beats2": ["", "", "C7", "-", "C8", "", "", ""],
}

patterns.append([[],[],[]])
        
patterns[0][0].extend(phrases["lead1"])
patterns[0][0].extend(phrases["lead2"])
patterns[0][0].extend(phrases["lead3"])
patterns[0][0].extend(phrases["lead4"])

patterns[0][1].extend(phrases["bass1"])
patterns[0][1].extend(phrases["bass1"])
patterns[0][1].extend(phrases["bass2"])
patterns[0][1].extend(phrases["bass2"])
        
patterns[0][2].extend(phrases["beats1"])
patterns[0][2].extend(phrases["beats2"])
patterns[0][2].extend(phrases["beats1"])
patterns[0][2].extend(phrases["beats2"])

tune = {
    "rowInterval": 0.06,
    "stepsPerRow": 4,
    "patterns": patterns
}