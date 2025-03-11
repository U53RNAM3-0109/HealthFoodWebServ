from app import WholeHealthWebServ

if __name__ == "__main__":
    # App is being run directly, consider this a development environment

    app = WholeHealthWebServ(__name__, 'http://127.0.0.1:8080')
    app.run(debug=True, port=5000)
else:
    # App is being run as app.py, having been imported by another program
    # Consider this the production environment of the Azure API Server.

    from os import environ

    api_url = environ.get("api_uri")

    app = WholeHealthWebServ(__name__, api_url)
