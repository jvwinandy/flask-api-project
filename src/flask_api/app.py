from flask import Flask
import flask_api.db.database as db
from flask_api.routes.demandas import demandas_bp

app = Flask(__name__)
db.init_db()

app.register_blueprint(demandas_bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    app.run()
