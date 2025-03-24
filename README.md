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
   Lets you easily set custom paths (e.g., for shader files, LUT directories) in a single interface, reducing guesswork.

3. **Intuitive UI**  
   Provides a user-friendly graphical interface for configuring vkBasalt, no need for manual editing of `vkBasalt.conf` files needed.

4. **Integration with `.desktop` Files for Separate `vkBasalt.conf` Files**  
   Automatically modifies `.desktop` files so each game or application can have its own dedicated vkBasalt configuration.

5. **AppImage Packaging**  
   Distributes PYroclast as an AppImage for easy installation and broad compatibility across various Linux distributions.

6. **Integration with ReShade FX Shaders**  
   Allows you to reference and enable ReShade `.fx` files for enhanced post-processing effects.

7. **Integration with 3D LUT Files**  
   Lets you specify custom 3D LUTs for color grading or other advanced visual modifications.
   
## Long-Term Features and Wish List

1. **Installation via [AppImage Package Manager](https://github.com/ivan-hc/AM)**  

2. **Integration with Lutris, Heroic, Steam, and Other Platforms**  
   Automates setup so vkBasalt configurations can be seamlessly used across popular gaming platforms and launchers.

3. **Custom File Names**  
   Allow users to specify filenames other than `vkBasalt.conf` for configurations while still ensuring vkBasalt can detect and load them.


## What PYroclast Will Not Do (At This Time or Possibly Ever)

- **Update the `vkBasalt.conf` file on the fly (while a game or program is running)**  
  Because vkBasalt (and Vulkan in general) loads and applies post-processing during the startup phase, 
  attempting to modify those settings mid-session often does not take effect or can cause crashes or instability.

- **Perform Real-Time In-Game Overlays**  
  PYroclast is only a configuration manager; it doesn't hook or inject any overlay UI into running games.

- **Provide Direct Troubleshooting of Vulkan or Driver Issues**  
  It won’t fix Vulkan/driver compatibility problems beyond what’s already handled by vkBasalt.

- **Offer Full ReShade-Style Effect Authoring**  
  PYroclast can point to ReShade FX shaders, but it doesn’t include a shader-authoring environment or advanced editing features.

## How PYroclast Works

1. **Install the AppImage**  
   - Download the PYroclast AppImage and make it executable (for example, `chmod +x PYroclast.AppImage`). 
   - Run the file to start the application.

2. **Dependency Checks**  
   - On first launch, PYroclast checks whether your system meets vkBasalt’s requirements.
   - If certain dependencies are missing, or if vkBasalt itself isn’t installed, you’ll be prompted to allow PYroclast to install them **or** you will need to install them manually.

3. **Directory Setup**  
   - Next, PYroclast asks where you want to keep your vkBasalt-related directories (for shaders, 3D LUT files, etc.).
   - **No file is created or modified without user input** — PYroclast will always confirm before making or updating anything.

4. **Directory Creation**  
   - If you approve, PYroclast will automatically create or populate these folders:
     - `~/.config/vkBasalt/` for vkBasalt’s main `vkBasalt.conf` configuration file (if not already present).
     - `~/pyroclast/` as a main folder for PYroclast-specific data.
     - `~/pyroclast/backupfiles/` to hold backups of existing `vkBasalt.conf` files before modifications.
     - `~/pyroclast/shaders/` and `~/pyroclast/lut/` for storing optional ReShade `.fx` shaders 
       and LUT files.

5. **Configuration & Backups**  
   - When you create a `vkBasalt.conf` or update the file, PYroclast checks for a file in `~/.config/vkBasalt/vkBasalt.conf`. If there is one it will copy it to `~/pyroclast/backupfiles/<timestamp>_vkBasalt.conf`. It then writes the corresponding settings to a new `~/.config/vkBasalt/vkBasalt.conf` file. This way, you can always restore or compare older versions.

6. **Interaction with `.desktop` Files and Game Directories**  
   - You can also choose to update `.desktop` files for separate vkBasalt configs per game or app. However, keep in mind that 
     if a `~/.config/vkBasalt/vkBasalt.conf` file exists, it can override configs found in `.desktop` files or game/app folders.
   - Native Linux games also allow `vkBasalt.conf` files in their working directory. You can point PYroclast to 
     that location or rely on the default `~/.config/vkBasalt/`. A `~/.config/vkBasalt/vkBasalt.conf` file will also override this.

7. **Launch & Manage**  
   - Once everything is set up, your system is ready to apply vkBasalt post-processing whenever you launch a Vulkan application.
   - If you want to change the vkBasalt.conf LUT files, custom shaders, or other settings later, PYroclast will prompt you to make a backup file to `~/pyroclast/backupfiles/` or overwrite where you are saving it to.

## Reminders
- Set a custom keybind to toggle vkBasalt on/off. The default is `HOME`
- vkBasalt will only detect and apply settings if the file is named `vkBasalt.conf`. Adding any extra characters to the name will make the file undetectable. I may look into enabling custom filenames later, but I've already expanded the scope considerably.
- vkBasalt will ALWAYS detect if there is a file in `~/.config/vkBasalt/vkBasalt.conf` If you launch a game with `ENABLE_VKBASALT=1` set, vkBasalt will attempt to activate. So if your game is crashing and you do not know why, check that vkBasalt is not globally enabled.
- [GOverlay](https://github.com/benjamimgois/goverlay) has an option to display the status of vkBasalt (currently in v1.3 at least). You can find it on the GOverlay app at Extras > Options > VKbasalt. 
- Refer to [vkBasalt/README.md](https://github.com/DadSchoorse/vkBasalt/blob/master/README.md) for more information on how vkBasalt works.
- This is only compatible with Vulkan. It has no effect on DX11/12 games.


## Transparency
PYroclast modifies only the directories and files that you explicitly configure or enable. Specifically, it:
- Reads and writes to the `.config/vkBasalt.conf` file (or the path you specify).  
- Reads and writes to `.desktop` files if you opt to have separate vkBasalt configs per game/application.  
- Optionally manages the directories containing ReShade FX shaders or 3D LUT files if you enable those features.  
- Does **not** collect or transmit any personal data or system information.  
- Avoids altering other system files outside the scope of vkBasalt configuration.

## Why is it called PYroclast?
It's continuing the joke: vulkan post processing → after vulcan → basalt → pyroclast 

<img src="https://raw.githubusercontent.com/TripleJumpStudios/PYroclast/f56ac72672bc6656973f1c27382510cc9de0d358/icon.png" alt="PYroclast Icon" width="25" /> 
#extras and thoughts
#vkmark is a vulkan benchmark tool
#GOverlay is pretty much a must or want
#build out links to great .fx files and LUT files
