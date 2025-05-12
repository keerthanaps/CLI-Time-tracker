import json
import os
from datetime import datetime
import argparse

DATA_FILE = "tracker_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"active_task": None, "logs": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def start_task(task_name):
    data = load_data()
    if data["active_task"]:
        print("A task is already running.")
        return
    data["active_task"] = {
        "name": task_name,
        "start": datetime.now().isoformat()
    }
    save_data(data)
    print(f"Started task: {task_name}")

def stop_task():
    data = load_data()
    if not data["active_task"]:
        print("No active task to stop.")
        return
    task = data["active_task"]
    task["end"] = datetime.now().isoformat()
    task["duration"] = (
        datetime.fromisoformat(task["end"]) - datetime.fromisoformat(task["start"])
    ).total_seconds()
    data["logs"].append(task)
    data["active_task"] = None
    save_data(data)
    print(f"Stopped task: {task['name']} | Duration: {task['duration']//60:.0f} min")

def show_status():
    data = load_data()
    task = data["active_task"]
    if task:
        print(f"Active task: {task['name']} (started at {task['start']})")
    else:
        print("No active task.")

def show_report():
    data = load_data()
    if not data["logs"]:
        print("No tasks logged yet.")
        return
    print("\nTask History:")
    for t in data["logs"]:
        minutes = t["duration"] // 60
        print(f"- {t['name']}: {minutes:.0f} min")

def main():
    parser = argparse.ArgumentParser(description="CLI Time Tracker")
    parser.add_argument("command", choices=["start", "stop", "status", "report"])
    parser.add_argument("--task", help="Task name (required for start)")
    args = parser.parse_args()

    if args.command == "start":
        if not args.task:
            print("Please provide a task name with --task")
            return
        start_task(args.task)
    elif args.command == "stop":
        stop_task()
    elif args.command == "status":
        show_status()
    elif args.command == "report":
        show_report()

if __name__ == "__main__":
    main()
