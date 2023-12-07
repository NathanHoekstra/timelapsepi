# take.py config file
config = {}

# ---- Base settings ----
config['base_path'] = '/pictures'
config['enable_annotation'] = True


# ---- Time settings  ----
config['am'] = 600 # Start time to take pictures
config['pm'] = 1900 # End time to take pictures
config['delay'] = 120 # Delay in seconds between pictures

# ---- Raspistill image settings ----
config['flip_horizontal'] = False
config['flip_vertical'] = False
config['width'] = 3200 # Max width is 3280 pixels
config['height'] = 1800 # Max height is 2464 pixels
config['quality'] = 50 # Set JPEG quality default is 35, range 0-100

# ----- Annotation settings
config['annotation_text'] = '(C) N.Hoekstra'
