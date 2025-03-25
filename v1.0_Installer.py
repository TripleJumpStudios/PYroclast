#!/usr/bin/env python3
"""
vkBasalt Installer / Uninstaller Script

This script detects your Linux distribution and installs or uninstalls vkBasalt.
It supports installation via:
  - System package managers (apt, dnf, pacman, xbps, eopkg)
  - AUR helpers (yay, paru) on Arch-like systems
  - Flatpak

After installation, it ensures a consistent configuration by copying the sample
config file to ~/.config/vkBasalt/vkBasalt.conf if it doesn't already exist.

Additionally, it creates necessary directories for PYroclast data:
  - ~/pyroclast/ as the main folder for PYroclast data.
  - ~/pyroclast/backupfiles/ for backing up existing vkBasalt.conf files.
  - ~/pyroclast/shaders/ for ReShade shaders.
  - ~/pyroclast/textures/ for ReShade texture files.
  - ~/pyroclast/lut/ for LUT files.

After setting up directories, the script will prompt to download shaders and textures
from GitHub (if desired).

Usage Examples:
  Install normally:
      ./vkbasalt_installer.py

  Force a distro (for testing):
      ./vkbasalt_installer.py --force-distro arch

  Uninstall vkBasalt:
      ./vkbasalt_installer.py --uninstall

  Use Flatpak:
      ./vkbasalt_installer.py --flatpak
      ./vkbasalt_installer.py --flatpak --uninstall

  Specify a custom detection path or AUR helper:
      ./vkbasalt_installer.py --custom-path /my/path --aur-helper paru

  Enable slow logging (adds a 2-second delay after each log message):
      ./vkbasalt_installer.py --slow
"""

import os
import platform
import subprocess
import shutil
import time
import argparse
import urllib.request
import zipfile
import tempfile

# Global configuration
SLOW_MODE = False
SLOW_DELAY = 2  # seconds
CUSTOM_PATH = None

# GitHub commit and URL constants
COMMIT_HASH = "a621b3f4f154e4a1ba8e07d63827e1e757a05bbd"
ZIP_URL = f"https://github.com/crosire/reshade-shaders/archive/{COMMIT_HASH}.zip"


def slow_log(message):
    """Logs a message and optionally pauses (if slow mode is enabled)."""
    print(message)
    if SLOW_MODE:
        time.sleep(SLOW_DELAY)


def detect_distro():
    """Detects the Linux distribution using /etc/os-release."""
    slow_log("Detecting Linux distribution by reading /etc/os-release...")
    distro = "unknown"
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
        info = {}
        for line in lines:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                info[key.lower()] = value.strip('"').lower()
        slow_log("Parsed /etc/os-release: " + str(info))

        if "id_like" in info:
            if "debian" in info["id_like"]:
                distro = "debian"
            elif "fedora" in info["id_like"]:
                distro = "fedora"
            elif "arch" in info["id_like"]:
                distro = "arch"
            elif "void" in info["id_like"]:
                distro = "void"
            elif "solus" in info["id_like"]:
                distro = "solus"
        if distro == "unknown" and "id" in info:
            if info["id"] in ["debian", "ubuntu", "linuxmint"]:
                distro = "debian"
            elif info["id"] in ["fedora", "centos", "rhel"]:
                distro = "fedora"
            elif info["id"] in ["arch", "manjaro", "cachyos"]:
                distro = "arch"
            elif info["id"] == "void":
                distro = "void"
            elif info["id"] == "solus":
                distro = "solus"
    except Exception as e:
        slow_log("Error reading /etc/os-release: " + str(e))
    slow_log("Determined distribution: " + distro)
    return distro


def is_vkbasalt_installed():
    """
    Checks if vkBasalt is installed by searching for its binary and known components.
    Returns True if any component is found.
    """
    slow_log("Checking if vkbasalt is installed (searching in PATH)...")
    for binary in ["vkbasalt", "vkBasalt"]:
        if shutil.which(binary):
            slow_log(f"Found binary {binary} in PATH.")
            return True

    slow_log("Not found in PATH; checking known locations...")
    found = False
    known_locations = {
        "/usr/lib/libvkbasalt.so": "Library file",
        "/usr/share/vulkan/implicit_layer.d/vkBasalt.json": "Vulkan layer config",
        "/usr/share/vkbasalt/vkBasalt.conf.example": "Example config file",
    }
    if CUSTOM_PATH:
        known_locations[CUSTOM_PATH] = "Custom provided path"
    for path, desc in known_locations.items():
        if os.path.exists(path):
            slow_log(f"Found {desc} at {path}.")
            found = True
    if found:
        slow_log("vkBasalt detected (Vulkan layer installed).")
    else:
        slow_log("vkbasalt not found in expected locations.")
    return found


