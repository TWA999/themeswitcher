import os
import subprocess

# List of available themes
themes = {
    "1": "OceanKDE",
    "2": "PirateKDE"
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

        # Ask if the user wants to restart Plasma Shell
        restart_plasma = input("Restart Plasma Shell? (y/n): ").strip().lower()
        if restart_plasma == "y":
            os.system("kquitapp5 plasmashell && kstart5 plasmashell")
        
        break  # Exit after applying the theme
    else:
        print("Invalid choice. Please try again.")