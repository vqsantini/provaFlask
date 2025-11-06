*** Settings ***
Library           SeleniumLibrary
Suite Setup       Abrir Navegador
Suite Teardown    Fechar Navegador

*** Variables ***
${URL_BASE}       http://127.0.0.1:5000/login

*** Keywords ***
Abrir Navegador
    Open Browser    ${URL_BASE}    chrome
    Maximize Browser Window

Fechar Navegador
    Close Browser

*** Test Cases ***
Deve Fazer Login Com Email E Senha
    [Documentation]    Testa o login real via navegador
    Input Text    id:email    admin@gmail.com
    Input Text    id:senha    123456
    Click Button    id:login-btn
    Sleep    2s
    Page Should Contain    Login feito com sucesso
