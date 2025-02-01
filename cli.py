# cli.py

from task_manager import TaskManager

def display_tasks(tasks):
    """Display tasks in a readable format."""
    if tasks:
        for idx, task in enumerate(tasks, start=1):
            print(f"\nTask {idx}:")
            for key, value in task.items():
                print(f"  {key.capitalize()}: {value}")
            print("-" * 30)
    else:
        print("No tasks found.")

def main_menu():
    """Display the main menu and return the user's choice."""
    print("\nTaskFlow - Intelligent Task Prioritizer")
    print("1. Add Task")
    print("2. Edit Task")
    print("3. Delete Task")
    print("4. Mark Task as Completed")
    print("5. Search Tasks")
    print("6. Show Top Tasks")
    print("7. Exit")
    return input("Select an option (1-7): ").strip()

def run_cli():
    """Run the CLI loop to interact with the task manager."""
    manager = TaskManager()

    while True:
        choice = main_menu()

        if choice == "1":
            title = input("Enter task title: ").strip()
            try:
                priority = int(input("Enter priority (1-5): ").strip())
            except ValueError:
                print("Invalid priority. Please enter a number between 1 and 5.")
                continue
            due_date = input("Enter due date (YYYY-MM-DD): ").strip()
            try:
                effort = int(input("Enter effort (in hours): ").strip())
            except ValueError:
                print("Invalid effort. Please enter an integer value.")
                continue
            category = input("Enter category: ").strip()
            manager.add_task(title, priority, due_date, effort, category)
            print(f"Task '{title}' added successfully.")

        elif choice == "2":
            title = input("Enter the title of the task to edit: ").strip()
            print("Enter new values (leave blank to keep current value):")
            new_priority = input("New priority (1-5): ").strip()
            new_due_date = input("New due date (YYYY-MM-DD): ").strip()
            new_effort = input("New effort (in hours): ").strip()
            new_category = input("New category: ").strip()

            updates = {}
            if new_priority:
                try:
                    updates["priority"] = int(new_priority)
                except ValueError:
                    print("Invalid priority input. Skipping update for priority.")
            if new_due_date:
                updates["due_date"] = new_due_date
            if new_effort:
                try:
                    updates["effort"] = int(new_effort)
                except ValueError:
                    print("Invalid effort input. Skipping update for effort.")
            if new_category:
                updates["category"] = new_category

            if updates and manager.edit_task(title, **updates):
                print("Task updated successfully.")
            else:
                print("Task not found or no valid updates provided.")

        elif choice == "3":
            title = input("Enter the title of the task to delete: ").strip()
            if manager.delete_task(title):
                print(f"Task '{title}' deleted successfully.")
            else:
                print("Task not found.")

        elif choice == "4":
            title = input("Enter the title of the task to mark as completed: ").strip()
            if manager.mark_task_completed(title):
                print(f"Task '{title}' marked as completed.")
            else:
                print("Task not found.")

        elif choice == "5":
            keyword = input("Enter a keyword to search: ").strip()
            results = manager.search_tasks(keyword)
            display_tasks(results)

        elif choice == "6":
            top_tasks = manager.get_top_tasks()
            print("\nTop Tasks:")
            display_tasks(top_tasks)

        elif choice == "7":
            print("Exiting TaskFlow. Goodbye!")
            break

        else:
            print("Invalid option. Please select a number between 1 and 7.")
