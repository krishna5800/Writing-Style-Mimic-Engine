import pkg_resources

required_packages = {
    'flask': '2.0.1',
    'flask-cors': '3.0.10',
    'numpy': '1.21.2',
    'scikit-learn': '0.24.2',
    'python-dotenv': '0.19.0',
    'gunicorn': '20.1.0'
}

def check_packages():
    missing_packages = []
    wrong_version_packages = []
    
    for package, version in required_packages.items():
        try:
            installed_version = pkg_resources.get_distribution(package).version
            if installed_version != version:
                wrong_version_packages.append(
                    f"{package} (required: {version}, installed: {installed_version})"
                )
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
    
    if not missing_packages and not wrong_version_packages:
        print("All packages are installed with the correct versions!")
        return True
    else:
        if missing_packages:
            print("Missing packages:")
            for pkg in missing_packages:
                print(f"- {pkg}")
        
        if wrong_version_packages:
            print("\nPackages with wrong versions:")
            for pkg in wrong_version_packages:
                print(f"- {pkg}")
        
        print("\nPlease install the correct versions of the missing or incorrect packages.")
        return False

if __name__ == '__main__':
    check_packages()