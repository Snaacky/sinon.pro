import os
import random
import string
import subprocess
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, redirect, render_template, request, send_file

import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY


def check_for_files_pending_removal():
    """ 
    Called via a scheduler, iterates over files in the downloads folder, 
    checks if any are more than 24 hours old, removes any that are.
    """
    if len(os.listdir(config.DOWNLOADS_PATH)) > 0:  # Needed or the next line will throw an exception if empty.
        for file in os.listdir(config.DOWNLOADS_PATH):
            if int(time.time()) - 86400 >= int(os.path.getmtime(os.path.join(config.DOWNLOADS_PATH, file))):
                if config.SECURE_REMOVAL:
                    subprocess.call(["srm", os.path.join(config.DOWNLOADS_PATH, file)])
                else:
                    os.remove(os.path.join(config.DOWNLOADS_PATH, file))


@app.route("/")
def index():
    """
    Serves the file upload template.
    """
    return render_template("index.html")


@app.route("/dl/<file>")
def download(file):
    """ 
    Serves the requested file.
    Returns HTTP status code 404 if the file cannot be found.
    """
    if os.path.isfile(os.path.join(config.DOWNLOADS_PATH, file)):
        if ".htm" or ".html" in file:  # Serve as plain text to prevent phishing pages.
            return send_file(os.path.join(config.DOWNLOADS_PATH, file), mimetype="text/plain")
        else:
            return send_file(os.path.join(config.DOWNLOADS_PATH, file))
    else:
        return render_template("404.html"), 404


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Serves the endpoint where users upload their files.
    
    Returns HTTP status code 200 and plain text containing 
    a link to the file on successful upload.
    
    Returns HTTP status codes 400, 403, or 405
    and an error message depending on the issue.
    """
    # User accessed endpoint via GET request instead of POST.
    if request.method == "GET":
        return("Files must be uploaded via POST request.", 405)

    elif request.method == "POST":
        # User sent a POST request but it did not contain a file
        if "file" not in request.files:
            return("An error occurred while processing your upload. Please try again.", 400)
        
        file = request.files["file"]
        
        # User either didn't send a file or the name was blank
        if file.filename == "":
            return("An error occurred while processing your upload. Please try again.", 400)

        # User attempted to upload a file with a blacklisted extension
        if file and file.filename.split(".")[1].lower() in config.BLACKLISTED_EXTENSIONS:
            return("That file extension is not allowed.", 403)
        
        # User uploaded a valid file
        if file:
            # Generate new filename for simplicity and to avoid name conflicts
            random_name = "".join(random.choice(string.ascii_letters) for char in range(config.FILENAME_LENGTH))
            extension = file.filename.split(".")[-1].lower()
            new_name = random_name + "." + extension
            file.save(os.path.join(config.DOWNLOADS_PATH, new_name))
            return(f"{request.url_root}{config.DOWNLOADS_PATH}{new_name}")


@app.errorhandler(404)
def file_not_found(error_code):
    """
    Serves the 404 template and status when the requested file can't be found.
    """
    return render_template('404.html'), 404


"""
Sets up the scheduler to run the function that clears the downloads folder
based on the cron interval set in the config file.
"""
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(check_for_files_pending_removal, "interval", minutes=config.CRON_INTERVAL)
scheduler.start()


if __name__ == "__main__":
    app.run(debug=config.DEBUG, port=config.PORT)