def is_vkbasalt_up_to_date_with_aur(aur_helper):
    """
    Checks if the AUR-installed vkBasalt is up-to-date using the specified AUR helper.
    Returns True if the installed version matches the latest available version.
    """
    try:
        installed = subprocess.check_output([aur_helper, "-Q", "vkbasalt"]).decode().strip().split()[1]
        available_output = subprocess.check_output([aur_helper, "-Si", "vkbasalt"]).decode()
        for line in available_output.splitlines():
            if line.lower().startswith("version"):
                latest = line.split(":", 1)[1].strip()
                break
        if installed == latest:
            slow_log(f"vkbasalt is already the latest version: {installed}")
            return True
        else:
            slow_log(f"vkbasalt is outdated. Installed: {installed}, Latest: {latest}")
            return False
    except subprocess.CalledProcessError:
        return False


def install_vkbasalt(distro, use_flatpak, flatpak_pkg, aur_helper):
    """Installs vkBasalt using the appropriate method for the distro or via Flatpak."""
    if use_flatpak:
        if not shutil.which("flatpak"):
            slow_log("Flatpak is not installed. Cannot proceed with Flatpak installation.")
            return
        slow_log("Installing vkbasalt via Flatpak...")
        subprocess.run(["flatpak", "install", "--user", "--noninteractive", "flathub", flatpak_pkg], check=True)
        return

    arch_type = platform.machine()
    slow_log("System architecture detected: " + arch_type)
    if arch_type != "x86_64":
        slow_log("Only 64-bit systems are supported. Your system architecture: " + arch_type)
        return

    try:
        if distro == "debian":
            slow_log("Installing vkbasalt via apt-get...")
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "vkbasalt"], check=True)
        elif distro == "fedora":
            slow_log("Installing vkbasalt via dnf...")
            subprocess.run(["sudo", "dnf", "install", "-y", "vkbasalt"], check=True)
        elif distro == "arch":
            slow_log("Installing vkbasalt via pacman...")
            try:
                subprocess.run(["sudo", "pacman", "-Syu", "vkbasalt", "--noconfirm"], check=True)
            except subprocess.CalledProcessError:
                slow_log("Pacman did not find/update vkbasalt. Checking for an AUR helper...")
                helper_used = aur_helper if aur_helper and shutil.which(aur_helper) else None
                if not helper_used:
                    for helper in ["yay", "paru"]:
                        if shutil.which(helper):
                            helper_used = helper
                            break
                if helper_used:
                    if is_vkbasalt_up_to_date_with_aur(helper_used):
                        slow_log(f"vkbasalt is already installed and up-to-date via {helper_used}.")
                        return
                    slow_log(f"Installing/updating vkbasalt via {helper_used}...")
                    subprocess.run([helper_used, "-S", "--needed", "--noconfirm", "vkbasalt"], check=True)
                else:
                    slow_log("No AUR helper found. Please install vkbasalt manually.")
        elif distro == "void":
            slow_log("Installing vkbasalt via xbps-install...")
            subprocess.run(["sudo", "xbps-install", "-S", "vkbasalt"], check=True)
        elif distro == "solus":
            slow_log("Installing vkbasalt via eopkg...")
            subprocess.run(["sudo", "eopkg", "update"], check=True)
            subprocess.run(["sudo", "eopkg", "install", "vkbasalt"], check=True)
        else:
            slow_log("Unsupported Linux distribution. Cannot install vkbasalt automatically.")
    except subprocess.CalledProcessError as e:
        slow_log("An error occurred during installation: " + str(e))


