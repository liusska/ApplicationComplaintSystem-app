
from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError

from db import db
from config import create_app


app = create_app()


@app.before_first_request
def init_request():
    db.init_app(app)


@app.after_request
def conclude_request(resp):
    try:
        db.session.commit()
    except Exception as ex:
        if ex.orig.pgcode == UNIQUE_VIOLATION:
            raise BadRequest('Please login')
        raise InternalServerError('Server is unavailable. Please try again later')
    return resp


if __name__ == '__main__':
    app.run()