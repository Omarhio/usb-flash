import subprocess
import numpy as np
import mss
import time

device_instance_id = r"USB\VID_XXXX&PID_YYYY"

def detect_flash(threshold=200):
    with mss.mss() as sct:
        monitor = {"top": 200, "left": 200, "width": 400, "height": 400}
        img = np.array(sct.grab(monitor))
        gray_img = np.mean(img, axis=2)
        brightness = np.mean(gray_img)
        return brightness > threshold

def enable_device(instance_id):
    try:
        result = subprocess.run(
            ["powershell", "-Command", f"Enable-PnpDevice -InstanceId '{instance_id}' -Confirm:$false"],
            capture_output=True, text=True, check=True, encoding='cp1252', errors='ignore'
        )
        print("Device enabled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable device: {e.stderr}")

def disable_device(instance_id):
    try:
        result = subprocess.run(
            ["powershell", "-Command", f"Disable-PnpDevice -InstanceId '{instance_id}' -Confirm:$false"],
            capture_output=True, text=True, check=True, encoding='cp1252', errors='ignore'
        )
        print("Device disabled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable device: {e.stderr}")

def main():
    print("En attente de la détection d'un flash...")
    flash_on = False

    while True:
        if detect_flash():
            if not flash_on:
                print("Flash détecté ! Activation du port USB...")
                enable_device(device_instance_id)
                flash_on = True
        else:
            if flash_on:
                print("Fin du flash. Désactivation du port USB...")
                disable_device(device_instance_id)
                flash_on = False

        time.sleep(0.1)

if __name__ == "__main__":
    main()
