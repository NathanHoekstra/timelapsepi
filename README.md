# TimelapsePi
A timelapse application written in Python3 for the Raspberry Pi.

## Usage
1. Install ImageMagick using `sudo apt install -y imagemagick` this is used for the annotation.
2. Edit `config.py` to adjust base directory and if necessary change resolution.
3. Use `python3 take.py` to run it, add `&` to run it in the background.

**NOTE:** Install the Picamera2 library when using a Raspberry Pi Lite image:
`sudo apt install -y python3-picamera2 --no-install-recommends`

## TODO
- [x] Use f-string instead of the 'old' string concatenation.
- [x] Add support for Raspberry Pi Camera Module 3.
- [x] Use openweathermap API for the sunrise/sunset config.
- [ ] Setup Systemd service file.
- [ ] Move to a .ini file for application configuration.
- [ ] Create installer/uninstaller script.
- [ ] Modify picture annotation with more config options.
