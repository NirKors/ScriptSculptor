import configparser

from actions.cancel_shutdown import CancelShutdown
from actions.copyfile import CopyFile
from actions.createfolder import CreateFolder
from actions.deletefiles import DeleteFiles
from actions.open import Open
from actions.ping_website import PingWebsite
from actions.shutdown import Shutdown
from actions.sleep import Sleep
from actions.system_information import SystemInformation
from actions.copyfolder import CopyFolder
from actions.deletefolders import DeleteFolders


def create_action(selected_action, dropdown_options):
    action_classes = {
        "Shutdown": Shutdown,
        "Sleep": Sleep,
        "Open": Open,
        "Copy File(s)": CopyFile,
        "Copy Folder": CopyFolder,
        "Delete File(s)": DeleteFiles,
        "Delete Folder": DeleteFolders,
        "Create": CreateFolder,
        "Ping Website": PingWebsite,
        "System Information": SystemInformation,
        "Cancel Shutdown": CancelShutdown,
    }

    action_class = action_classes.get(selected_action)
    return action_class()

def clear_frame(frame):
    counter = 0
    for child in frame.winfo_children():
        if counter >= 3:
            child.destroy()
        counter += 1
