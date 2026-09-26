*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}          https://www.saucedemo.com/
${BROWSER}      Chrome
${USERNAME}     standard_user
${PASSWORD}     secret_sauce

*** Test Cases ***
Task 1 - Open Browser And Navigate
    [Documentation]    Basic syntax: open browser + verify title
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Title Should Be    Swag Labs
    Log    Browser opened successfully
    [Teardown]    Close Browser

Task 1b - Input Text And Verify Element
    [Documentation]    Fill form + verify login button exists
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Input Text      id:user-name    ${USERNAME}
    Input Text      id:password     ${PASSWORD}
    Page Should Contain Element    id:login-button
    Log    Form filled, button present
    [Teardown]    Close Browser

Task 2 - Login With Variables
    [Documentation]    Login using stored variables
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Input Text      id:user-name    ${USERNAME}
    Input Text      id:password     ${PASSWORD}
    Click Button    id:login-button
    Wait Until Location Contains    inventory.html    timeout=10s
    Log    Login succeeded with variables
    [Teardown]    Close Browser

Task 2b - Data Driven Login
    [Documentation]    Loop through multiple user/pass combinations
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    FOR    ${user}    ${pass}    IN
    ...    standard_user    secret_sauce
    ...    locked_out_user  secret_sauce
    ...    wrong_user       wrong_pass
        Go To    ${URL}
        Input Text      id:user-name    ${user}
        Input Text      id:password     ${pass}
        Click Button    id:login-button
        Sleep    2s
        Log    Attempted login: ${user}
    END
    [Teardown]    Close Browser

Task 4 - Assertion After Login
    [Documentation]    Verify page elements and URL after login
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Input Text      id:user-name    ${USERNAME}
    Input Text      id:password     ${PASSWORD}
    Click Button    id:login-button
    Wait Until Location Contains    inventory.html    timeout=10s

    Page Should Contain Element    class:inventory_list
    Location Should Contain    inventory.html
    Title Should Be    Swag Labs

    Log    All assertions passed
    [Teardown]    Close Browser

Task 7 - Custom Log Messages
    [Documentation]    Use Log keyword at different levels
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Log    Info level message    level=INFO
    Log    Warning level message    level=WARN
    Page Should Contain Element    id:login-button
    Log    Logs visible in log.html
    [Teardown]    Close Browser
