1 - Para executar, clone o repostório;

2 - Navegue até a pasta do projeto com o comando cd Addsab-site-de-denuncia

3 - Crie seu ambiente virtual (venv) no seu terminal para instalar os pacotes necessários: 

No Linux - python3 -m venv venv 

Ative com: source venv/bin/activate

No Windows - python3 -m venv venv 

ative com: venv\Scripts\activate se estiver assim (venv) está ativada, pode 
instalar os requirements nesse ambiente criado.

4 - Estando dentro da pasta do projeto Addsab-site-de-denuncia instale os requirements(pacotes) com a venv ativa no terminal (venv) com o comando pip install -r requirements.txt

5 - Execute o comando no terminal python manage.py makemigrations e python manage.py migrate para executar as migrações e popular o 
banco de dados.

6 - No terminal crie seu próprio super usuario com python manage.py createsuperuser e coloque apenas o nome e password, 
pule os outros dados que pede lá, preencha apenas um nome e senha, tipo admin e senha 123.

em seguida execute com python manage.py runserver e o projeto vai rodar na porta 8000.
acesse o admin do django para ter ver as funcionalidades, até agora não tem frontend.
Logue com seu super usuario que criou em:
http://127.0.0.1:8000/admin/
