from app import create_app, db
app = create_app("config")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    app.run(debug=True, ssl_context='adhoc')