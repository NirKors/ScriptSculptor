from configparser import ConfigParser


class Processing:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config/settings.ini')
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
        with open('config/settings.ini', 'w') as configfile:
            self.config.write(configfile)

    def save_script(self, commands):

        print("processing.save_script:")
        print(commands)
        pass
