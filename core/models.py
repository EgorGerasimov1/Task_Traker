import datetime
import uuid
import json

class Task:
    def __init__(self, task_text='', priority=0, id=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.task_text = task_text
        self.priority = priority
        self.date = datetime.date.today()
        self.done = False

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.task_text,
            'priority': self.priority,
            'date': str(self.date),
            'done': self.done
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(
            task_text = data.get('text', ''),
            priority = data.get('priority', 0)
        )
        task.id = data.get('id', task.id )
        task.date = data.get('date', task.date)
        task.done = data.get('done', task.done)
        return task
    
class TasksList:
    def __init__(self, file_name='tasks.json'):
        self.file_name = file_name
        self.tasks = []
        self.load()

    def load(self):
        try:
            with open(self.file_name, 'r', encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def append(self, text, priority=0):
        task = Task(text, priority)
        self.tasks.append(task)
        self.save()
        return task
    
    def edit(self, task_id, text, priority):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                task.task_text = text
                task.priority = priority
                self.save()
                return task
        return None

    def delete(self, delete_task_id):
        for i, task in enumerate(self.tasks):
            if task.id == delete_task_id:
                delete_task = self.tasks.pop(i)
                self.save()
                return delete_task
        return None

    def complete(self, complete_id):
        for i, task in enumerate(self.tasks):
            if task.id == complete_id:
                task.done = True
                self.save()
                return task
        return None

    def get_all(self):
        return self.tasks
    def get_active(self):
        return [task for task in self.tasks if not task.done]
    def get_completed(self):
        return [task for task in self.tasks if task.done]
    