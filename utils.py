#!/usr/bin/env python
from pyechonest import track
from scikits import audiolab
from collections import OrderedDict
import echonestconfig

pitches = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def pitches_to_keys(seg_pitches, min_confidence=0.8):
    return OrderedDict(sorted(((k,v) for k,v in zip(pitches, seg_pitches) if v>min_confidence), key=lambda x:-x[1]))

def isegments(t, min_confidence=0.8):
    for seg in t.segments:
        seg["end"] = seg["start"] + seg["duration"]
        seg["keys"] = pitches_to_keys(seg["pitches"], min_confidence=min_confidence)
        yield seg

def iproperty(t, field="timbre"):
    for seg in t.segments:
        yield seg.get(field, None)

def play_segment(segment):
    audiolab.play(segment["raw"].mean(axis=1))

def track_with_file(filename, mp3=None, track_id=None):
    if track_id:
        nest_track = track.track_from_id(track_id)
    else:
        nest_track = track.track_from_filename(mp3 or filename)
    audio_track = audiolab.Sndfile(filename)
    nest_track.samplerate = rate = audio_track.samplerate
    nest_track.nframes = audio_track.nframes
    cur_frame = 0
    for seg in nest_track.segments:
        num_frames = rate * seg["duration"]
        if cur_frame != seg["start"] * rate:
            num_frames += seg["start"] * rate - cur_frame
        if cur_frame + num_frames > audio_track.nframes:
            num_frames = audio_track.nframes - cur_frame
        seg["raw"] = audio_track.read_frames(num_frames)
        cur_frame += num_frames
    return nest_track

if __name__ == "__main__":
    chad = track.track_from_id(u'TRP8KVE11BC6E02570') #Chad VanGaalen - Willow Tree

    #print "%s - %s"%(chad.artist, chad.title)
    for seg in isegments(chad,min_confidence=0.85):
        #print "[%7.2f -> %7.2f] %s"%(seg["start"], seg["end"], seg["keys"])
        print """<span  data-start="%0.2f" data-stop="%0.2f">%s</span>"""%(seg["start"], seg["end"], ", ".join(seg["keys"].keys()))
