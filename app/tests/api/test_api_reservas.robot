*** Settings ***
Library           RequestsLibrary
Suite Setup       Create Session    api    http://127.0.0.1:5000

*** Variables ***
${BASE_URL}       http://127.0.0.1:5000
${LOGIN_ENDPOINT}    /api/login
${RESERVAS_ENDPOINT}    /api/reservas

*** Test Cases ***
Deve Efetuar Login Com Sucesso
    ${body}=    Create Dictionary    email=admin@gmail.com    senha=123456
    ${response}=    POST On Session    api    ${LOGIN_ENDPOINT}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console    Login bem-sucedido na API

Listar Reservas (GET)
    ${response}=    GET On Session    api    ${RESERVAS_ENDPOINT}
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console    Reservas listadas com sucesso

Criar Reserva (POST)
    ${body}=    Create Dictionary
    ...    cliente_nome=Teste Robot
    ...    cliente_email=teste@robot.com
    ...    cliente_telefone=9999-9999
    ...    pacote_id=1
    ...    quantidade=1
    ${response}=    POST On Session    api    ${RESERVAS_ENDPOINT}    json=${body}
    Log To Console    Url: ${response.url}
    Should Be Equal As Integers    ${response.status_code}    201
    Log To Console    Reserva criada com sucesso

Cancelar Reserva (POST)
    ${response}=    POST On Session    api    ${RESERVAS_ENDPOINT}/1/cancelar
    Should Be Equal As Integers    ${response.status_code}    200
    Log To Console    Reserva cancelada com sucesso
