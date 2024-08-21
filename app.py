from flask import Flask
from flask_restful import Api
from models import db, Task
from resources.task import TaskResource, TaskListResource # type: ignore
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

api = Api(app)
api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
