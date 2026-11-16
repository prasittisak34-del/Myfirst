#!/bin/bash
# usage: tools/finish.sh PROJ "ชื่อคลิป"   -> PROJ/final/<ชื่อ> (มีเพลง).mp4, (ไม่มีเพลง).mp4, ปก <ชื่อ>.jpg
set -e
P=$(cd "$1" && pwd); NAME="$2"; E=$(cd "$(dirname "$0")/../engine" && pwd)  # project-local engine (move/scale/fadeout, bigger text)
END=$(cd "$P" && python3 -c "from episode import END;print(END)")
PROJ="$P" python3 "$E/audio.py"
W="$P/work"; mkdir -p "$P/final"
# music bed: MUSIC=/path/royalty-free.mp3, else the self-made synth bed (tools/music_synth.py); never a copyrighted song
if [ -z "$MUSIC" ]; then MUSIC="$W/music_bed.wav"; python3 -c "import sys,soundfile as sf; sys.path.insert(0,'$(dirname "$0")'); from music_synth import music_bed; sf.write('$MUSIC', music_bed($END + 1, 44100), 44100)"; fi
ffmpeg -v error -y -f f32le -ar 44100 -ac 2 -i "$W/sfx.f32" -i "$P/vo_trim.wav" -filter_complex "[1]aresample=44100,pan=stereo|c0=c0|c1=c0,apad=pad_dur=1[v];[0]volume=-10dB[s];[v][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$END,loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map "[a]" -ar 44100 "$W/mix_nomusic.wav"
ffmpeg -v error -y -f f32le -ar 44100 -ac 2 -i "$W/sfx.f32" -i "$P/vo_trim.wav" -stream_loop -1 -i "$MUSIC" -filter_complex "[1]aresample=44100,pan=stereo|c0=c0|c1=c0,apad=pad_dur=1[v];[0]volume=-10dB[s];[2]atrim=0:$END,volume=-23dB,afade=t=in:d=1,afade=t=out:st=$(python3 -c "print($END-1.8)"):d=1.8[m];[v][s][m]amix=inputs=3:normalize=0:duration=first,atrim=0:$END,loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map "[a]" -ar 44100 "$W/mix_music.wav"
ffmpeg -v error -y -i "$W/video.mp4" -c:v libx264 -preset slow -crf ${CRF:-25} -pix_fmt yuv420p "$W/video_final.mp4"
ffmpeg -v error -y -i "$W/video_final.mp4" -i "$W/mix_music.wav" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$P/final/$NAME (มีเพลง).mp4"
ffmpeg -v error -y -i "$W/video_final.mp4" -i "$W/mix_nomusic.wav" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$P/final/$NAME (ไม่มีเพลง).mp4"
PROJ="$P" python3 "$E/cover.py" "$P/final/ปก $NAME.jpg"
ls -la "$P/final"
