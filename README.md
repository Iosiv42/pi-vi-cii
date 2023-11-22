# PI VI CII (more precisely Python Video Ascii)
/pʰaɪ vɪ kʰiː/ is a Python script to play videos in terminal.
At now, tested only on Linux and probably can run of Unix-like systems.

# Requirements
* ffmpeg
* mediainfo

# Potential risks
Output of other programs can be corrupted (e.g. there'll be no lineb breaks) if
you'll interrupt program execution.

# How to use
```bash
$ python path/to/src/pi_vi_cii.py path/to/video
```

Example:
```bash
$ python src/pi_vi_cii.py tests/bad-apple.mp4
```

If path to video contains spaces of special chars. that need to be escaped,
then wrap it into double quotes. It's probably argparse brain farts...
