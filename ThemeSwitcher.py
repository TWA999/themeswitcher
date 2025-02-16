import os
import subprocess
import re

# List of available themes
themes = {
    "1": "PirateKDE",
    "2": "OceanKDE"
}

# Function to check if the theme exists
def is_theme_available(theme_name):
    try:
        result = subprocess.run(["lookandfeeltool", "--list"], capture_output=True, text=True)
        return theme_name in result.stdout
    except FileNotFoundError:
        print("Error: lookandfeeltool not found. Ensure KDE is installed.")
        return False

# Function to apply the KDE theme
def apply_kde_theme(theme_name):
    if not is_theme_available(theme_name):
        print(f"Error: Theme '{theme_name}' not found. Run 'lookandfeeltool --list' to check.")
        return

    print(f"Applying theme: {theme_name}...")
    result = subprocess.run(["lookandfeeltool", "--apply", theme_name], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Theme applied successfully!")
    else:
        print("Failed to apply theme. Error:\n", result.stderr)

# Function to change wallpaper plugin
def change_wallpaper_plugin(theme_name):
    file_path = "/home/twa/.config/plasma-org.kde.plasma.desktop-appletsrc"

    # Read the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Look for the section after [Containments][44]
    section_start_pattern = r'(\[Containments\]\[44\])'
    section_start_match = re.search(section_start_pattern, content)

    if section_start_match:
        # Get the position where the section starts
        section_start_pos = section_start_match.end()

        # Now, find all instances of 'wallpaperplugin=org.kde.image' or 'wallpaperplugin=org.kde.snow' after the section header
        section_content = content[section_start_pos:]

        # If theme is PirateKDE, change wallpaperplugin from org.kde.image to org.kde.snow
        if theme_name == "PirateKDE":
            section_content = re.sub(r'wallpaperplugin=org.kde.image', 'wallpaperplugin=org.kde.snow', section_content)
        # If theme is OceanKDE, change wallpaperplugin from org.kde.snow to org.kde.image
        elif theme_name == "OceanKDE":
            section_content = re.sub(r'wallpaperplugin=org.kde.snow', 'wallpaperplugin=org.kde.image', section_content)

        # Reconstruct the content: the part before the section, the modified section, and the part after
        modified_content = content[:section_start_pos] + section_content

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)

        print(f"Wallpaper plugin updated successfully for {theme_name}.")
    else:
        print("[Containments][44] section not found.")

# Function to change wallpaper based on theme for both monitors
def change_wallpaper_image(theme_name):
    file_path = "/home/twa/.config/plasma-org.kde.plasma.desktop-appletsrc"
    
    # Read the file
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Loop through the content to modify the wallpaper for both monitors
    for i, line in enumerate(content):
        if 'Image=' in line:
            # For the main monitor (43)
            if '[Containments][43][Wallpaper][org.kde.image][General]' in content[i-1]:
                if theme_name == "PirateKDE":
                    content[i] = 'Image=/home/twa/Pictures/wallpapers/01.jpg\n'
                    content[i+1] = 'PreviewImage=/home/twa/Pictures/wallpapers/01.jpg\n'
                elif theme_name == "OceanKDE":
                    content[i] = 'Image=/home/twa/Pictures/wallpapers/11.jpg\n'
                    content[i+1] = 'PreviewImage=/home/twa/Pictures/wallpapers/11.jpg\n'
            
            # For the second monitor (44)
            if '[Containments][44]' in content[i]:
                if theme_name == "PirateKDE":
                    content[i] = 'wallpaperplugin=org.kde.snow\n'

                elif theme_name == "OceanKDE":
                    content[i] = 'wallpaperplugin=org.kde.image\n'

    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(content)

    print(f"Wallpaper changed for {theme_name} on both monitors.")

# Ensure UTF-8 locale is set
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

# Display menu
while True:
    print("\nSelect a KDE theme to apply:")
    for key, theme in themes.items():
        print(f"{key}. {theme}")
    print("0. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "0":
        print("Exiting...")
        break
    elif choice in themes:
        apply_kde_theme(themes[choice])

        # Change wallpaper image based on theme selection
        change_wallpaper_image(themes[choice])

        # Change wallpaper plugin based on theme selection
        change_wallpaper_plugin(themes[choice])

        # Automatically restart Plasma Shell
        os.system("kquitapp5 plasmashell && kstart5 plasmashell")
        
        break  # Exit after applying the theme
    else:
        print("Invalid choice. Please try again.")
