from flask import Flask
from routes.web_scraping import web_scraping_bp
from routes.tratamento_dados import tratamento_dados_bp
from routes.banco_dados import execucao_processamento_bp

app = Flask(__name__)

# Equivalente ao teste 1 
app.register_blueprint(web_scraping_bp)

# Equivalente ao teste 2
app.register_blueprint(tratamento_dados_bp)

# Equivalente ao teste 3 
app.register_blueprint(execucao_processamento_bp)

if __name__ == '__main__':
    app.run(debug=True)