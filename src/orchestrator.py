# Generates clouds of frequency data from SPEAR analysis
# John Burnett

from abjad import *
from SPEAR import SPEAR_Analyzer

def main():
    analysis = SPEAR_Analyzer("../analysis/transitory_static.txt")
    analysis.populate_data(500)
    analysis.high_pass_filter(100)
    analysis.normalize_amplitudes()
    analysis.convert_to_midi()
    analysis.round_microtones(4)

    # score = to_piano_staff(analysis)
    score = to_piano_staff_with_amplitude_coloring(analysis)
    remove_common_tones(score)
    score = format_score(score)
    show(score)

#-------------------------------------------------------------------------------
#_Score

def to_chord_sequence(spear_data):
    staff = Staff()
    for i in range(len(spear_data)):
        pitch_set = []
        for j in range(len(spear_data[i])):
            pitch_set.append(spear_data[i][j][0])
        chord = Chord(pitch_set, (1,1))
        staff.append(chord)
    return staff


def to_piano_staff(SPEAR_analysis):
    spear_data = SPEAR_analysis.data

    top_staff = Staff()
    bot_staff = Staff()
    attach(Clef('bass'), bot_staff)

    for i in range(len(spear_data)):
        top_pitches = []
        bot_pitches = []
        for j in range(len(spear_data[i])):
            pitch = spear_data[i][j][0]
            if pitch >= 0:
                top_pitches.append(pitch)
            else:
                bot_pitches.append(pitch)
        top_chord = Chord(top_pitches, (1,1))
        bot_chord = Chord(bot_pitches, (1,1))
        top_staff.append(top_chord)
        bot_staff.append(bot_chord)

    score = Score([top_staff, bot_staff])
    return score


def to_piano_staff_with_amplitude_coloring(SPEAR_analysis):
    spear_data = SPEAR_analysis.data
    median = SPEAR_analysis.median_amplitude()

    top_staff = Staff()
    bot_staff = Staff()
    attach(Clef('bass'), bot_staff)

    for i in range(len(spear_data)):

        top_pitches = []
        bot_pitches = []

        for j in range(len(spear_data[i])):
            pitch = spear_data[i][j][0]
            if pitch >= 0:
                top_pitches.append(pitch)
            else:
                bot_pitches.append(pitch)

        top_chord = Chord(top_pitches, (1,1))
        bot_chord = Chord(bot_pitches, (1,1))

        for chord in [top_chord, bot_chord]:
            for j, note_head in enumerate(chord.note_heads):
                amplitude = spear_data[i][j][1]
                if amplitude < median:
                    note_head.tweak.color = 'grey'
                else:
                    note_head.tweak.color = 'black'

        top_staff.append(top_chord)
        bot_staff.append(bot_chord)

    score = Score([top_staff, bot_staff])
    return score


def remove_common_tones(score):
    for staff in score:
        for i in range(len(staff)):
            if i < len(staff):
                if str(staff[i]) == 's1':
                    continue

                pitches = list(staff[i].written_pitches)
                for pitch in pitches:
                    for j in range(i, len(staff)-1):
                        if str(staff[j+1]) == 's1':
                            break

                        # next_chord = staff[j+1]
                        following_pitches = list(staff[j+1].written_pitches)
                        pc_dict = make_pitch_color_dict(staff[j+1]) #remember colors

                        if pitch in following_pitches:
                            following_pitches.remove(pitch)
                            if len(following_pitches) > 0:
                                staff[j+1] = Chord(following_pitches,(1,1))
                                for note_head in (staff[j+1].note_heads):
                                    try:
                                        note_head.tweak.color = pc_dict[note_head.written_pitch]
                                    except KeyError:
                                        continue #temp fix

                            else:
                                staff[j+1] = scoretools.Skip((1,1))

                        else:
                            break


def format_score(score):
    for staff in score:
        override(staff).bar_line.stencil = False
        override(staff).time_signature.stencil = False
    lilypondFile = lilypondfiletools.make_basic_lilypond_file(score)
    lilypondFile.default_paper_size = '11x17', 'landscape'
    vector = layouttools.make_spacing_vector(0, 0, 10, 0)
    lilypondFile.paper_block.system_system_spacing = vector

    lilypondFile.header_block.title = Markup('Transitory Static')
    lilypondFile.header_block.composer = Markup('John Burnett')
    lilypondFile.header_block.tagline = Markup('')
    return lilypondFile


#-------------------------------------------------------------------------------
#_Utilities

def make_pitch_color_dict(chord):
    note_heads = chord.note_heads
    pc_dict = {}
    for note_head in note_heads:
        pitch = note_head.written_pitch
        try:
            color = note_head.tweak.color
        except AttributeError:
            continue #temp fix
        pc_dict[pitch] = color
    return pc_dict


#-------------------------------------------------------------------------------

main()
