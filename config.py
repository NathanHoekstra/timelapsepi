# take.py config file
config = {}

# ---- Base settings ----
config['base_path'] = '/pictures'
config['enable_annotation'] = True


# ---- Time settings  ----
config['am'] = 400
config['pm'] = 2100
config['delay'] = 180

# ---- Raspistill image settings ----
config['flip_horizontal'] = False
config['flip_vertical'] = False
config['width'] = 1920 #Max width is 3280 pixels
config['height'] = 1080 #Max height is 2464 pixels
config['quality'] = 35 # Set JPEG quality default is 35, range 0-100

# ----- Annotation settings
config['annotation_text'] = '(c) N.Hoekstra'
