from flask_restful import Resource, reqparse
from models import Task, db

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help="Title cannot be blank!")
parser.add_argument('description', type=str)
parser.add_argument('done', type=bool)

class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return {"id": task.id, "title": task.title, "description": task.description, "done": task.done}

    def put(self, task_id):
        data = parser.parse_args()
        task = Task.query.get_or_404(task_id)
        task.title = data['title']
        task.description = data.get('description')
        task.done = data.get('done', task.done)
        db.session.commit()
        return {"message": "Task updated successfully"}, 200

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}, 200

class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return [{"id": task.id, "title": task.title, "description": task.description, "done": task.done} for task in tasks]

    def post(self):
        data = parser.parse_args()
        task = Task(title=data['title'], description=data.get('description'), done=data.get('done', False))
        db.session.add(task)
        db.session.commit()
        return {"message": "Task created successfully"}, 201
