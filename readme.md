# Wikipedia Checker – RAG Project

[![Mariadb](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](#)
[![Docker](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](#)
[![OpenAI](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)](#)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000)](#)

This project uses Retrieval-Augmented Generation (RAG) to compare real-world source articles to Wikipedia and suggest factual improvements. The project uses mariadb-vector as a vector database, and openai to for comparing the source to wikipedia data.

This project was a part of MariaDB AI_RAG hackathon.

## Requirements
Aside from packages in requirements.txt:
* Python 3.10+
* MariaDB (if running locally)
* pip or conda (if running locally)


## Project Setup

### Using Docker

1. Make sure Docker and Docker Compose are installed.
2. In the project root, run:

docker-compose up --build

3. Open the app in your browser: http://localhost:8501

### Manual Setup (No Docker)

#### 1. Create a virtual environment

With venv:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Or with Conda:
```
conda create -n wiki-checker python=3.10
conda activate wiki-checker
```
#### 2. Install Python dependencies
```
cd app
pip install -r requirements.txt
```
#### 3. Set up MariaDB

For this project to work, wou will need mariadb-server 11.7+ (for vector to be included).  
See https://mariadb.org/download for instructions on downloading the correct version
(remember to also $ sudo apt install libmariadb3 libmariadb-dev
)

With mariadb installed, run
```
sudo systemctl start mariadb`
sudo systemctl status mariadb
```
To Start and verify that mariadb is running


Then (optional), create a user for the project
```
CREATE DATABASE ragdb;
CREATE USER 'raguser'@'localhost' IDENTIFIED BY 'ragpass';
GRANT ALL PRIVILEGES ON ragdb.* TO 'raguser'@'localhost';
FLUSH PRIVILEGES;
```
To load the schema:
```
mysql -u raguser -p ragdb < ./mariadb/init.sql
```
#### 4. Create .env in app/

You can base the .env off the .env.exaple, a valid api key for openAI is required

#### 5. Run the app

The UI app runs using streamlit. Start it by running:
```
python -m streamlit run app_ui.py
```
UI should now be accessible on http://localhost:8501

### Using the wiki-enhancer

1. Load wikipedia articles (from .csv currently)
2. Insert source text 
3. Specify number of chunks to be returned, choose n chunks from ONE article
4. Generate suggestions

### License
This project is open source and available under the [MIT license](LICENSE)
