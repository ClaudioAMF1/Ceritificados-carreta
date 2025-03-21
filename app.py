from app import create_app
from config.settings import PORT, DEBUG

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)