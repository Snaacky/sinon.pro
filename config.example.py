# A list of all blacklisted extensions to forbid from uploading.
BLACKLISTED_EXTENSIONS = ['exe', 'pdf', 'scr', 'jar', 'doc', 'docx']

# How often check_for_files_pending_removal() should be ran in minutes.
CRON_INTERVAL = 86400

# Whether or not to use Flask's debug mode.
DEBUG = False

# The file system path to the folder where uploads will be stored.
DOWNLOADS_PATH = "/your/path/here"

# How long the randomly generated file names should be.
FILENAME_LENGTH = 6

# A randomly generated key needed for Flask to work.
SECRET_KEY = "REPLACE_THIS_WITH_A_SECURELY_GENERATED_KEY"

# The port you want the web app to run on.
PORT = 13337

# Whether or not to use srm instead of the OS's remove
SECURE_REMOVAL = False

