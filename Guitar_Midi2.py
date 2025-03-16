import pygame
import pygame.midi

# Initialize pygame and MIDI
pygame.init()
pygame.midi.init()

# Create an invisible window (necessary for event loop)
pygame.display.set_mode((1, 1))  # 1x1 pixel window, invisible

# Open MIDI output
player = pygame.midi.Output(0)
player.set_instrument(24)  # Acoustic Guitar

# Key mappings for strings (same as before)
string_keys = {
    pygame.K_b: 0,  # Low E
    pygame.K_n: 1,  # A
    pygame.K_m: 2,  # D
    pygame.K_i: 3,  # G
    pygame.K_o: 4,  # B
    pygame.K_p: 5   # High E
}

# Chord mappings for each Nashville Numbering Key
chord_mappings = { #Open Tuning [40, 45, 50, 55, 59, 64]
    "NNC": {  # C Major Key
        pygame.K_1: [48, 48, 52, 55, 60, 64],  # C (I)
        pygame.K_2: [50, 50, 50, 57, 62, 65],  # D Minor (ii)
        pygame.K_3: [40, 47, 52, 55, 59, 64],  # E Minor (iii)
        pygame.K_4: [53, 53, 53, 57, 60, 65],  # F (IV)
        pygame.K_5: [43, 47, 50, 55, 59, 67],  # G (V)
        pygame.K_6: [45, 45, 52, 57, 60, 64],  # A Minor (vi)
        pygame.K_7: [50, 50, 50, 56, 59, 65],  # B Diminished (vii°)
        pygame.K_8: [40, 45, 50, 55, 59, 64],  # Open
    },
    "NND": {  # D Major Key
        pygame.K_1: [50, 50, 50, 57, 62, 66],  # D (I)
        pygame.K_2: [40, 47, 52, 55, 59, 64],  # E Minor (ii)
        pygame.K_3: [42, 49, 54, 57, 61, 66],  # F# Minor (iii)
        pygame.K_4: [43, 47, 50, 55, 59, 67],  # G (IV)
        pygame.K_5: [45, 45, 52, 57, 61, 64],  # A (V)
        pygame.K_6: [47, 47, 54, 59, 62, 66],  # B Minor (vi)
        pygame.K_7: [49, 49, 52, 55, 61, 64],  # C# Diminished (vii°)
        pygame.K_8: [40, 45, 50, 55, 59, 64],  # Open
    },
    "NNE": {  # E Major Key
        pygame.K_1: [40, 47, 52, 56, 59, 64],  # E (I)
        pygame.K_2: [42, 49, 54, 57, 61, 66],  # F# Minor (ii)
        pygame.K_3: [44, 51, 56, 59, 63, 68],  # G# Minor (iii)
        pygame.K_4: [45, 45, 52, 57, 61, 64],  # A (IV)
        pygame.K_5: [47, 51, 54, 59, 63, 66],  # B (V)
        pygame.K_6: [49, 49, 56, 61, 64, 68],  # C# Minor (vi)
        pygame.K_7: [51, 51, 51, 57, 63, 66],  # D# Diminished (vii°)
        pygame.K_8: [40, 45, 50, 55, 59, 64],  # Open
    },
    "NNF": {  # F Major Key
        pygame.K_1: [53, 53, 53, 57, 60, 65],  # F (I)
        pygame.K_2: [43, 50, 55, 58, 62, 67],  # G Minor (ii)
        pygame.K_3: [45, 45, 52, 57, 60, 64],  # A Minor (iii)
        pygame.K_4: [46, 46, 50, 58, 62, 65],  # Bb (IV)
        pygame.K_5: [48, 48, 52, 55, 60, 64],  # C (V)
        pygame.K_6: [50, 50, 50, 57, 62, 65],  # D Minor (vi)
        pygame.K_7: [52, 52, 52, 58, 64, 67],  # E Diminished (vii°)
        pygame.K_8: [40, 45, 50, 55, 59, 64],  # Open
    },
    "NNG": {  # G Major Key
        pygame.K_1: [43, 47, 50, 55, 59, 67],  # G (I)
        pygame.K_2: [45, 45, 52, 57, 60, 64],  # A Minor (ii)
        pygame.K_3: [47, 47, 54, 59, 62, 66],  # B Minor (iii)
        pygame.K_4: [48, 48, 52, 55, 60, 64],  # C (IV)
        pygame.K_5: [50, 50, 50, 57, 62, 66],  # D (V)
        pygame.K_6: [40, 47, 52, 55, 59, 64],  # E Minor (vi)
        pygame.K_7: [54, 54, 54, 57, 60, 66],  # F# Diminished (vii°)
        pygame.K_8: [40, 45, 50, 55, 59, 64],  # Open
        pygame.K_9: [None],  # End/error Function

    }
}

# Track selected key and chord
selected_key = "NNC"  # Default to key of C
selected_chord = pygame.K_1  # Default chord

# Keyboard mappings for key selection
key_selection = {
    pygame.K_c: "NNC",
    pygame.K_d: "NND",
    pygame.K_e: "NNE",
    pygame.K_f: "NNF",
    pygame.K_g: "NNG",
}

# Track pressed keys to avoid retriggering
pressed_keys = {}

# Function to mute changed notes
def mute_changed_notes(old_chord, new_chord):
    for idx in range(6):
        if old_chord[idx] != new_chord[idx]:  # If the note has changed
            note_to_stop = old_chord[idx]
            if note_to_stop in pressed_keys.values():
                player.note_off(note_to_stop, 64)
                print(f"Muted note: {note_to_stop}")  # Debugging

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Change key (C or D)
            if event.key in key_selection:
                selected_key = key_selection[event.key]
                print(f"Switched to {selected_key}")  # Debugging

            # Change chord
            if event.key in chord_mappings[selected_key]:
                new_chord = chord_mappings[selected_key][event.key]
                mute_changed_notes(chord_mappings[selected_key][selected_chord], new_chord)
                selected_chord = event.key
                print(f"Chord selected: {event.key}")  # Debugging

            # Play string notes based on selected chord
            if event.key in string_keys:
                note = chord_mappings[selected_key][selected_chord][string_keys[event.key]]
                player.note_on(note, 127)
                pressed_keys[event.key] = note
                print(f"Playing string: {event.key}, note: {note}")  # Debugging

pygame.midi.quit()
pygame.quit()
