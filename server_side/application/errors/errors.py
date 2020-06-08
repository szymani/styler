from flask import jsonify, make_response, Blueprint

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    if _error.description is not "The browser (or proxy) sent a request that this server could not understand.":
        return make_response(jsonify({'error': _error.description}), 400)
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@error_handlers.app_errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@error_handlers.app_errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    if _error.description is not "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.":
        return make_response(jsonify({'error': _error.description}), 404)
    return make_response(jsonify({'error': 'Not found'}), 404)


@error_handlers.app_errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)
