# PI VI CII (more precisely Python Video Ascii)
/pʰaɪ vɪ kʰiː/ is a Python script to play videos in terminal.
At now, tested only on Linux and probably can run of Unix-like systems.

# Installation
Merely install as python module:
```sh
$ python -m pip install .
```

# Requirements
* ffmpeg
* mediainfo

# How to use
```sh
$ pi-vi-cii path/to/video
```

Example:
```sh
$ pi-vi-cii bad-apple.mp4
```

# Improving user experience
Script based on that terminal cell aspect ratio (width/height) is ~½. So,
it's blindingly recommended to use such fonts (btw, I use Perfect DOS VGA
437 Win). It's obviously, but set terminal colors such that selected text
is white, normal is white, and background is black.
