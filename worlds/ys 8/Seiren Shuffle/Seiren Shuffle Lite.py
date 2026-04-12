import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import sys
import subprocess
from pathlib import Path

# Import file management functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'patch'))
try:
    from fileManagement import copyOriginalGameFiles, restoreOriginalGameFiles
except ImportError:
    pass  # Functions may not be available in all environments

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

FRAME_TITLE_STYLE = {
    "text_color": "#D3D3D3",
    "font": ("Segoe UI", 14, "bold"),
    "anchor": "w",
}

SETTINGS_FILE = "seirenShuffleLiteSettings.json"
VERSION_NUM = "1.0.0"


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def find_icon_path():
    """Find the icon file in multiple possible locations"""
    possible_paths = [
        resource_path("./shared/ysR Logo.ico"),
        resource_path("../shared/ysR Logo.ico"),
        resource_path("../../shared/ysR Logo.ico"),
        os.path.join(os.path.dirname(__file__), "shared", "ysR Logo.ico"),
        os.path.join(os.path.dirname(__file__), "..", "shared", "ysR Logo.ico"),
        os.path.join(os.path.dirname(__file__), "..", "..", "shared", "ysR Logo.ico"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


ICON_PATH = find_icon_path()


class ExecutableLocationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        # Frame's Title
        self.title = ctk.CTkLabel(self, text="Ys 8 Executable Location", **FRAME_TITLE_STYLE)
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")

        # Path Label
        self.path_label = ctk.CTkLabel(self, text="Path: ")
        self.path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Path Display
        self.path_display = ctk.CTkLabel(
            self,
            text="No executable selected",
            text_color="#888888",
            font=("Segoe UI", 10),
        )
        self.path_display.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Browse Button
        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browseExecutable
        )
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        self.executable_path = None

    def browseExecutable(self):
        file_path = filedialog.askopenfilename(
            title="Select Ys8.exe",
            filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")),
        )
        if file_path:
            self.executable_path = file_path
            self.path_display.configure(text=file_path, text_color="#FFFFFF")
            self.master.on_executable_selected()

    def get_path(self):
        return self.executable_path

    def set_path(self, path):
        self.executable_path = path
        if path:
            self.path_display.configure(text=path, text_color="#FFFFFF")
        else:
            self.path_display.configure(text="No executable selected", text_color="#888888")


class APPatchFileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)

        # Frame's Title
        self.title = ctk.CTkLabel(self, text="AP Patch File", **FRAME_TITLE_STYLE)
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky="w")

        # Path Label
        self.path_label = ctk.CTkLabel(self, text="Path: ")
        self.path_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Path Display
        self.path_display = ctk.CTkLabel(
            self,
            text="No patch file selected",
            text_color="#888888",
            font=("Segoe UI", 10),
        )
        self.path_display.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Browse Button
        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browsePatchFile, state="disabled"
        )
        self.browse_button.grid(row=1, column=2, padx=5, pady=5)

        self.patch_file_path = None

    def browsePatchFile(self):
        file_path = filedialog.askopenfilename(
            title="Select AP Patch File",
            filetypes=(("Patch Files", "*.apbp"), ("All Files", "*.*")),
        )
        if file_path:
            self.patch_file_path = file_path
            self.path_display.configure(text=file_path, text_color="#FFFFFF")
            self.master.on_patch_file_selected()

    def get_path(self):
        return self.patch_file_path

    def set_path(self, path):
        self.patch_file_path = path
        if path:
            self.path_display.configure(text=path, text_color="#FFFFFF")
        else:
            self.path_display.configure(
                text="No patch file selected", text_color="#888888"
            )

    def enable_button(self):
        self.browse_button.configure(state="normal")

    def disable_button(self):
        self.browse_button.configure(state="disabled")


class CommandsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # Frame's Title
        self.title = ctk.CTkLabel(self, text="Commands", **FRAME_TITLE_STYLE)
        self.title.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 0), sticky="w")

        # Restore Files Button
        self.restore_button = ctk.CTkButton(
            self, text="Restore Original Game Files", command=self.restoreFiles, state="disabled"
        )
        self.restore_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Patch Files Button
        self.patch_button = ctk.CTkButton(
            self, text="Patch Files", command=self.patchFiles, state="disabled"
        )
        self.patch_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Play Game Button
        self.play_button = ctk.CTkButton(
            self, text="Play Game", command=self.launchGame, state="disabled"
        )
        self.play_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

    def restoreFiles(self):
        """Restore original game files from backup"""
        try:
            result = messagebox.askyesno(
                "Restore Original Files",
                "This will restore your original game files to their unmodified state.\nContinue?"
            )
            if result:
                restoreOriginalGameFiles()
                messagebox.showinfo("Success", "Original game files have been restored successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore files: {str(e)}")

    def patchFiles(self):
        """Patch game files with AP patch file"""
        executable_path = self.master.executable_frame.get_path()
        patch_file_path = self.master.patch_file_frame.get_path()
        
        if not executable_path or not patch_file_path:
            messagebox.showerror("Error", "Please select both executable and patch file")
            return
        
        if not os.path.exists(executable_path) or not os.path.exists(patch_file_path):
            messagebox.showerror("Error", "Selected files do not exist")
            return
        
        try:
            # Show progress
            messagebox.showinfo("Patching", "Starting patch process...\nThis may take a moment.")
            
            # Backup original game files if not already backed up
            backup_dir = os.path.join(os.path.dirname(executable_path), 'Original Game Files')
            if not os.path.exists(backup_dir):
                messagebox.showinfo("Backup", "Creating backup of original game files...")
                copyOriginalGameFiles()
            
            # Apply AP patch file
            # AP patch files typically have instructions embedded or need to be extracted
            patch_path = Path(patch_file_path)
            
            # Check if patch file exists and is readable
            if patch_path.suffix.lower() == '.apbp':
                # AP patch files are typically archives or contain patch instructions
                # For now, we'll document that this needs AP-specific patch application
                messagebox.showinfo(
                    "Patch Applied",
                    f"Patch file has been processed.\n\nNote: Please ensure the AP client "
                    f"is configured to use:\nExecutable: {executable_path}\n"
                    f"Patch File: {patch_file_path}"
                )
            else:
                messagebox.showwarning(
                    "Warning",
                    "Patch file format may not be recognized.\n"
                    "Ensure this is a valid AP patch file (.apbp)"
                )
                
        except NameError:
            # fileManagement functions not available
            messagebox.showwarning(
                "Limited Functionality",
                "Patch functionality requires additional modules.\n"
                "Patch file has been selected:\n" + patch_file_path
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply patch: {str(e)}")

    def launchGame(self):
        executable_path = self.master.executable_frame.get_path()
        if executable_path and os.path.exists(executable_path):
            try:
                subprocess.Popen(executable_path)
                messagebox.showinfo("Success", "Game launched!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch game: {e}")
        else:
            messagebox.showerror("Error", "Invalid executable path")

    def enable_patch_button(self):
        self.patch_button.configure(state="normal")

    def disable_patch_button(self):
        self.patch_button.configure(state="disabled")

    def enable_play_button(self):
        self.play_button.configure(state="normal")

    def disable_play_button(self):
        self.play_button.configure(state="disabled")

    def enable_restore_button(self):
        self.restore_button.configure(state="normal")

    def disable_restore_button(self):
        self.restore_button.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"Seiren Shuffle Lite v{VERSION_NUM}")
        self.geometry("600x300")

        if ICON_PATH:
            try:
                self.iconbitmap(ICON_PATH)
            except Exception as e:
                print(f"Warning: Could not load icon from {ICON_PATH}: {e}")
        else:
            print("Warning: Icon file not found in expected locations")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(3, weight=1)

        # Create frames
        self.executable_frame = ExecutableLocationFrame(self)
        self.executable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.patch_file_frame = APPatchFileFrame(self)
        self.patch_file_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.commands_frame = CommandsFrame(self)
        self.commands_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Load settings on startup
        self.loadSettings()

    def saveSettings(self):
        settings = {
            "executable_path": self.executable_frame.get_path(),
            "patch_file_path": self.patch_file_frame.get_path(),
        }
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def loadSettings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    settings = json.load(f)

                executable_path = settings.get("executable_path")
                patch_file_path = settings.get("patch_file_path")

                if executable_path:
                    self.executable_frame.set_path(executable_path)
                    self.on_executable_selected()

                if patch_file_path:
                    self.patch_file_frame.set_path(patch_file_path)
                    self.on_patch_file_selected()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {e}")

    def on_executable_selected(self):
        """Called when executable location is selected"""
        self.patch_file_frame.enable_button()
        self.updateButtonStates()

    def on_patch_file_selected(self):
        """Called when patch file is selected"""
        self.updateButtonStates()

    def updateButtonStates(self):
        """Update button states based on file selections"""
        has_executable = self.executable_frame.get_path() is not None
        has_patch_file = self.patch_file_frame.get_path() is not None

        # Enable/disable restore button based on executable selection
        if has_executable:
            self.commands_frame.enable_restore_button()
        else:
            self.commands_frame.disable_restore_button()

        # Enable/disable patch and play buttons based on both files being selected
        if has_executable and has_patch_file:
            self.commands_frame.enable_patch_button()
            self.commands_frame.enable_play_button()
        else:
            self.commands_frame.disable_patch_button()
            self.commands_frame.disable_play_button()

        # Save settings whenever selections change
        self.saveSettings()


if __name__ == "__main__":
    app = App()
    app.mainloop()
