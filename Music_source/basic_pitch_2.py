from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

model_output, midi_data, note_events = predict("bass.wav")

print("Model Output:")
print(model_output)

print("MIDI Data:")
print(midi_data)

print("Note Events:")
print(note_events)