from configparser import ConfigParser

import xerox


class Processing:
    def __init__(self, config_path):
        self.config = ConfigParser()
        self.config_path = config_path

        self.config.read(f'{self.config_path}\\settings.ini')
        self.reliefs = self.config.get('styles', 'relief').split(', ')

    def cycle_relief(self):
        relief_counter = int(self.config.get('styles', 'relief_counter'))
        if relief_counter < len(self.reliefs) - 1:
            relief = self.reliefs[relief_counter]
            relief_counter += 1
        else:
            relief_counter = 0
            relief = self.reliefs[relief_counter]

        # Update the value of relief_counter
        self.config.set('styles', 'relief_counter', str(relief_counter))
        self.save_settings()
        return relief

    def get_relief(self):
        relief_num = int(self.config.get('styles', 'relief_counter'))
        return self.reliefs[relief_num]

    def save_settings(self):
        with open(f'{self.config_path}\\settings.ini', 'w') as configfile:
            self.config.write(configfile)

    @staticmethod
    def check_for_errors(values):
        errors = []
        # Check if there are any errors
        for frame in values:
            check = frame.action.check_for_errors()
            if check:
                errors.append(f"Action - {frame.action.name}\nError: {check}")
        return errors

    def save_script(self, commands):
        """
        Saves a list of script commands to a file.

        Args:
            commands (list): A list of strings representing the script commands.

        Returns:
            None

        Raises:
            Exception: If there is an error writing the file.
        """

        with open("script.bat", "w") as file:
            file.writelines(command + "\n" for command in commands)

    @staticmethod
    def copy_to_clipboard(commands):
        commands = "\n".join(commands)
        xerox.copy(commands)
