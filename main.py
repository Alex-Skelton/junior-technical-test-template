from app import create_app, configure_logging


app = create_app()
configure_logging()


if __name__ == '__main__':
    configure_logging()
    app = create_app()
    app.run(debug=True)