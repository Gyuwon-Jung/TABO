from mido import MidiFile

mid = MidiFile('MIDI_school.mid')
mididict = []
output = []

# Put all note on/off in midinote as dictionary.
for i in mid:
    if i.type in ('note_on', 'note_off', 'time_signature'):
        mididict.append(i.dict())
# change time values from delta to relative time.
mem1=0
for i in mididict:
    time = i['time'] + mem1
    i['time'] = time
    mem1 = i['time']
# make every note_on with 0 velocity note_off
    if i['type'] == 'note_on' and i['velocity'] == 0:
        i['type'] = 'note_off'
# put note, starttime, stoptime, as nested list in a list. # format is [type, note, time, channel]
    mem2=[]
    if i['type'] in ('note_on', 'note_off'):
        mem2.append(i['type'])
        mem2.append(i['note'])
        mem2.append(i['time'])
        mem2.append(i['channel'])
        output.append(mem2)
# put timesignatures
    if i['type'] == 'time_signature':
        mem2.append(i['type'])
        mem2.append(i['numerator'])
        mem2.append(i['denominator'])
        mem2.append(i['time'])
        output.append(mem2)

clean_midi = []
on_air = [] 
for i in range(len(output)):
    event_type, note, time, channel = output[i]
    if event_type == 'note_on':
        on_air.append({'note': note, 'time': time, 'index': i }) 
        clean_midi.append(output[i])
    elif event_type == 'note_off':
        dirty_found = False

        for entry in on_air:
            if entry['note'] == note:
                if entry['time'] == time:
                    for j in range(len(clean_midi)):
                        if clean_midi[j][0] == 'note_on' and clean_midi[j][1] == note and clean_midi[j][2] == time:
                            clean_midi.pop(j)
                            dirty_found = True
                            break
                
                if not dirty_found:
                    clean_midi.append(output[i])
                
                on_air.remove(entry)
                break

print(mid.ticks_per_beat)
print(len(output))
print(len(clean_midi))

def midi_note_to_name(midi_note):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note_index = midi_note % 12
    note_name = note_names[note_index]
    return f"{note_name}{octave}"

# clean_midi의 음표들을 음표 이름으로 변환하여 출력
for event in clean_midi:
    event[1] = midi_note_to_name(event[1])
 
note_on_events = []
note_off_events = []

for event in clean_midi:
    event_type, note, time, channel = event
    
    if event_type == 'note_on':
        note_on_events.append((note, time))
    elif event_type == 'note_off':
        note_off_events.append((note, time))

def time_to_note(note_on_events, note_off_events):
    final_events = []

    for i in range(len(note_on_events)):
        note_pointer = note_on_events[i][0]
        time_pointer = note_on_events[i][1]
        for j in range(len(note_off_events)):
            if time_pointer >= note_off_events[j][1]:
                continue
            elif note_pointer == note_off_events[j][0]:
                beat = note_list(time_pointer, note_off_events[j][1])
                final_events.append({'note': note_pointer, 'beat': beat, 'start_time': time_pointer})
                break
    
    return final_events
                
def note_list(on_time, off_time):
    time = off_time - on_time
     
    if time == 0.25:
        beat = 'q'  #임시
    elif time == 0.5:
        beat = 'h'  #임시

    return beat

final_events = time_to_note(note_on_events, note_off_events)
for event in final_events:
    print(event)