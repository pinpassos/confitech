- Instale o redis em sua máquina
Ubuntu - abra o terminal e ditite o comando sudo apt-get install redis
Windows - https://redis.io/docs/getting-started/installation/install-redis-on-windows/ (Como o passo é um pouco mais longo, é melhor se basear na própia documentação)

- Para que possamos instalar as dependências do nosso projeto, primeiro vamos criar uma virtualenv
Abra o terminal, caminhe até o diretório onde deseja criar sua venv e digite o comando python3 -m venv nome-da-sua-env
Após o passo anterior devemos informar que queremos trabalhar com esta venv e para isso iremos digitar no terminal:
Windows: venv\Scripts\activate
Ubuntu: source venv/bin/activate

- Estando dentro da venv, caminhe até o diretório raíz do projeto e dentro do terminal digte o comando pip install -r requirements.txt
feito isso todas as dependências utilizadas no projeto estarão instaladas em sua venv.

Após configurar seu dynamoDB, instale a CLI da aws para que possa prover as chaves de segurança para que o boto3 funcione corretamente:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html


No diretório api/Geniusapi.py, contém uma variável protegida com dotenv, para que você possa ter acesso a uma, precisa ter um token de acesso que pode ser gerado em: https://genius.com/api-clients
Após isso, crie um arquivo no diretório raíz do projeto com o nome de .env e adicione: ACCESS_TOKEN=Bearer YOUR-CLIENT-ACCESS-TOKEN. Em tese ela já deev ser adicionada ao header da classe para a conexão com a API da Genius

- Para iniciar nosso servidor, navegue até o diretório de seu projeto e informe ao terminal o aplicativo com o qual quer trabalhar exportando a variável de ambiente
FLASK_APP. Digite no terminal export FLASK_APP=main.py

- Inicie o servidor digitando no terminal: flask run

- Para pesquisar por um artista basta passar um numero na url:
Exemplo de consulta: http://127.0.0.1:5000/16775/
Sugestões - 2300 / 78010 / 16775 / 250


# ==================================== #
Quando iniciamos o servidor pela primeira vez e passamos um id pela url, nossa apliacação faz uma requisição à API da Genius já que nosso redis ainda não possui nenhum dado armazenado em cache.
Quando essa primeira requisição por um artista é feita, ele salva essa transação no formato do nosso banco de dados do dynamoDB e também armazena esses dados em cache no redis.
Se pesquisarmos novamente por esse mesmo artista a resposta da requisição vem diretamente do cache do redis.
# ==================================== #
