# TimelapsePi
A timelapse application written in Python3 for the Raspberry Pi.

## Usage
1. Install ImageMagick using ```sudo apt-get install imagemagick -y``` this is used for the annotation.
2. Edit config.py to adjust base directory and if necessary change resolution.
3. Use ```python3 take.py``` to run it, add ```&``` to run it in the background.

## TODO

- [x] Use f-string instead of the 'old' string concatenation.
- [x] Add support for Raspberry Pi Camera Module 3.
- [x] Use openweathermap API for the sunrise/sunset config.
- [ ] Modify picture annotation with more config options.
