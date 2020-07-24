from mycroft import MycroftSkill, intent_file_handler


class WebLauncher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('launcher.web.intent')
    def handle_launcher_web(self, message):
        self.speak_dialog('launcher.web')


def create_skill():
    return WebLauncher()

