*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.

*** Test Case ***
first dummy test
    [Tags]    Iteration-3    Smoke
    [Documentation]    Opens a browser to login url, inputs valid username
    ...                and password and checks that the welcome page is open.
    ...                This is a smoke test. Created in iteration 3.
    Log    Hello, world!

failing test
    Fail	Test not ready

skipping test
    Pass Execution	was too drunk to run this test

tags tests
    set tags    aapeli
