*** Settings ***
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://127.0.0.1:5000

*** Test Cases ***
Deve Efetuar Login Com Sucesso
    Create Session    api    ${BASE_URL}
    ${body}=    Create Dictionary    email=admin@gmail.com    senha=123456
    ${response}=    POST On Session    api    /api/login    json=${body}
    Status Should Be    200    ${response}
    Should Contain    ${response.json()["message"]}    Login feito com sucesso
