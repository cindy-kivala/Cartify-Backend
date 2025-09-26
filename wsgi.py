from server.app import create_app

# Instantiate the Flask app
app = create_app()

if __name__ == "__main__":
    app.run()
