from app import create_app
from app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)  # 'config.DevelopmentConfig

if __name__ == '__main__':
    app.run()