def uninstall_vkbasalt(distro, use_flatpak, flatpak_pkg, aur_helper):
    """Uninstalls vkBasalt using the appropriate package manager or Flatpak."""
    if use_flatpak:
        if not shutil.which("flatpak"):
            slow_log("Flatpak is not installed. Cannot proceed with uninstallation.")
            return
        slow_log("Uninstalling vkbasalt via Flatpak...")
        subprocess.run(["flatpak", "uninstall", "--user", "-y", flatpak_pkg], check=True)
        return

    try:
        if distro == "debian":
            slow_log("Uninstalling vkbasalt via apt-get...")
            subprocess.run(["sudo", "apt-get", "remove", "-y", "vkbasalt"], check=True)
        elif distro == "fedora":
            slow_log("Uninstalling vkbasalt via dnf...")
            subprocess.run(["sudo", "dnf", "remove", "-y", "vkbasalt"], check=True)
        elif distro == "arch":
            slow_log("Uninstalling vkbasalt via pacman...")
            try:
                subprocess.run(["sudo", "pacman", "-Rns", "--noconfirm", "vkbasalt"], check=True)
            except subprocess.CalledProcessError:
                slow_log("Pacman removal failed. Checking for an AUR helper...")
                helper_used = aur_helper if aur_helper and shutil.which(aur_helper) else None
                if not helper_used:
                    for helper in ["yay", "paru"]:
                        if shutil.which(helper):
                            helper_used = helper
                            break
                if helper_used:
                    subprocess.run([helper_used, "-Rns", "--noconfirm", "vkbasalt"], check=True)
                else:
                    slow_log("No AUR helper found. Cannot uninstall vkbasalt automatically for Arch.")
        elif distro == "void":
            slow_log("Uninstalling vkbasalt via xbps-remove...")
            subprocess.run(["sudo", "xbps-remove", "-R", "vkbasalt"], check=True)
        elif distro == "solus":
            slow_log("Uninstalling vkbasalt via eopkg...")
            subprocess.run(["sudo", "eopkg", "remove", "vkbasalt"], check=True)
        else:
            slow_log("Unsupported Linux distribution. Cannot uninstall vkbasalt automatically.")
    except subprocess.CalledProcessError as e:
        slow_log("An error occurred during uninstallation: " + str(e))


def setup_vkbasalt_config():
    """
    Ensures the user's vkBasalt configuration exists by copying the example config
    to ~/.config/vkBasalt/vkBasalt.conf if it doesn't already exist.
    """
    config_dir = os.path.expanduser("~/.config/vkBasalt")
    config_file = os.path.join(config_dir, "vkBasalt.conf")
    example_file = "/usr/share/vkBasalt/vkBasalt.conf.example"

    if not os.path.exists(config_dir):
        slow_log(f"Creating configuration directory at {config_dir}.")
        os.makedirs(config_dir, exist_ok=True)
    else:
        slow_log(f"Configuration directory exists at {config_dir}.")

    if not os.path.exists(config_file):
        if os.path.exists(example_file):
            slow_log(f"Copying example config from {example_file} to {config_file}.")
            shutil.copy(example_file, config_file)
        else:
            slow_log(f"Example config not found at {example_file}.")
    else:
        slow_log(f"Configuration file already exists at {config_file}.")


