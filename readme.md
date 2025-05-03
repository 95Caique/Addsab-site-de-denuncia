Sistema de Denúncias - ADDSAB

Requisitos
Docker
Docker Compose
Configuração Inicial
1. Clone o repositório
bash
git clone git@github.com:95Caique/Addsab-site-de-denuncia.git
cd Addsab-site-de-denuncia
2. Configure o arquivo de ambiente
Crie um arquivo .env na raiz do projeto a partir do exemplo fornecido:

bash
cp .env.example .env
O arquivo .env já vem configurado com valores padrão para desenvolvimento, mas você pode personalizar conforme necessário.

Executando o Projeto
Iniciar em modo de desenvolvimento

bash
docker compose up
Para executar em segundo plano (modo detached):

bash
docker-compose up -d
Acessar o sistema
Após a inicialização bem-sucedida, o sistema estará disponível em:

http://localhost:8000/ ou
http://127.0.0.1:8000/
Parar os containers
Para parar os containers mantendo os dados:

bash
docker-compose down
Para parar e remover volumes (apaga o banco de dados):

bash
docker-compose down -v
Comandos Úteis
Executar migrações manualmente
bash
docker-compose exec web python manage.py migrate
Criar um superusuário
bash
docker-compose exec web python manage.py createsuperuser
Coletar arquivos estáticos
bash
docker-compose exec web python manage.py collectstatic --noinput
Acessar o shell do Django
bash
docker-compose exec web python manage.py shell
Ver logs dos containers
bash
docker-compose logs
Para acompanhar logs em tempo real:

bash
docker-compose logs -f
Estrutura do Projeto
O projeto utiliza SQLite para simplificar o desenvolvimento. Os principais arquivos de configuração Docker são:

docker-compose.yml: Define os serviços e volumes do Docker
Dockerfile: Define como a imagem do container é construída
.env: Contém variáveis de ambiente para configuração do projeto
Desenvolvimento
Todos os arquivos do projeto são montados como volumes no container Docker, o que significa que qualquer alteração feita nos arquivos locais será refletida automaticamente no container sem necessidade de reconstruir a imagem.

O servidor Django é executado com o auto-reloader habilitado, então ele reiniciará automaticamente quando detectar alterações no código.

Solução de Problemas
Container não inicia
Verifique se as portas necessárias estão disponíveis:

bash
sudo lsof -i :8000
Alterações não aparecem
Algumas alterações podem exigir a reinicialização do container:

bash
docker-compose restart web
Erros de permissão
Se encontrar erros de permissão ao criar arquivos, pode ser necessário ajustar as permissões:

bash
sudo chown -R $USER:$USER .
Problemas com SQLite
Se o banco de dados SQLite estiver corrompido, você pode removê-lo e recriá-lo:

bash
rm db.sqlite3
docker-compose up
Produção
Para ambientes de produção, recomenda-se:

Modificar o .env para definir DEBUG=False
Configurar um banco de dados PostgreSQL (descomentando o serviço db no docker-compose.yml)
Usar um servidor WSGI como Gunicorn ou uWSGI
Configurar um proxy reverso como Nginx
Contribuindo
Crie um fork do projeto
Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
Faça commit das alterações (git commit -m 'Adiciona nova funcionalidade')
Faça push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request
