# task_manager.py

import json
import datetime
import heapq

class Task:
    def __init__(self, title, priority, due_date, effort, category, completed=False):
        """
        Initialize a task.
        :param title: Task title.
        :param priority: Task priority (1-low to 5-high).
        :param due_date: Due date in YYYY-MM-DD format.
        :param effort: Estimated effort in hours.
        :param category: Task category.
        :param completed: Task completion status.
        """
        self.title = title
        self.priority = priority
        self.due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")
        self.effort = effort
        self.category = category
        self.completed = completed
        self.score = self.calculate_score()

    def calculate_score(self):
        """Calculate a task score based on priority, due date, and effort.
           Completed tasks have a score of 0.
        """
        if self.completed:
            return 0
        days_left = (self.due_date - datetime.datetime.now()).days
        urgency_factor = max(1, 10 - days_left)
        return self.priority * urgency_factor - self.effort

    def to_dict(self):
        """Return task details as a dictionary for JSON storage."""
        return {
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "effort": self.effort,
            "category": self.category,
            "completed": self.completed,
            "score": self.score
        }

    def update(self, **kwargs):
        """Update task attributes and recalculate score."""
        for key, value in kwargs.items():
            if key == "due_date":
                setattr(self, key, datetime.datetime.strptime(value, "%Y-%m-%d"))
            else:
                setattr(self, key, value)
        self.score = self.calculate_score()


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []  # We'll store tuples: (-score, task) for a max-heap
        self.load_tasks()

    def add_task(self, title, priority, due_date, effort, category):
        task = Task(title, priority, due_date, effort, category)
        heapq.heappush(self.tasks, (-task.score, task))
        self.save_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                for task_data in data:
                    # Ensure the 'completed' field exists
                    if "completed" not in task_data:
                        task_data["completed"] = False
                    task = Task(**task_data)
                    heapq.heappush(self.tasks, (-task.score, task))
        except FileNotFoundError:
            # File will be created when saving if it doesn't exist
            pass

    def save_tasks(self):
        """Save all tasks to the JSON file."""
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for _, task in self.tasks], file, indent=4)

    def get_top_tasks(self, count=5):
        """Return a list of the top tasks (by score)."""
        return [task.to_dict() for _, task in heapq.nsmallest(count, self.tasks)]

    def mark_task_completed(self, title):
        """Mark the first task with the given title as completed."""
        for idx, (neg_score, task) in enumerate(self.tasks):
            if task.title.lower() == title.lower():
                task.completed = True
                task.score = task.calculate_score()
                self.tasks[idx] = (-task.score, task)
                heapq.heapify(self.tasks)
                self.save_tasks()
                return True
        return False

    def delete_task(self, title):
        """Delete the first task with the given title."""
        for idx, (neg_score, task) in enumerate(self.tasks):
            if task.title.lower() == title.lower():
                del self.tasks[idx]
                heapq.heapify(self.tasks)
                self.save_tasks()
                return True
        return False

    def edit_task(self, title, **kwargs):
        """
        Edit an existing task identified by title.
        Pass updated fields as keyword arguments (e.g., priority=4, due_date="2025-02-15").
        """
        for idx, (neg_score, task) in enumerate(self.tasks):
            if task.title.lower() == title.lower():
                task.update(**kwargs)
                self.tasks[idx] = (-task.score, task)
                heapq.heapify(self.tasks)
                self.save_tasks()
                return True
        return False

    def search_tasks(self, keyword):
        """Search for tasks that contain the keyword in the title or category."""
        results = []
        keyword_lower = keyword.lower()
        for _, task in self.tasks:
            if keyword_lower in task.title.lower() or keyword_lower in task.category.lower():
                results.append(task.to_dict())
        return results
