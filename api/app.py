import config

from flask         import Flask
from sqlalchemy    import create_engine
from flask_cors    import CORS

from model   import UserDao, StatusDao
from service import UserService, StatusService
from view    import create_endpoints

class Services:
    pass

################################
# Create App
################################
def create_app(test_config = None):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)

    ## Persistenace Layer
    user_dao  = UserDao(database)
    status_dao = StatusDao(database)
    
    ## Business Layer
    services = Services
    services.user_service  = UserService(user_dao, config)
    services.status_service = StatusService(status_dao)

    ## 엔드포인트들을 생성
    create_endpoints(app, services)

    return app

if __name__ == "__main__":
	app = create_app()
	app.run(host="0.0.0.0")
	
	
