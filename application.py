from app import create_app



if __name__ == "__main__":
    from aiohttp.web import run_app
    from dotenv import load_dotenv
    load_dotenv()
    application = create_app()
    run_app(application)