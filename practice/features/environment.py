import sys
#from mock.mock import self
import allure
from selenium import webdriver
import time
import logging
import os
import shutil
from allure_commons.types import AttachmentType

# Initialization of Testing Suite

def before_all(context):
    print("Executing before all")

# Initialization of the Feature file under Suite

def before_feature(context, feature):
    # Create logger
    # TODO - http://stackoverflow.com/questions/6386698/using-the-logging-python-class-to-write-to-a-file
    context.logger = logging.getLogger ( 'seleniumframework_tests' )
    hdlr = logging.FileHandler ( './seleniumframework_tests.log' )
    formatter = logging.Formatter ( '%(asctime)s %(levelname)s %(message)s' )
    hdlr.setFormatter ( formatter )
    context.logger.addHandler ( hdlr )
    context.logger.setLevel ( logging.DEBUG )
    args=(sys.stdout)
    context.logger.debug(args)

    # Initialization of browser

    print("User data:" , context.config.userdata)
    # behave -D BROWSER=chrome
    if 'BROWSER' in context.config.userdata.keys ( ):
        if context.config.userdata['BROWSER'] is None:
            BROWSER = 'chrome'
        else:
            BROWSER = context.config.userdata['BROWSER']
    else:
        BROWSER = 'chrome'
    # For some reason, python doesn't have switch case -
    # http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
    if BROWSER == 'chrome':
        context.browser = webdriver.Chrome ( )
    elif BROWSER == 'firefox':
        context.browser = webdriver.Firefox ( )
    elif BROWSER == 'safari':
        context.browser = webdriver.Safari ( )
    elif BROWSER == 'ie':
        context.browser = webdriver.Ie ( )
    elif BROWSER == 'opera':
        context.browser = webdriver.Opera ( )
    elif BROWSER == 'phantomjs':
        context.browser = webdriver.PhantomJS ( )
    else:
        print("Browser you entered:" , BROWSER , "is invalid value")

    context.browser.maximize_window ( )

# Initialization of Scenario under feature file

def before_scenario(context, scenario):
    print("Before scenario\n")

# if the scenario Fails, it capture screenshots

def after_scenario(context , scenario):
    print("scenario status : " + str(scenario.status))
    if scenario.status == "Status.failed":
        if not os.path.exists ( "failed_scenarios_screenshots" ):
            os.makedirs ( "failed_scenarios_screenshots" )
        os.chdir ( "failed_scenarios_screenshots" )
        context.browser.save_screenshot ( scenario.name + "_" + time.strftime("%Y%m%d%H%M%S") + "_failed.png" )
    allure.attach(context.browser.get_screenshot_as_png(), name="Screenshot", attachment_type=AttachmentType.PNG)


# End of Feature

def after_feature(context , feature):
    print("\nAfter Feature")
    context.browser.quit ( )

# End of Test Suite

def after_all(context):
    print("User data:", context.config.userdata)
    #behave -D ARCHIVE=Yes
    if 'ARCHIVE' in context.config.userdata.keys():
        if os.path.exists("failed_scenarios_screenshots"):
            os.rmdir("failed_scenarios_screenshots")
            os.makedirs("failed_scenarios_screenshots")
        if context.config.userdata['ARCHIVE'] == "Yes":
            shutil.make_archive(
    time.strftime("%d_%m_%Y"),
    'zip',
     "failed_scenarios_screenshots")
            #os.rmdir("failed_scenarios_screenshots")
            print("Executing after all")