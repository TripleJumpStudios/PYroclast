# PYroclast

<br style="clear: both;" />

<table>
  <tr valign="middle">
    <td>
      <img src="https://raw.githubusercontent.com/TripleJumpStudios/PYroclast/f56ac72672bc6656973f1c27382510cc9de0d358/icon.png" 
           alt="PYroclast Icon" 
           width="100" />
    </td>
    <td>
      An AppImage-based configuration manager for the `vkBasalt.conf` files used by
      <a href="https://github.com/DadSchoorse/vkBasalt">vkBasalt</a>, a Vulkan post-processing layer
      for Linux similar to ReShade on Windows.
    </td>
  </tr>
</table>

<br style="clear: both;" />

## Planned Features

1. **Automatic Dependency Checks and Installation**  
   Ensures that all vkBasalt-required libraries and tools are installed or prompts you to install them.

2. **Directory and File Path Management**  
   Lets you easily set custom paths (for example, shader files or LUT directories) in a single interface, reducing guesswork.

3. **Intuitive UI**  
   Provides a user-friendly graphical interface for configuring vkBasalt, eliminating the need for manual editing of `vkBasalt.conf` files.

4. **Integration with `.desktop` Files for Separate `vkBasalt.conf` Files**  
   Automatically modifies `.desktop` files so each game or application can have its own dedicated vkBasalt configuration.

5. **AppImage Packaging**  
   Distributes PYroclast as an AppImage for easy installation and broad compatibility across various Linux distributions.

6. **Integration with ReShade FX Shaders**  
   Allows you to reference and enable ReShade `.fx` files for enhanced post-processing effects.

7. **Integration with 3D LUT Files**  
   Lets you specify custom 3D LUTs for color grading or other advanced visual modifications.

## Long-Term Features and Wish List

