import pygame
import pygame.midi

# Initialize pygame and MIDI
pygame.init()
pygame.midi.init()

# Create an invisible window (necessary for event loop)
pygame.display.set_mode((1, 1))  # 1x1 pixel window, invisible

# Open MIDI output
player = pygame.midi.Output(0)
player.set_instrument(24)  # 24 is the MIDI instrument for Acoustic Guitar

# Key mappings for strings (adjust as needed for standard guitar tuning)
string_keys = {
    pygame.K_b: 0,  # Low E (E2)
    pygame.K_n: 1,  # A (A2)
    pygame.K_m: 2,  # D (D3)
    pygame.K_i: 3,  # G (G3)
    pygame.K_o: 4,  # B (B3)
    pygame.K_p: 5   # High E (E4)
}

# Chord mappings (example Nashville system chords in C major)
# These chords will correspond to each string (from low E to high E) with correct guitar tuning
chord_mappings = {
    pygame.K_1: [48, 48, 52, 55, 60, 64],  # C Major (I)
    pygame.K_2: [50, 50, 50, 57, 62, 65],  # D Minor (ii)
    pygame.K_3: [40, 47, 52, 55, 59, 64],  # E Minor (iii)
    pygame.K_4: [53, 53, 53, 57, 60, 65],  # F Major (IV)
    pygame.K_5: [43, 47, 50, 55, 59, 67],  # G Major (V)
    pygame.K_6: [45, 45, 52, 57, 60, 64],  # A Minor (vi)
    pygame.K_7: [50, 50, 50, 56, 59, 65],  # B Diminished (vii°)
}

# Variable to track the selected chord (default to C Major)
selected_chord = pygame.K_1

# Track pressed keys to avoid retriggering
pressed_keys = {}

# Function to mute only the changed notes
def mute_changed_notes(old_chord, new_chord):
    for idx in range(6):
        if old_chord[idx] != new_chord[idx]:  # If the note has changed
            note_to_stop = old_chord[idx]
            if note_to_stop in pressed_keys.values():
                # Stop the old note that has changed
                player.note_off(note_to_stop, 64)
                print(f"Muted note: {note_to_stop}")  # Debugging

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Mute the changed notes when the chord changes
            if event.key in chord_mappings:
                new_chord = chord_mappings[event.key]
                mute_changed_notes(chord_mappings[selected_chord], new_chord)  # Mute only changed notes
                selected_chord = event.key
                print(f"Chord selected: {event.key}")  # Debugging

            # Handle string key presses for the selected chord
            if event.key in string_keys:
                if selected_chord:
                    note = chord_mappings[selected_chord][string_keys[event.key]]
                    player.note_on(note, 127)  # Play the note
                    pressed_keys[event.key] = note
                    print(f"Playing string: {event.key}, note: {note}")  # Debugging

pygame.midi.quit()
pygame.quit()
