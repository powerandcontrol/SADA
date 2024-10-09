<div align="center">

  <img src="static/logo-unirio.png" alt="logo" width="60" height="auto" />
  <h1>Unihelp</h1>
  
  <p>
    Frase de efeito
  </p>
  
  
<!-- Badges -->
<p>
  <a href="https://github.com/powerandcontrol/unihelp/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/powerandcontrol/unihelp" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/powerandcontrol/unihelp" alt="last update" />
  </a>
  <a href="https://github.com/powerandcontrol/unihelp/network/members">
    <img src="https://img.shields.io/github/forks/powerandcontrol/unihelp" alt="forks" />
  </a>
  <a href="https://github.com/powerandcontrol/unihelp/stargazers">
    <img src="https://img.shields.io/github/stars/powerandcontrol/unihelp" alt="stars" />
  </a>
  <a href="https://github.com/powerandcontrol/unihelp/issues/">
    <img src="https://img.shields.io/github/issues/powerandcontrol/unihelp" alt="open issues" />
  </a>
  <a href="https://github.com/powerandcontrol/unihelp/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/powerandcontrol/unihelp.svg" alt="license" />
  </a>
</p>
   
<!--
<h4>
    <a href="https://github.com/Louis3797/awesome-readme-template/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template">Documentation</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">Request Feature</a>
</h4>
-->

</div>

<!-- Sumário 
# 📔 Sumário

- [Sobre](#star2-sobre)
  * [Screenshots](#camera-screenshots)
  * [Tech Stack](#space_invader-tech-stack)
  * [Features](#dart-features)
  * [Color Reference](#art-color-reference)
  * [Environment Variables](#key-environment-variables)
- [Getting Started](#toolbox-getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Installation](#gear-installation)
  * [Running Tests](#test_tube-running-tests)
  * [Run Locally](#running-run-locally)
  * [Deployment](#triangular_flag_on_post-deployment)
- [Usage](#eyes-usage)
- [Roadmap](#compass-roadmap)
- [Contributing](#wave-contributing)
  * [Code of Conduct](#scroll-code-of-conduct)
- [FAQ](#grey_question-faq)
- [License](#warning-license)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)


-->

<br>

## 🌟 Sobre

O SADA é um site pensado para auxiliar todos os estudantes do curso de Sistemas de Informação que se sentem perdidos na hora de organizar a sua grade curricular.

Nosso objetivo é criar telas de visualização de dados que possam auxiliar esses alunos na hora da criação da grade de horários.

### 📷 Tela Inicial

<div align="center"> 
  <img src="static/screenshot.jpg" alt="screenshot" />
</div>

<!-- TechStack -->
### 👾 Tecnologias Utilizadas

O SADA é uma solução web que utiliza `HTML`, `CSS` e `Javascript` para o Front-End da aplicação, enquanto o Back-End fica por conta do `Python` e do seu framework web `Flask`. 

O SGBD escolhido para fazer a criação e manutenção do Banco de Dados foi o `SQLite`, devido a sua integração com a biblioteca do Python `SQLAlchemy`.

#### Linguagens, Bibliotecas e Frameworks
<p>
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57.svg?style=for-the-badge&logo=SQLite&logoColor=white"/>
<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=for-the-badge&logo=HTML5&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6.svg?style=for-the-badge&logo=CSS3&logoColor=white"/>
<img src="https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=for-the-badge&logo=JavaScript&logoColor=black"/>
<img src="https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white"/>
<img src="https://img.shields.io/badge/pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white"/>
</p>

### 🎯 Funcionalidades

- Upload de Histórico
- Análise de Progresso Curricular
- Visualização de dados

<!-- Color Reference -->
### 🎨 Paleta de Cores

| Cor             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Cor Principal | ![#08415C](https://via.placeholder.com/10/08415C?text=+) #08415C |
| Cor Secundária | ![#FFFFFF](https://via.placeholder.com/10/FFFFFF?text=+) #FFFFFF |
| Cor de Destaque | ![#CC2936](https://via.placeholder.com/10/CC2936?text=+) #CC2936 |
| Text Color | ![#000000](https://via.placeholder.com/10/000000?text=+) #000000 |

<br>

## 🖥️ Ambiente de desenvolvimento

### 🐍 Pré-Requisitos

Esse website é uma solução em Python, então antes de tudo é necessário baixar a linguagem de programação no <a href="https://www.python.org/downloads/"> site oficial </a>.

O segundo requisito necessário é o Git, que gerencia o controle de versionamento do projeto. Um tutorial de como instalar e começar a usar o Git pode ser encontrado no <a href="https://git-scm.com/downloads"> site oficial </a> da ferramenta.

### 🧰 Clonando o projeto

Tendo ambos os Pré-Requitos instalados no seu computador, você já consegue rodar o projeto localmente.

O primeiro passo é clonar o projeto na sua pasta de preferência.

```bash
git clone https://github.com/powerandcontrol/unihelp.git
```

### 🔑 Ambiente virtual

Para rodar esse projeto você precisará criar um ambiente virtual `venv` dentro da pasta do Unihelp.

```bash
  cd unihelp
  python -m venv venv
```

E, depois de criado, será necessário ativá-lo.

```bash
  venv\scripts\activate
```

### ⚙️ Instalando as Bibliotecas

As bibliotecas necessárias podem ser encontradas no arquivo `requirements.txt` e conseguimos baixar elas usando o gerenciador de pacotes `pip`.

```bash
  pip install -r requirements.txt
```
   
<!-- Running Tests -->
### 🧪 Rodando Localmente

Tendo seguido todos os passos anteriores você pode rodar o projeto sem maiores problemas usando o comando:

```bash
  python app.py
```

<!-- Deployment
### 🚩 Deployment

To deploy this project run

```bash
  yarn deploy
```
 -->

<br>

## 👀 Como usar o site?

Ao abrir a tela inicial, você deve preencher três inputs principais:

- <b>Currículo:</b> escolher entre o currículo antigo 2008.1 ou o atual 2023.2 (de acordo com a sua grade curricular atual)

- <b>Tipo do Histórico:</b> escolher qual tipo de histórico você baixou pelo Portal do Aluno (CR Aprovado entre o currículo antigo 2008.1 ou o atual 2023.2 (de acordo com a sua grade curricular atual)

- <b>Período:</b> escolher o período que você está cursando no período atual.


<!--
```javascript
import Component from 'my-project'

function App() {
  return <Component />
}
```

 Roadmap 
## 🧭 Roadmap

* [x] Todo 1
* [ ] Todo 2

-->
<!-- Contributing -->

<br>

## 👋 Contribuidores

<a href="https://github.com/powerandcontrol/unihelp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=powerandcontrol/unihelp" />
</a>

<br>

<!--
Contributions are always welcome!

See `contributing.md` for ways to get started.


### 📜 Code of Conduct

Please read the [Code of Conduct](https://github.com/Louis3797/awesome-readme-template/blob/master/CODE_OF_CONDUCT.md)

## ❔ FAQ

- Question 1

  + Answer 1

- Question 2

  + Answer 2

-->

## ⚠️ Licensa
Licensa MIT.


<!--
## 🤝 Contato

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/Louis3797/awesome-readme-template](https://github.com/Louis3797/awesome-readme-template)


## 💎 Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

 - [Shields.io](https://shields.io/)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md#travel--places)
 - [Readme Template](https://github.com/othneildrew/Best-README-Template)
-->
