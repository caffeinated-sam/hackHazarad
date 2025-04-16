import subprocess
import os

def main():
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("❌ requirements.txt not found.")
        return

    print("📦 Installing packages from requirements.txt...\n")

    try:
        subprocess.check_call(["pip", "install", "-r", requirements_file])
        print("✅ All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")

if __name__ == '__main__':
    main()
