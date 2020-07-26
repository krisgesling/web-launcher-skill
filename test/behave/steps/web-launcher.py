from behave import then

from test.integrationtests.voight_kampff import mycroft_responses, then_wait


@then('"{url}" should be opened')
def then_url_opened(context, url):
    def check_url_in_msg(message):
        success = message.data.get('site_url') == url
        debug_msg = "" if success else "Incorrect url"
        return (success, debug_msg)

    passed, debug = then_wait('skill.weblauncher.opening', check_url_in_msg,
                              context)
    if not passed:
        assert_msg = debug
        assert_msg += mycroft_responses(context)

    assert passed, assert_msg or "Web Launcher did not open the url"
