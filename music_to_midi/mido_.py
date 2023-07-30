import mido

def parse_midi_file(filename):
    mid = mido.MidiFile(filename)

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':  # 음표 온 이벤트인 경우
                note_number = msg.note  # 음의 높이
                velocity = msg.velocity  # 음의 세기
                time = msg.time  # 박자 정보

                # 악보 정보 출력
                print(f"음의 높이: {note_number}, 음의 세기: {velocity}, 박자: {time} 틱")

# MIDI 파일 파싱 실행
midi_filename = 'bass_basic_pitch.mid'
parse_midi_file(midi_filename)
