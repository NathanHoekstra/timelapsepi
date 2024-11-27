# take.py config file
config = {}

# ---- Base settings ----
config['base_path'] = '/pictures'   # Base path to store the images
config['enable_annotation'] = True  # Enable annotation of the images

# ----- Annotation settings ----
config['annotation_text'] = '(C) N.Hoekstra'    # Optional, adds text on the bottom-left of the image

# ---- OpenWeatherAPI settings ----
config['use_openweather'] = False       # Use openweather API to get unrise/sunset times (am/pm setting)
config['openweather'] = {}
config['openweather']['api_key'] = ""   # Set openweather API key
config['openweather']['city']    = ""   # Set city name

# ---- Time settings  ----
config['am']    = 800   # Start time to take pictures (ignored if use_openweather = True)
config['pm']    = 1900  # End time to take pictures  (ignored if use_openweather = True)
config['delay'] = 120   # Delay in seconds between pictures

# ---- Picamera2 image settings ----
config['flip_horizontal'] = False   # Flip the screen on the horizontal axis
config['flip_vertical']   = False   # Flip the screen on the vertical axis
config['width']   = 4608    # Max width is 4608 pixels (for v2 = 3280)
config['height']  = 2592    # Max height is 2592 pixels (for v2 = 2464)
config['quality'] = 90      # Set JPEG quality default is 90, range 0-95

# ---- Logfile settings ----
config['logfile'] = {}
config['logfile']['maxsize']     = 5 * 1000 # Max logfile size in bytes (Default = 5 KB)
config['logfile']['backupcount'] = 5        # Amount of logfiles to keep
