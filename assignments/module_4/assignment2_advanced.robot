*** Settings ***
Library           SeleniumLibrary
Library           my_keywords.py
Library           String
Suite Setup       Log    === Suite Starting ===
Suite Teardown    Log    === Suite Finished ===

*** Variables ***
${URL}          https://www.saucedemo.com/
${BROWSER}      Chrome

*** Test Cases ***
Task 3 - Custom Python Keyword
    [Documentation]    Use custom Python keyword
    [Tags]    smoke    math
    ${result}=    Add Numbers    15    27
    Should Be Equal As Integers    ${result}    42
    Log    Custom keyword returned ${result}

Task 3b - BuiltIn Library Operations
    [Documentation]    Use String library for text operations
    [Tags]    smoke
    ${upper}=    Convert To Uppercase    hello
    Should Be Equal    ${upper}    HELLO

    ${length}=    Get Length    robotframework
    Should Be Equal As Integers    ${length}    14

    ${sum}=    Evaluate    5 + 10
    Should Be Equal As Integers    ${sum}    15

    Log    BuiltIn operations passed

Task 5 - Setup And Teardown Demo
    [Documentation]    Suite setup opens browser, teardown closes it
    [Tags]    smoke    login
    [Setup]    Open Login Page
    Perform Login
    Verify Inventory Page
    [Teardown]    Close Login Page

Task 6 - Tagged Smoke Test
    [Documentation]    Runs when --include smoke is used
    [Tags]    smoke
    [Setup]    Open Login Page
    Page Should Contain Element    id:login-button
    Log    Login button present - smoke test passed
    [Teardown]    Close Login Page

Task 6b - Tagged Regression Test
    [Documentation]    Runs when --include regression is used
    [Tags]    regression
    [Setup]    Open Login Page
    Input Text      id:user-name    standard_user
    Input Text      id:password     secret_sauce
    Click Button    id:login-button
    Wait Until Location Contains    inventory.html    timeout=10s
    Log    Regression test completed
    [Teardown]    Close Login Page

*** Keywords ***
Open Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Close Login Page
    Close Browser

Perform Login
    Input Text      id:user-name    standard_user
    Input Text      id:password     secret_sauce
    Click Button    id:login-button
    Wait Until Location Contains    inventory.html    timeout=10s

Verify Inventory Page
    Page Should Contain Element    class:inventory_list
    Log    Login verified
