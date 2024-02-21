# take.py config file
config = {}

# ---- Base settings ----
config['base_path'] = '/pictures'
config['enable_annotation'] = True


# ---- Time settings  ----
config['am'] = 800 # Start time to take pictures
config['pm'] = 1900 # End time to take pictures
config['delay'] = 120 # Delay in seconds between pictures

# ---- Picamera2 image settings ----
config['flip_horizontal'] = False
config['flip_vertical'] = False
config['width'] = 4608 # Max width is 4608 pixels (for v2 = 3280)
config['height'] = 2592 # Max height is 2592 pixels (for v2 = 2464)
config['quality'] = 90 # Set JPEG quality default is 90, range 0-95

# ----- Annotation settings
config['annotation_text'] = '(C) N.Hoekstra'
