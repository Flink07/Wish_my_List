from flask_app import app
#import routes
from flask_app.controllers import restaurants_controller, users_controller


if __name__ == "__main__":
    app.run(debug=True)