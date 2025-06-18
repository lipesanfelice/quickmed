# Projeto de Software 1 - Quickmed

![Imagem](Tela_site(2).png)

#### Desenvolvedor(a)

Francisco ALbrecht Ribas - Sistemas de Informação

Felipe Peripolli Sanfelice - Sistemas de Informação

#### Nosso Produto

O nosso produto tem 2 clientes alvo, primeiramente o úsuario que deseja encontar a clínica, hospital ou veterinária que corresponda a suas necessidades e um espaço onde possa guardar 
informações médicas. E não menos importante, os profissionais da área da saúde que precisam divulgar suas clínicas de forma clara, objetiva e simples. O sistema já está populado com 
informações de unidades básicas de saúde no Brasil.


##### Conteúdo:

O site tem uma pagína ínicial com um mapa focado na região mais próxima do usuário. A partir dela o usuário pode acessar a tela para fazer o registro ou login, se já tiver uma conta. 
No protótipo inicial, qualquer usuário pode criar uma "clínica", porém a ideia propósta é a de existirem dois tipos de usuários com roles diferentes e métodos de registro difirentes. 
O usuário logado pode acessar a suas "clínicas" para atualizar ou apagar, acessar as suas informações médicas para a atualizar, e criar uma nova "clínica". Após as interações o usuário 
pode deslogar.

##### Aparência:

O site tem uma aparencia simples com uma tonalidade com verde menta e branca

##### Código: 
O projeto foi desenvolvido com o microframework Flask para python e o Banco de Dados MySQL no Backend e PHP e Javascript para o Frontend, o deploy do projeto construido dentro do 
ambiente sandbox (para estudantes) da AWS onde foram estabelecidas a conexão entre o componente de Banco de Dados RBS(MySQL) e o componente EC2, onde o back e front foram hospedados,
através da arquitetura de networking da AWS. Dentro do componente EC2 está estabelecido um web server com Nginx que gerencia as requests como uma reverse proxy, além disso também foi 
necessario usar o WSGI, gunicorn, para servir de interface entre a aplicação python e nginx.

#### Desenvolvimento

O desenvolvimento foi desafidor, ambos os desenvolvedores aprenderam e lidaram com novas técnologias em um curto período de tempo, mas num todo a organização da equipe estava bem estabelecida com 
reuniões sobre o projeto frequentemente durante a semana.

#### Tecnologias
- Javascript
- PHP
- HTML e CSS
- Python - Flask
- MySQL DataBase
- Aws - SandBox

#### Ambiente de desenvolvimento
- VS Code
- GitHub
- AWS SANDBOX

#### Referências e créditos
- ChatGPT
- [Deploy](https://medium.com/@kawsarlog/from-flask-to-live-deploying-your-app-with-nginx-gunicorn-ssl-and-custom-domain-1e8b57709fc0)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [PHP](https://www.php.net/docs.php)
- [Unidades Básicas de Saúde UBS](https://www.arcgis.com/home/item.html?id=21fda7429717414caf7b436e1f2da868)
- [JavaScript](https://www.w3schools.com/js/js_intro.asp)

---
Projeto entregue para a disciplina de [Projeto de Software 2] em 2024b
