from actions.cancel_shutdown import CancelShutdown
from actions.copyfiles import CopyFiles
from actions.deletefiles import DeleteFiles
from actions.openfiles import OpenFiles
from actions.ping import Ping
from actions.shutdown import Shutdown
from actions.system_information import SystemInformation
from actions.copyfolder import CopyFolder
from actions.deletefolder import DeleteFolder
from actions.createfolder import CreateFolder
from actions.openfolder import OpenFolder


def create_action(selected_action, dropdown_options):
    """
    Create an instance of the selected action class.

    This function dynamically selects and creates an instance of the action class
    corresponding to the selected action from the dropdown menu.

    Args:
        selected_action (str): The selected action from the dropdown menu.
        dropdown_options (list): List of available action options.

    Returns:
        Instance of the selected action class.
    """
    action_classes = {option: globals().get(option.replace(' ', '')) for option in dropdown_options}
    action_class = action_classes.get(selected_action)

    return action_class()


def clear_frame(frame):
    """
    Clear the contents of a Tkinter frame.

    This function removes all children of the specified Tkinter frame, except for the first three children.
    The first three children are the UI elements that exist in every action frame.

    Args:
        frame: Tkinter frame to clear.

    Returns:
        None
    """
    counter = 0
    for child in frame.winfo_children():
        if counter >= 3:
            child.destroy()
        counter += 1
