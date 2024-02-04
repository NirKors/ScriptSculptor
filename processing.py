from configparser import ConfigParser


class Processing:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.relief_counter = self.config.getint('styles', 'relief_counter')
        self.reliefs = self.config.get('styles', 'relief').split(', ')

    def get_relief(self):
        if self.reliefs and self.relief_counter < len(self.reliefs):
            relief = self.reliefs[self.relief_counter]
            self.relief_counter += 1
        else:
            self.relief_counter = 0
            relief = self.reliefs[self.relief_counter]

        # Update the value of relief_counter
        self.config.set('styles', 'relief_counter', str(self.relief_counter))
        return relief

    def process_user_info(self, info):
        return
