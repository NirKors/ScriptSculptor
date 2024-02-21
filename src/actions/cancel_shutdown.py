from .action import Action


class CancelShutdown(Action):
    def __init__(self):
        super().__init__()
        self.name = "Cancel Shutdown"

    def build_ui(self):
        tooltip = """
        This command cancels a pending system shutdown. If your computer is scheduled to shut down 
        automatically at a later time, running this command will prevent it from doing so. 
        
        Important Points:
        
            - This command only works if a shutdown is already scheduled. It has no effect if the computer is not 
              currently set to shut down automatically.
        
        Warning!
        
            - Cancelling a planned shutdown that is critical for system maintenance or updates can have negative 
              consequences.
        """
        # Set the tooltip text for your Cancel Shutdown action using this variable
        self.explanatory_tooltip(tooltip)

    def check_for_errors(self):
        pass

    def check_for_warnings(self):
        return True

    def get_command_string(self):
        return "/shutdown /a"
