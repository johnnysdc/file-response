## POC Django para fazer envio de arquivos locais e armazenados no sqlite

Usando o BinaryField do Django para armazenar os binários no banco de dados.
Os dados enviados no POST são convertidos e salvos no sqlite.
Após salvar essas informações é possivel obter os arquivos scaler e modelo

Ainda falta implementar muitas coisas mas a prova de conceito está funcionando

## Comando úteis powershell:

### Cria ambiente virtual para o instalar as dependências do projeto

* `python -m venv .env`
* `.\.env\Scripts\activate`

### Instalar as dependências do projeto 

* `pip install -r .\requirements.txt`

### Acessar o diretório com o codigo fonte: 

* `cd .\src\`

### Criar banco de dados sqlite (necessário rodar pelo menos uma vez)

* `python .\manage.py makemigrations`
* `python .\manage.py migrate`

### Realiza o build e executa o servidor 

* `python .\manage.py runserver`

### Diretório que falta ser criado com os arquivos de modelo

* `src\files\analisadores\<tagName>\files.etc`
