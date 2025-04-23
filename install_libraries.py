import subprocess
import sys

def install_packages():
    required_packages = [
        'flask==2.0.1',
        'flask-cors==3.0.10',
        'numpy==1.21.2',
        'scikit-learn==0.24.2',
        'python-dotenv==0.19.0',
        'gunicorn==20.1.0'
    ]
    
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")

if __name__ == '__main__':
    install_packages()
    print("\nAll required libraries have been installed. You can now run the application.")