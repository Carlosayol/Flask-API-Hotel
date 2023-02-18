from flask import Flask

def create_app():
  """
  Generate flask object
  returns: Flask instace
  """
  app = Flask(__name__)

  return app