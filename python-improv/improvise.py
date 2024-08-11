from scamp import *
from scamp_extensions.pitch import Scale
# scale is SUPER useful!
import random
import sys

s = Session()
s.tempo = 100

piano = s.new_part("piano")
flute = s.new_part("flute")
clarinet = s.new_part("clarinet")


def close_note_chord(pitch,chord):
    chord_pitches = [chord[1],chord[2],chord[3],chord[4]]
    print(chord1)
    choices = []
    for w in range(2):
        for x in chord_pitches:
            chord1 = Scale.from_pitches(chord_pitches)
            if len(choices) == w:
                choices.append(x)   
            elif abs(x-pitch) < abs(pitch-choices[w]):
                choices[w] = x
        chord1.remove(choices[w])
    return random.choice(choices)

def longest(nested_list):
    if len(nested_list) == 0:
        return 0
    max = nested_list[0]
    for n in nested_list:
        if len(n) > len(max):
            max = n
    return max

def get_rhythm_motifs(num_motifs=4, motif_length_beats=4, duration_options=[0.25, 0.5]):
    rhythm_motifs = []
    for _ in range(num_motifs):
        motif = []
        while sum(motif) < motif_length_beats:
            motif.append(random.choice(duration_options))
        if sum(motif) > motif_length_beats:
            motif[-1] = (motif_length_beats - sum(motif[0:-1]))
        rhythm_motifs.append(motif)
    '''
    for m in rhythm_motifs:
        print(f"# of notes in rhythm motif: {len(m)}")
    print(f"Notes in max rhythm motif: {len(longest(rhythm_motifs))}")
    print(f"Notes in max rhythm motif: {len(longest(rhythm_motifs))}")
    print(f"Index of max rhythm motif: {rhythm_motifs.index(longest(rhythm_motifs))}")
    '''
    return rhythm_motifs
    #print(f"Rhythm motifs: {rhythm_motifs}")

def get_pitch_shift_motifs(rhythm_motifs, num_motifs=4, interval_options=[1,2]):
    # list of lists of pitch-shifts
    motif_length = len(longest(rhythm_motifs))
    pitch_shift_motifs = []
    direction = 1
    for _ in range(num_motifs):
        motif = [0]
        for _ in range(motif_length-1):
            if random.random() < 0.2:
                direction *= -1
            motif.append(motif[-1]+random.choice(interval_options)*direction)
        pitch_shift_motifs.append(motif)
    '''
    for m in pitch_shift_motifs:
        print(f"Notes in pitch motif: {len(m)}")
    '''
    #print(f"Pitch shift motifs: {pitch_shift_motifs}")
    return pitch_shift_motifs

def create_note2midi():
    note2midi = {}
    note_names = [['a'],['a#','bb'],['b','cb'],['b#','c'],['c#','db'],['d'],['d#','eb'],['e','fb'],['e#','f'],['f#','gb'],['g'],['g#','ab']]
    i = 0
    for notes in note_names:
        for note in notes: 
            note2midi[note]=57+i
        i += 1
    return note2midi

def get_chord_quality2scale(root):
    chord_quality2scale = {
        'major7': Scale.ionian(root),
        'dominant7': Scale.mixolydian(root),
        'minor7': Scale.dorian(root),
        'augmented': Scale.from_pitches([root, root+2, root+4, root+5, root+7, root+8, root+10, root+12]),
        'diminished': Scale.from_pitches([root,root+1,root+3,root+4,root+6,root+7,root+9,root+10,root+12])
    }
    return chord_quality2scale


def get_chord_quality2arpeggio(root):
    chord_quality2arpeggio = {
        'major7': Scale.from_pitches([root,root+4,root+7,root+11,root+12]),
        'dominant7': Scale.from_pitches([root,root+4,root+7,root+10,root+12]),
        'minor7': Scale.from_pitches([root,root+3,root+7,root+10,root+12]),
        'augmented': Scale.from_pitches([root,root+4,root+8,root+12]),
        'diminished': Scale.from_pitches([root,root+3,root+6,root+9,root+12])
    }
    return chord_quality2arpeggio

def get_rhythm_set(num_measures, rhythm_motifs, beats_per_measure=4):
    # create a rhythm set
    rhythm_set = []
    while sum(rhythm_set) < num_measures * beats_per_measure:
        # loose e.g. of rhythm_motifs's value: [ [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1] ]
        rhythm_set += random.choice(rhythm_motifs)

    # "going overboard": when total duration exceeds num_measures * beats_per_measure, truncate the extra
    # num_measures = 1, beats_per_measure = 4, and rhythm_set = [0.5,1,0.5,1,0.75,0.5,1,0.5]
    while sum(rhythm_set) > num_measures * beats_per_measure:
        rhythm_set.remove(rhythm_set[-1])
        # aftermath: rhythm_set = [0.5,1,0.5,1,0.75]
    if sum(rhythm_set) < num_measures * beats_per_measure:
        rhythm_set.append(num_measures * beats_per_measure - sum(rhythm_set))
        # aftermath: rhythm_set = [0.5,1,0.5,1,0.75,0.25]
    return rhythm_set

def get_scale_note_from_range(scale, bottom, top):
    valid_notes = []
    for i in range(bottom, top+1):
        if scale.ceil(i) == i:
            valid_notes.append(i)
    return random.choice(valid_notes)

