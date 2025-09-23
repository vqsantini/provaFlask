# Sistema de Gestão de Pacotes de Viagem

## Requisitos
- Python 3.10+
- pip
- virtualenv

## Instalação
1. Criar ambiente virtual:
   python -m venv venv

2. Ativar ambiente:
   - Windows: venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate

3. Instalar dependências:
   pip install -r requirements.txt

4. Criar banco de dados:
   flask db init
   flask db migrate
   flask db upgrade

5. Executar aplicação:
   python main.py
