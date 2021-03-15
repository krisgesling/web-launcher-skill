import subprocess

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message


class WebLauncher(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.sites = self.translate_namedvalues("sites")

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()

    def on_settings_changed(self):
        """Load all custom site settings and register names as vocab.
        
        If expanding number of custom url settings available remember to 
        increment range stop.
        """
        for num in range(1, 6):
            name = self.settings.get('name_' + str(num))
            url = self.settings.get('url_' + str(num))
            if name and url:
                self.sites[name] = url
        self.register_sites_as_vocab()

    def register_sites_as_vocab(self):
        """Registers site names as vocab for Adapt intents."""
        for site_name in self.sites:
            self.register_vocabulary(site_name.lower(), 'SiteName')

    @intent_handler(IntentBuilder('LaunchSite').require('Launch')
                                               .require('SiteName'))
    def handle_launch_site(self, message):
        """Launch known site using xdg-open url.
        
        Primary intent handler for this Skill. Uses Adapt so that only
        utterances that include a known site are triggered. Prevents conflicts
        with other intents that also use vocabularly like "launch" or "open".
        """
        requested_site = message.data.get('SiteName')
        if requested_site in self.sites:
            site_url = self.sites[requested_site]
            if self.gui.connected:
                self.gui.show_url(site_url)
            else:
                args = ['xdg-open', site_url]
                current_process = subprocess.Popen(args)
            self.bus.emit(Message('skill.weblauncher.opening', {
                                      'site_name': requested_site,
                                      'site_url': site_url }))
        else:
            # This should never actually be triggered
            self.speak_dialog('not.found')


def create_skill():
    return WebLauncher()

