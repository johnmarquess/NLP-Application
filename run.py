from app import create_app

app = create_app('dev')  # or 'prod' or 'test'

if __name__ == "__main__":
    app.run()
