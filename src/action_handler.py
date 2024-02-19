from actions.cancel_shutdown import CancelShutdown
from actions.copyfiles import CopyFiles
from actions.deletefiles import DeleteFiles
from actions.open import Open
from actions.ping_website import PingWebsite
from actions.shutdown import Shutdown
from actions.sleep import Sleep
from actions.system_information import SystemInformation
from actions.copyfolder import CopyFolder
from actions.deletefolder import DeleteFolder
from actions.createfolder import CreateFolder



def create_action(selected_action, dropdown_options):
    action_classes = {option: globals().get(option.replace(' ', '')) for option in dropdown_options}
    action_class = action_classes.get(selected_action)

    return action_class()


def clear_frame(frame):
    counter = 0
    for child in frame.winfo_children():
        if counter >= 3:
            child.destroy()
        counter += 1