1. **Installation via [AppImage Package Manager](https://github.com/ivan-hc/AM).**  

2. **Integration with Lutris, Heroic, Steam, and Other Platforms.**  
   Automates setup so vkBasalt configurations can be seamlessly used across popular gaming platforms and launchers.

3. **Custom File Names.**  
   Allows users to specify filenames other than `vkBasalt.conf` for configurations while still ensuring vkBasalt can detect and load them.

## What PYroclast Will Not Do (At This Time or Possibly Ever)

- **Update the `vkBasalt.conf` file on the fly (while a game or program is running).**  
  Because vkBasalt (and Vulkan in general) loads and applies post-processing during the startup phase, attempting to modify those settings mid-session often does not take effect or can cause crashes or instability.

- **Perform Real-Time In-Game Overlays.**  
  PYroclast is only a configuration manager; it does not hook or inject any overlay UI into running games.

- **Provide Direct Troubleshooting of Vulkan or Driver Issues.**  
  It will not fix Vulkan or driver compatibility problems beyond what is already handled by vkBasalt.

- **Offer Full ReShade-Style Effect Authoring.**  
  PYroclast can point to ReShade FX shaders, but it does not include a shader-authoring environment or advanced editing features.

## How PYroclast Works

1. **Install the AppImage.**  
   - Download the PYroclast AppImage and make it executable (for example, `chmod +x PYroclast.AppImage`). 
   - Run the file to start the application.

2. **Dependency Checks.**  
   - On first launch, PYroclast checks whether your system meets vkBasalt’s requirements.
   - If certain dependencies are missing, or if vkBasalt itself is not installed, you will be prompted to allow PYroclast to install them or install them manually.

3. **Directory Setup.**  
   - Next, PYroclast asks where you want to keep your vkBasalt-related directories (for shaders, 3D LUT files, and so on).
   - **No file is created or modified without user input**—PYroclast always confirms before making or updating anything.

4. **Directory Creation.**  
   - If you approve, PYroclast automatically creates or populates these folders:
     - `~/.config/vkBasalt/` for vkBasalt’s main `vkBasalt.conf` configuration file (if not already present).
     - `~/pyroclast/` as a main folder for PYroclast-specific data.
     - `~/pyroclast/backupfiles/` to hold backups of existing `vkBasalt.conf` files before modifications.
     - `~/pyroclast/shaders/` and `~/pyroclast/lut/` for storing optional ReShade `.fx` shaders and LUT files.

5. **Configuration & Backups.**  
   - When you create a `vkBasalt.conf` or update the file, PYroclast checks for an existing `~/.config/vkBasalt/vkBasalt.conf`. If found, it copies that file to `~/pyroclast/backupfiles/<timestamp>_vkBasalt.conf`. It then writes the corresponding settings to a new `~/.config/vkBasalt/vkBasalt.conf`. This way, you can always restore or compare older versions.

6. **Interaction with `.desktop` Files and Game Directories.**  
   - You can choose to update `.desktop` files for separate vkBasalt configs per game or app. However, keep in mind that if a `~/.config/vkBasalt/vkBasalt.conf` file exists, it can override configs in `.desktop` files or game/app folders.
   - Native Linux games can also have `vkBasalt.conf` in their working directory. You can point PYroclast to that location or rely on the default `~/.config/vkBasalt/`. A `~/.config/vkBasalt/vkBasalt.conf` file will also override this.

7. **Launch & Manage.**  
   - Once everything is set up, your system is ready to apply vkBasalt post-processing whenever you launch a Vulkan application.
   - If you want to change LUT files, custom shaders, or other settings later, PYroclast will prompt you to back up or overwrite your configuration files.

## Installer Script (v1.1_Installer.py)

PYroclast ships with a helper script that automates installing or uninstalling vkBasalt, creates the needed directories, and optionally downloads shaders and textures:

1. **Automatic Distribution Detection.**  
   - The script reads `/etc/os-release` to identify whether your system is Debian/Ubuntu, Fedora, Arch, Void, Solus, or openSUSE.

2. **Package Manager Integration.**  
   - Once it knows your distro, the script installs vkBasalt from the appropriate repository:
     - **Debian/Ubuntu**: `apt-get`
     - **Fedora**: `dnf`
     - **Arch**: `pacman` first; if it fails, tries an AUR helper (i.e. `yay` or `paru`)   
         **note**: Currently, there is no official package for vkBasalt on Arch.
     - **Void**: `xbps-install`
     - **Solus**: `eopkg`
     - **openSUSE**: `zypper`  
         **note**: Still untested, but the functionality is built in.
   - **Arch-Specific Check**: If no C compiler is found on Arch-based systems, the script aborts and instructs you to install `base-devel`.

3. **Optional Shaders and Textures.**  
   - If you approve, the script downloads ReShade shader and texture files from the [GitHub](https://github.com/crosire/reshade-shaders/tree/slim) and places them into `~/pyroclast/shaders/` and `~/pyroclast/textures/`.  
     **Note**: This is currently set to the slim branch.
   - This step is entirely optional—you can skip it by typing “N” when prompted.

4. **Directory Creation.**  
   - The script automatically sets up:
     - `~/.config/vkBasalt/` for the main `vkBasalt.conf`
     - `~/pyroclast/` as the main folder for PYroclast data
     - `~/pyroclast/backupfiles/` for storing backups of any `vkBasalt.conf` file you already had
     - `~/pyroclast/shaders/` and `~/pyroclast/lut/` for your future expansions

5. **Uninstall Mode.**  
   - Running `./v1.1_Installer.py --uninstall` attempts to remove vkBasalt using the same package manager logic.
   - If you installed vkBasalt manually or from outside the script’s recognized sources, it may not detect or remove it fully.

6. **Advanced Usage.**  
   - **`--custom-path /my/custom/path`**: Lets you specify a custom location to look for vkBasalt files.  
   - **`--aur-helper <yay|paru>`**: Sets which AUR helper to use on Arch if `pacman` does not find vkBasalt. (example ./v1.1_Installer.py --aur-helper yay) 
   - **`--slow`**: Adds a delay after each log message (useful for debugging or demonstrations).
  
7. **Tested Distros**  
   - **If there is a distro you would like tested, please let me know.**
     -  Fedora 41
     -  Nobara 41
     -  POP!_OS
     -  CachyOS
     -  Manjaro
     -  EndeavourOS
     -  Solus
     -  Void

8. **Testing the script**
    - Download the v1.1_Installer.py and move it to the preferred directory.
    - In a terminal make it executable `chmod +x v1.1_Installer.py`
    - In the same terminal run it `./v1.1_Installer.py`
    - Optionally add -s for slow mode `./v1.1_Installer.py -s`
    - Copy and paste the terminal/logs and send them to me if there are any problems.
    - If you have questions, suggestions, or issues, feel free to [open an issue](https://github.com/TripleJumpStudios/PYroclast/issues) or email me at [TripleJumpStudios@proton.me](mailto:TripleJumpStudios@proton.me)

## Reminders

- Set a custom keybind to toggle vkBasalt on or off. The default is `HOME`.
- vkBasalt will only detect and apply settings if the file is named `vkBasalt.conf`. Adding extra characters to the name will make the file undetectable. Custom filenames may come in the future.
- vkBasalt will ALWAYS detect if there is a file in `~/.config/vkBasalt/vkBasalt.conf`. If you launch a game with `ENABLE_VKBASALT=1` set, vkBasalt will attempt to activate. If your game is crashing and you do not know why, check that vkBasalt is not globally enabled.
- [GOverlay](https://github.com/benjamimgois/goverlay) can display the status of vkBasalt (as of version 1.3 or later). You can find it in GOverlay under **Extras** > **Options** > **VKbasalt**.
- Refer to [vkBasalt/README.md](https://github.com/DadSchoorse/vkBasalt/blob/master/README.md) for more information on how vkBasalt works.
- vkBasalt is only compatible with Vulkan. It has no effect on DX11 or DX12 games.

## Transparency

PYroclast modifies only the directories and files that you explicitly configure or enable. Specifically, it:
- Reads and writes to the `.config/vkBasalt.conf` file (or the path you specify).  
- Reads and writes to `.desktop` files if you opt to have separate vkBasalt configs per game or application.  
- Optionally manages directories containing ReShade FX shaders or 3D LUT files if you enable those features.  
- Does **not** collect or transmit any personal data or system information.  
- Avoids altering other system files outside the scope of vkBasalt configuration.

## Why Is It Called PYroclast?

It continues the joke: Vulkan post-processing → after Vulkan → basalt → pyroclast.

<img src="https://raw.githubusercontent.com/TripleJumpStudios/PYroclast/f56ac72672bc6656973f1c27382510cc9de0d358/icon.png" alt="PYroclast Icon" width="25" />

<!-- extras and thoughts
# vkmark is a vulkan benchmark tool
# GOverlay is recommended for monitoring vkBasalt
# Build out links to great .fx files and LUT files as needed
-->
Added new sections for installer script and tested distros that it works on.
