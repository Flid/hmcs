from .app import app
from flask import jsonify


class BaseHMCSException(Exception):
    code = 'internal'
    status_code = 500

    def to_dict(self):
        return {
            'code': self.code,
        }


class ValidationError(BaseHMCSException):
    code = 'invalid_form'
    status_code = 400

    def __init__(self, errors):
        self._errors = errors

    def to_dict(self):
        response = super().to_dict()
        response['details'] = self._errors
        return response


@app.errorhandler(BaseHMCSException)
def handle_invalid_usage(error):
    response = jsonify({
        'status': 'error',
        'error': error.to_dict(),
    })
    response.status_code = error.status_code
    return response
