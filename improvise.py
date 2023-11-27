from scamp import *
from scamp_extensions.pitch import Scale
# scale is SUPER useful!
import random

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

def melody(instr,chord_prog,measures_per_chord):

    # make a list of lists of durations
    rhythm_motifs = []
    for _ in range(4):
        motif = []
        while sum(motif) < 4:
            motif.append(random.choice([0.25,0.5]))
        if sum(motif) < 4:
            motif.append(4 - sum(motif))
        elif sum(motif) > 4:
            motif[-1] -= sum(motif) - 4
        rhythm_motifs.append(motif)
    #print(f"Rhythm motifs: {rhythm_motifs}")
    
    # list of lists of pitch-shifts
    motif_length = len(max(rhythm_motifs))
    pitch_shift_motifs = []
    direc = 1
    for _ in range(4):
        motif = [0]
        for _ in range(motif_length-1):
            if random.random() > 0.5:
                direc *= -1
            motif.append(motif[-1]+random.choice([1,2])*direc)
        pitch_shift_motifs.append(motif)
    #print(f"Pitch shift motifs: {pitch_shift_motifs}")

    for key,measures in zip(chord_prog,measures_per_chord):
        # find root note of chord
        key = key.lower().strip().split()
        chromatic = [['a'],['a#','bb'],['b','cb'],['b#','c'],['c#','db'],['d'],['d#','eb'],['e','fb'],['e#','f'],['f#','gb'],['g'],['g#','ab']]
        for x in range(len(chromatic)):
            if key[0] in chromatic[x]:
                root = 57+x
        print(f"Root note in midi notation: {root}")
        
        corresp_scales = {
            'major7': Scale.ionian(root),
            'dominant7': Scale.mixolydian(root),
            'minor7': Scale.dorian(root),
            'augmented': Scale.melodic_minor(root-4,4),
            'diminished': Scale.from_pitches([root,root+1,root+3,root+4,root+6,root+7,root+9,root+10,root+12])
        }

        corresp_chords = {
            'major7': Scale.from_pitches([root,root+4,root+7,root+11,root+12]),
            'dominant7': Scale.from_pitches([root,root+4,root+7,root+10,root+12]),
            'minor7': Scale.from_pitches([root,root+3,root+7,root+10,root+12]),
            'augmented': Scale.from_pitches([root,root+4,root+8,root+12]),
            'diminished': Scale.from_pitches([root,root+3,root+6,root+9,root+12])
        }

        # corresponding series of notes to scale/chord name
        scale = corresp_scales[key[1]]
        chord = corresp_chords[key[1]]
        print(f"Scale: {scale[0:8]}")

        for m in rhythm_motifs:
            print(f"Motif duration: {sum(m)}")


        '''
        degree = random.randrange(-12,12)
        interval = 1
        for _ in range(len(rhythm)):
            if len(pitches) > 0:
                degree += interval
                pitches.append(scale[degree])
            elif len(pitches) == 0 and len(all_pitches) > 0:
                blah = close_note_chord(all_pitches[-1],scale)
                print(all_pitches[-1],blah)
                pitches.append(blah) 
            else:
                pitches.append(scale[degree])
            if random.random() < 0.4:
                interval *= -1
        #pitches[0],pitches[-1] = random.choice(chord),random.choice(chord)
        all_pitches += pitches
        '''

        for _ in range(measures):
            pitch_shifts = list(random.choice(pitch_shift_motifs))
            rhythms = random.choice(rhythm_motifs)
            scale_snip = scale[-3:17]
            #print(scale_snip)
            note = random.choice(scale[-3:17])
            index = random.randrange(-5,10)
            pitches = []
            for p in pitch_shifts:
                pitches.append(scale[index+p])
                #print(f"Modified pitch: {pitches[p]}")
            print(f"Pitches: {pitches}")
            for pitch,dur in zip(pitches,rhythms):
                #print(f"Pitch & duration: {pitch,dur}")
                instr.play_note(pitch,1,dur)

        '''
        for pitch,dur in zip(pitches,rhythm):
            if pitch == 0:
                wait(dur)
            else:
                instr.play_note(pitch,1,dur)
        '''

# Andy recommends putting chords in the background

def bass(notes,measures_per_chord):
    for note,measures in zip(notes,measures_per_chord):
        chromatic = [['a'],['a#','bb'],['b','cb'],['b#','c'],['c#','db'],['d'],['d#','eb'],['e','fb'],['e#','f'],['f#','gb'],['g'],['g#','ab']]
        for x in range(len(chromatic)):
            if note.lower().strip().split()[0] in chromatic[x]:
                root_note = 33+x
                for _ in range(4*measures):
                    piano.play_note(root_note,0.5,1,"staccato")

chord_prog = ['a minor7','d minor7','e augmented','e augmented','a minor7']
measures_per_chord = [1,1,1,1,1]


fork(melody,args=[clarinet,chord_prog,measures_per_chord])
fork(bass,args=[chord_prog,measures_per_chord])
wait_for_children_to_finish()
#piano.play_note(random.choice([67,71,74,79]),1,4,blocking=False)
#piano.play_note(43,1,4)
