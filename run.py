from app import create_app

app = create_app()


# The host and post is changed to http://localhost:8000
if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
