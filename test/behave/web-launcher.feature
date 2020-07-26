Feature: Web-Launcher

  Scenario Outline: Open a known website
    Given an english speaking user
      When the user says "<open website by name>"
      Then "<url>" should be opened

   Examples: open a known website
     | open website by name | url |
     | open duck duck go | https://duckduckgo.com |
     | navigate to github | https://github.com |
     | launch twitter | https://twitter.com |
     | go to Todoist | https://todoist.com/app |
     | launch gmail | https://gmail.com |
     | open Reddit | https://reddit.com |