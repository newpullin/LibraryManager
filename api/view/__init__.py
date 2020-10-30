import jwt

from flask      import request, jsonify, current_app, Response, g
from flask.json import JSONEncoder
from functools  import wraps

## Default JSON encoder는 set를 JSON으로 변환할 수 없다.
## 그럼으로 커스텀 엔코더를 작성해서 set을 list로 변환하여
## JSON으로 변환 가능하게 해주어야 한다.
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

#########################################################
#       Decorators
#########################################################
def login_required(f):      
    @wraps(f)                   
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization') 
        if access_token is not None:  
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256') 
            except jwt.InvalidTokenError:
                 payload = None     

            if payload is None: return Response(status=401)  

            user_id   = payload['user_id']  
            g.user_id = user_id
        else:
            return Response(status = 401)  

        return f(*args, **kwargs)
    return decorated_function

def create_endpoints(app, services):
    app.json_encoder = CustomJSONEncoder

    user_service  = services.user_service
    status_service = services.status_service

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user = request.json
        new_user = user_service.create_new_user(new_user)

        return jsonify(new_user)
        
    @app.route('/login', methods=['POST'])
    def login():
        credential = request.json
        authorized = user_service.login(credential) 

        if authorized:
            user_credential = user_service.get_user_id_and_password(credential['email'])
            user_id         = user_credential['id']
            token           = user_service.generate_access_token(user_id)

            return jsonify({
                'user_id'      : user_id,
                'access_token' : token
            })
        else:
            return '', 401
            
    @app.route('/userstatus', methods=['GET'])
    @login_required
    def userStatus():
        user_status = status_service.get_status(g.user_id)
        return jsonify({
            'status' : user_status
        })
    
    @app.route('/libraries', methods=['GET'])
    def libraries():
        libraries_list = status_service.get_libraries()
        return jsonify({
            'Libraries' : libraries_list
        })
    
    @app.route('/books', methods=['GET'])
    def books():
        book_list = status_service.get_books()
        return jsonify({
            'books': book_list
            })





