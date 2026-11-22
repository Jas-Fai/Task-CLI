import argparse
import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(title: str) -> None:
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")


def list_tasks() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        print(f"{t['id']}. {status} {t['title']}")


def complete_task(task_id: int) -> None:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Completed task #{task_id}")
            return
    print(f"Task #{task_id} not found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal CLI Task Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task description")

    sub.add_parser("list", help="List all tasks")

    done_p = sub.add_parser("done", help="Mark a task complete")
    done_p.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()
    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)


if __name__ == "__main__":
    main()
