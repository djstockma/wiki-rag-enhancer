## Git wiki enhancer

This solution uses RAG to analyze whether a source or text could be used to enhance the knowledge base of wikipedia.

### Components:



### Running:
For now: either install dependancies locally:
```
pip install --no-cache-dir -r requirements.txt
```

Amd then simply run:
```
python main.py
```

OR run it in docker using:
```
Docker-compose up --build
```

Warning: the library sentence-transformers is quite and contains a fair amount of other dependencies. Consider using something like venv for development!

