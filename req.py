import subprocess

def install_requirements(file_path='requirements.txt'):
    try:
        subprocess.check_call(['pip', 'install', '-r', file_path])
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if name == 'main':
    install_requirements()
