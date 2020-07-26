import subprocess

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler


class WebLauncher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.sites = self.translate_namedvalues("sites")

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()
        self.register_sites_as_vocab()

    def register_sites_as_vocab(self):
        for site_name in self.sites:
            self.register_vocabulary(site_name.lower(), 'SiteName')

    def on_settings_changed(self):
        options = [('name_one', 'url_one'), 
                   ('name_two', 'url_two'), 
                   ('name_three', 'url_three')]
        for o in options:
            name = self.settings.get(o[0])
            url = self.settings.get(o[1])
            if name and url:
                self.sites[name] = url

    @intent_handler(IntentBuilder('LaunchSite').require('Launch').require('SiteName'))
    def handle_launch_site(self, message):
        requested_site = message.data.get('SiteName')
        if requested_site in self.sites:
            args = ['xdg-open', self.sites[requested_site]]
            current_process = subprocess.Popen(args)
        else:
            self.speak_dialog('not.found')


def create_skill():
    return WebLauncher()

