from behave import *
from selenium import webdriver

@Given("open google page")
def step_impl(context):
    context.driver=webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.get("https://google.com")

@When("Enter the text")
def step_impl(context):
    context.driver.find_element_by_xpath("//INPUT[@id='lst-ib']").send_keys("allure-behave")
    context.driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[3]/center/input[1]").click()

@Then("Search")
def step_impl(context):
    print("Thanks")