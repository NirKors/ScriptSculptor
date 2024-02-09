from actions.cancel_shutdown import CancelShutdown
from actions.copy import Copy
from actions.create import Create
from actions.delete import Delete
from actions.open import Open
from actions.ping_website import PingWebsite
from actions.shutdown import Shutdown
from actions.sleep import Sleep
from actions.system_information import SystemInformation


def handle_action_selection(selected_action, master_frame):
    # Destroy previous UI components
    clear_frame(master_frame)

    # Create an instance of the selected action class
    action = create_action(selected_action)
    action.build_ui(master_frame)


def create_action(selected_action):
    action_classes = {
        "Shutdown": Shutdown,
        "Sleep": Sleep,
        "Open": Open,
        "Copy": Copy,
        "Delete": Delete,
        "Create": Create,
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
