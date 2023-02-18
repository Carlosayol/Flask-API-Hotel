from src.app import create_app

if __name__ == "__main__":
    """
    hotelapi - API for managing hotel data
    """
    app = create_app()
    app.run(host='0.0.0.0', port=5000)