def create_pyroclast_directories():
    """
    Creates necessary directories for PYroclast if they don't already exist:
      - ~/pyroclast/ as the main folder for PYroclast data.
      - ~/pyroclast/backupfiles/ for backing up existing vkBasalt.conf files.
      - ~/pyroclast/shaders/ for ReShade shaders.
      - ~/pyroclast/textures/ for ReShade texture files.
      - ~/pyroclast/lut/ for LUT files.
    """
    pyroclast_main = os.path.expanduser("~/pyroclast")
    backup_dir = os.path.join(pyroclast_main, "backupfiles")
    shaders_dir = os.path.join(pyroclast_main, "shaders")
    textures_dir = os.path.join(pyroclast_main, "textures")
    lut_dir = os.path.join(pyroclast_main, "lut")

    directories = [pyroclast_main, backup_dir, shaders_dir, textures_dir, lut_dir]
    for directory in directories:
        if not os.path.exists(directory):
            slow_log(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
        else:
            slow_log(f"Directory already exists: {directory}")


def download_and_extract_zip(url, extract_to):
    """
    Downloads a ZIP archive from the given URL and extracts its contents to the specified directory.
    """
    slow_log(f"Downloading from {url} ...")
    zip_path = os.path.join(extract_to, "download.zip")
    urllib.request.urlretrieve(url, zip_path)
    slow_log("Download complete. Extracting...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_path)
    slow_log("Extraction complete.")


def copy_directory(src, dst):
    """
    Copies the contents of the source directory to the destination directory.
    Uses shutil.copytree with dirs_exist_ok=True (requires Python 3.8+).
    """
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        slow_log(f"Copied contents from {src} to {dst}.")
    else:
        slow_log(f"Source directory {src} not found.")


def prompt_and_download_assets():
    """
    Prompts the user whether they want to download shaders and/or textures from GitHub.
    Downloads the reshade-shaders ZIP archive and copies the requested directories into their targets.
    """
    shaders_choice = input("Download shaders from GitHub? (Y/N): ").strip().lower()
    textures_choice = input("Download textures from GitHub? (Y/N): ").strip().lower()

    download_shaders = shaders_choice.startswith("y")
    download_textures = textures_choice.startswith("y")

    if not download_shaders and not download_textures:
        slow_log("Skipping download of shaders and textures.")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        download_and_extract_zip(ZIP_URL, temp_dir)
        extracted_folder = os.path.join(temp_dir, f"reshade-shaders-{COMMIT_HASH}")

        if download_shaders:
            src_shaders = os.path.join(extracted_folder, "Shaders")
            dst_shaders = os.path.expanduser("~/pyroclast/shaders")
            slow_log(f"Copying shaders from {src_shaders} to {dst_shaders}...")
            copy_directory(src_shaders, dst_shaders)

        if download_textures:
            src_textures = os.path.join(extracted_folder, "Textures")
            dst_textures = os.path.expanduser("~/pyroclast/textures")
            slow_log(f"Copying textures from {src_textures} to {dst_textures}...")
            copy_directory(src_textures, dst_textures)


def main():
    global SLOW_MODE, CUSTOM_PATH

    parser = argparse.ArgumentParser(description="vkBasalt installer/uninstaller script.")
    parser.add_argument("--slow", "-s", action="store_true", help="Enable slow logging mode")
    parser.add_argument("--force-distro", help="Force the distribution value (e.g., debian, fedora, arch, void, solus)")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall vkBasalt instead of installing")
    parser.add_argument("--flatpak", action="store_true", help="Use Flatpak for installation/uninstallation")
    parser.add_argument("--flatpak-pkg", default="org.vkbasalt.vkbasalt",
                        help="Flatpak package ID (default: org.vkbasalt.vkbasalt)")
    parser.add_argument("--custom-path", help="Custom path to check for vkBasalt installation")
    parser.add_argument("--aur-helper", default="", help="Specify AUR helper (default: try yay then paru)")
    args = parser.parse_args()

    SLOW_MODE = args.slow
    if SLOW_MODE:
        slow_log("Slow logging mode enabled.")
    else:
        slow_log("Normal logging mode.")

    if args.custom_path:
        CUSTOM_PATH = args.custom_path
        slow_log("Using custom detection path: " + CUSTOM_PATH)

    distro = detect_distro()
    if args.force_distro:
        distro = args.force_distro.lower()
        slow_log("Overriding detected distro with: " + distro)
    slow_log("Detected distribution: " + distro)

    if args.uninstall:
        slow_log("Uninstall mode activated.")
        uninstall_vkbasalt(distro, args.flatpak, args.flatpak_pkg, args.aur_helper)
        return

    if is_vkbasalt_installed():
        if distro == "arch" and args.aur_helper:
            if is_vkbasalt_up_to_date_with_aur(args.aur_helper):
                slow_log("vkBasalt is installed and up-to-date. Skipping installation.")
                setup_vkbasalt_config()
                create_pyroclast_directories()
                prompt_and_download_assets()
                return
        else:
            slow_log("vkBasalt is already installed. Skipping installation.")
            setup_vkbasalt_config()
            create_pyroclast_directories()
            prompt_and_download_assets()
            return

    slow_log("vkBasalt is not installed or is outdated. Proceeding with installation...")
    install_vkbasalt(distro, args.flatpak, args.flatpak_pkg, args.aur_helper)
    setup_vkbasalt_config()
    create_pyroclast_directories()
    prompt_and_download_assets()


if __name__ == "__main__":
    main()
