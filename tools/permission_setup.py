import os
import sys
import platform
import subprocess


def set_permissions_unix(path):
    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            try:
                os.chmod(full_path, 0o777)
            except Exception as e:
                print(f"Failed to set permissions for {full_path}: {e}")
    try:
        os.chmod(path, 0o777)
    except Exception as e:
        print(f"Failed to set permissions for {path}: {e}")

def set_permissions_windows(path):
    for root, dirs, files in os.walk(path):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            try:
                subprocess.run([
                    'icacls', full_path, '/grant', 'Everyone:F', '/T', '/C'
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                print(f"Failed to set permissions for {full_path}: {e}")
    try:
        subprocess.run([
            'icacls', path, '/grant', 'Everyone:F', '/T', '/C'
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Failed to set permissions for {path}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python permission_setup.py <folder_path>")
        sys.exit(1)
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        sys.exit(1)
    if platform.system() == 'Windows':
        set_permissions_windows(folder_path)
    else:
        set_permissions_unix(folder_path)
    print("Permissions set successfully.")

if __name__ == "__main__":
    main()