def get_pitch_set(rhythm_set, pitch_shift_motifs, scale, previous_pitch=None):
     # create a pitch set
    pitch_set = []
    while len(pitch_set) < len(rhythm_set):
        # Append a pitch set. Each item of pitch set is scale[degree + motif[i]]
        # determining the scale degree that the motifs are relative to
        degree = 0
        if previous_pitch != None:
            print(previous_pitch)
            # degree = pitch within a major 3rd of previous_pitch. degree != previous_pitch
            for pitch in (list(range(previous_pitch-4, previous_pitch)) + list(range(previous_pitch+1, previous_pitch+5))):
                if pitch in scale: 
                    degree = scale.pitch_to_degree(pitch)
        else:
            # if there's no previous pitch, I want degree to range from ~G3 to ~D5
            bottom_pitch = scale[0]
            top_pitch = scale[7]
            bottom_pitch = get_scale_note_from_range(scale, 53, 56)
            top_pitch = get_scale_note_from_range(scale, 72,75)
            '''
            for pitch in range(53, 57): # ~G3
                if pitch in scale:
                    bottom_pitch = pitch
            for pitch in range(72,76): # ~D5
                if pitch in scale: 
                    top_pitch = pitch
            '''
            degree = random.randrange(bottom_pitch, top_pitch)
        motif = random.choice(pitch_shift_motifs)
        for shift in motif: 
            pitch_set.append(scale[degree+shift])
        previous_pitch = int(pitch_set[-1])
    # taking "going overboard" into account
    pitch_set = pitch_set[0: len(rhythm_set)]
    return pitch_set

def melody(instr,chord_prog,measures_per_chord):

    rhythm_motifs = get_rhythm_motifs()
    pitch_shift_motifs = get_pitch_shift_motifs(rhythm_motifs)

    all_pitches = []
    all_rhythms = []

    note2midi = create_note2midi()

    for chord, num_measures in zip(chord_prog,measures_per_chord): # append a bunch of pitches to all_pitches and a bunch of rhythms to all_rhythms

        # find root note of chord
        chord = chord.lower().strip().split() # e.g. chord = ['a', 'major7']
        root = note2midi[chord[0]]
        
        chord_quality2scale = get_chord_quality2scale(root)
        chord_quality2arpeggio = get_chord_quality2arpeggio(root)

        # corresponding series of notes to scale/chord name
        scale = chord_quality2scale[chord[1]]
        arpeggio = chord_quality2arpeggio[chord[1]]

        print(f"Scale: {scale[0:8]}")
        
        rhythm_set = get_rhythm_set(num_measures, rhythm_motifs)
        all_rhythms += rhythm_set

        previous_pitch = None
        if len(all_pitches) > 0:
            previous_pitch = int(all_pitches[-1])
        pitch_set = get_pitch_set(rhythm_set, pitch_shift_motifs, scale, previous_pitch)
        all_pitches += pitch_set
        
    for pitch,dur in zip(all_pitches, all_rhythms):
        instr.play_note(pitch,1,dur)
    print(all_pitches)

# Andy recommends putting chords in the background

def chord(chord_prog, measures_per_chord):
    for key,measures in zip(chord_prog,measures_per_chord):
        # find root note of chord
        key = key.lower().strip().split()
        note2midi = create_note2midi()
        root = note2midi[key[0]]
        chord_quality2arpeggio = get_chord_quality2arpeggio(root)
        '''
        chromatic = [['a'],['a#','bb'],['b','cb'],['b#','c'],['c#','db'],['d'],['d#','eb'],['e','fb'],['e#','f'],['f#','gb'],['g'],['g#','ab']]
        for x in range(len(chromatic)):
            if key[0] in chromatic[x]:
                root = 57+x
        corresp_chords = {
                'major7': Scale.from_pitches([root,root+4,root+7,root+11,root+12]),
                'dominant7': Scale.from_pitches([root,root+4,root+7,root+10,root+12]),
                'minor7': Scale.from_pitches([root,root+3,root+7,root+10,root+12]),
                'augmented': Scale.from_pitches([root,root+4,root+8,root+12]),
                'diminished': Scale.from_pitches([root,root+3,root+6,root+9,root+12])
            }
        '''
        print(f"key[1] = {key[1]}")
        chord = chord_quality2arpeggio[key[1]]
        print(f"chord = {chord}")
        bottom_note = get_scale_note_from_range(chord, 51,55)
        '''
        bottom_note = None
        for note in range(47, 52):
            print(f"note = {note}")
            if chord.ceil(note) == note: # TODO: write function to clear readers' confusions
                print(f"note in chord: {note}")
                bottom_note = note
                break
        '''
        print(f"bottom_note: {bottom_note}")
        bottom_note_index = chord.pitch_to_degree(bottom_note)
        print(chord[bottom_note: bottom_note+4])
        piano.play_chord(chord[bottom_note_index : bottom_note_index+4],0.7,measures*4)

def bass(notes,measures_per_chord):
    for note,measures in zip(notes,measures_per_chord):
        chromatic = [['a'],['a#','bb'],['b','cb'],['b#','c'],['c#','db'],['d'],['d#','eb'],['e','fb'],['e#','f'],['f#','gb'],['g'],['g#','ab']]
        for x in range(len(chromatic)):
            if note.lower().strip().split()[0] in chromatic[x]:
                root_note = 33+x
                '''
                for _ in range(4*measures):
                    piano.play_note(root_note,0.5,1,"staccato")
                '''
        beats_per_measure = 4
        piano.play_note(root_note,0.5,measures*beats_per_measure)

chord_prog = ['e minor7','c major7','b minor7','f dominant7']
measures_per_chord = [1,1,1,1]


fork(melody,args=[piano, chord_prog, measures_per_chord])
fork(chord,args=[chord_prog, measures_per_chord])
fork(bass,args=[chord_prog,measures_per_chord])
wait_for_children_to_finish()

#piano.play_note(random.choice([67,71,74,79]),1,4,blocking=False)
