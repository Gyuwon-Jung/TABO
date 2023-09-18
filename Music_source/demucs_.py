import demucs.separate
import shlex
demucs.separate.main(shlex.split('--wav --two-stems vocals -n mdx_extra "bass.wav"'))