1 - Para executar, clone o repostório;

2 - Navegue até a pasta do projeto com o comando cd Addsab-site-de-denuncia

3 - Crie seu ambiente virtual (venv) para instalar os pacotes: 

No Linux - python3 -m venv venv Ative com: source venv/bin/activate

No Windows - python3 -m venv venv ative com: venv\Scripts\activate se estiver assim (venv) está ativada, pode 
instalar os requirements nesse ambiente criado.

4 - Instale os requirements com a venv ativa no terminal (venv) com o comando pip install -r requirements.txt

5 - Execute o comando python manage.py makemigrations e python manage.py migrate para executar as migrações e popular o 
banco de dados, em seguida execute com python manage.py runserver e o projeto vai rodar na porta 8000.

no terminal crie seu proprio super usuario com python manage.py createsuperuser e coloque apenas o nome e password, 
pule os outros dados que pede lá e acesse a url do django admin por aqui para logar:

http://127.0.0.1:8000/admin/