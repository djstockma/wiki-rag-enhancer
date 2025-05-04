# Wikipedia Checker – RAG Project

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

Start your local MariaDB server (refer to https://mariadb.com/get-started-with-mariadb/), then:

```
CREATE DATABASE ragdb;
CREATE USER 'raguser'@'localhost' IDENTIFIED BY 'ragpass';
GRANT ALL PRIVILEGES ON ragdb.* TO 'raguser'@'localhost';
FLUSH PRIVILEGES;
```
To load the schema:
```
mysql -u raguser -p ragdb < ../mariadb/init.sql
```
#### 4. Create .env in app/

You can base the .env off the .env.exaple, a valid api key for openAI is required

#### 5. Run the app
```
streamlit run app_ui.py
```
UI should now be accessible on http://localhost:8501

### Using the wiki-enhancer

1. Load wikipedia articles (from .csv currently)
2. Insert source text 
3. Specify number of chunks to be returned, choose n chunks from ONE article
4. Generate suggestions

