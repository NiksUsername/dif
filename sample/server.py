from flask import Flask, request, render_template
import subprocess
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form['message']
    logging.info(f"User submitted message: {message}")  # Log the user's input
    command = f"echo '{message}' | gpg --encrypt --recipient 'test' --armor --output - --trust-model always --no-tty"
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )

        encrypted_message = result.stdout
        return render_template('result.html', encrypted_message=encrypted_message)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during encryption for message '{message}': {e}") # Log the error
        logging.error(e.stderr)
        error_message = f"Error during encryption: {e}"
        return render_template('result.html', error_message=error_message)
    except FileNotFoundError:
        logging.error("Error: 'pgp' command not found.") # Log if pgp is not found
        error_message = "Error: 'pgp' command not found. Please ensure it is installed and in your system's PATH."
        return render_template('result.html', error_message=error_message)

if __name__ == '__main__':
    # Create a dummy public key for 'test' if it doesn't exist
    # This is for simplicity and should NOT be done in a real scenario
    if not os.path.exists(os.path.expanduser('~/.gnupg')):
        os.makedirs(os.path.expanduser('~/.gnupg'))
    try:
        subprocess.run("gpg --list-keys 'test'", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        subprocess.run("gpg --batch --gen-key --no-tty <<< $(echo -e 'Key-Type: RSA\nKey-Length: 2048\nSubkey-Type: RSA\nSubkey-Length: 2048\nName-Real: test\nName-Email: test@example.com\nExpire-Date: 0\n%commit\n')", shell=True, check=False)

    app.run(debug=True, host='0.0.0.0')