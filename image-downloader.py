from flask import Flask, send_file, Response
import os
import subprocess
import tempfile

app = Flask(__name__)

def pull_image(image_name):
    try:
        subprocess.run(["docker", "pull", image_name], check=True)
    except subprocess.CalledProcessError as e:
        return False
    return True

@app.route('/download/<image_name>')
def download_image(image_name):
    # Create a temporary directory to hold the image
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, f"{image_name}.tar")

    # Pull the image if it's not available locally
    if pull_image(image_name) is False:
        return Response(f"Error in pulling Docker image {image_name}", status=500)

    # Save the Docker image as a tar file
    try:
        subprocess.run(["docker", "save", "-o", file_path, image_name], check=True)
    except subprocess.CalledProcessError as e:
        return Response(f"Error in saving Docker image: {e.output}", status=500)

    # Provide the tar file for download
    return send_file(file_path, as_attachment=True, download_name=f"{image_name}.tar")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
