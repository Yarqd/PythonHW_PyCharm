#!/usr/bin/env python3
"""
ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ (curl):

1) Создание задачи:
   curl -X POST http://127.0.0.1:8080/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Gym","priority":"low"}'

2) Получение списка задач:
   curl http://127.0.0.1:8080/tasks

3) Отметка задачи как выполненной:
   curl -X POST http://127.0.0.1:8080/tasks/1/complete

После каждого изменения файл tasks.txt автоматически сохраняется.
При перезапуске сервера данные восстанавливаются из tasks.txt.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    id: int
    title: str
    priority: str  # low | normal | high
    isDone: bool


class TaskStore:
    """
    Хранилище задач + загрузка/сохранение в файл tasks.txt (JSON).
    Сохраняем ВСЁ после каждого запроса, который меняет список задач.
    """

    _ALLOWED_PRIORITIES = {"low", "normal", "high"}

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._lock = Lock()
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self._load_from_file_if_exists()

    def list_tasks(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [asdict(t) for t in self._tasks]

    def create_task(self, title: str, priority: str) -> Dict[str, Any]:
        title = (title or "").strip()
        priority = (priority or "").strip().lower()

        if not title:
            raise ValueError("title must be non-empty")
        if priority not in self._ALLOWED_PRIORITIES:
            raise ValueError("priority must be one of: low, normal, high")

        with self._lock:
            task = Task(id=self._next_id, title=title, priority=priority, isDone=False)
            self._tasks.append(task)
            self._next_id += 1
            self._save_to_file()
            return asdict(task)

    def complete_task(self, task_id: int) -> bool:
        with self._lock:
            for t in self._tasks:
                if t.id == task_id:
                    t.isDone = True
                    self._save_to_file()
                    return True
            return False

    def _load_from_file_if_exists(self) -> None:
        if not self._file_path.exists():
            return

        try:
            raw = self._file_path.read_text(encoding="utf-8").strip()
            if not raw:
                return

            data = json.loads(raw)
            if not isinstance(data, list):
                return

            tasks: List[Task] = []
            max_id = 0

            for item in data:
                if not isinstance(item, dict):
                    continue
                try:
                    tid = int(item.get("id"))
                    title = str(item.get("title", "")).strip()
                    priority = str(item.get("priority", "")).strip().lower()
                    is_done = bool(item.get("isDone"))
                except Exception:
                    continue

                if not title or priority not in self._ALLOWED_PRIORITIES or tid <= 0:
                    continue

                tasks.append(Task(id=tid, title=title, priority=priority, isDone=is_done))
                max_id = max(max_id, tid)

            self._tasks = tasks
            self._next_id = max_id + 1

        except Exception:
            # Если файл битый — не падаем, стартуем с пустым списком
            self._tasks = []
            self._next_id = 1

    def _save_to_file(self) -> None:
        data = [asdict(t) for t in self._tasks]
        self._file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def read_json_body(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    length_str = handler.headers.get("Content-Length")
    if not length_str:
        return {}
    try:
        length = int(length_str)
    except ValueError:
        return {}

    raw = handler.rfile.read(length)
    if not raw:
        return {}

    try:
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def send_json(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def send_empty(handler: BaseHTTPRequestHandler, status: int) -> None:
    handler.send_response(status)
    handler.send_header("Content-Length", "0")
    handler.end_headers()


def parse_complete_path(path: str) -> Optional[int]:
    """
    Ожидаем: /tasks/<id>/complete
    """
    m = re.fullmatch(r"/tasks/(\d+)/complete", path)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def make_handler(store: TaskStore):
    class TasksHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/tasks":
                tasks = store.list_tasks()
                send_json(self, 200, tasks)
                return
            send_empty(self, 404)

        def do_POST(self) -> None:
            if self.path == "/tasks":
                data = read_json_body(self)
                title = data.get("title")
                priority = data.get("priority")

                try:
                    task = store.create_task(str(title), str(priority))
                except ValueError as e:
                    send_json(self, 400, {"error": str(e)})
                    return

                send_json(self, 200, task)
                return

            task_id = parse_complete_path(self.path)
            if task_id is not None:
                ok = store.complete_task(task_id)
                send_empty(self, 200 if ok else 404)
                return

            send_empty(self, 404)

        # чуть тише лог в консоли (по желанию)
        def log_message(self, format: str, *args: Any) -> None:
            return

    return TasksHandler


def run_server(host: str, port: int, storage_file: Path) -> None:
    store = TaskStore(storage_file)
    handler_cls = make_handler(store)
    httpd = ThreadingHTTPServer((host, port), handler_cls)
    print(f"Server started: http://{host}:{port}")
    print(f"Storage file: {storage_file}")
    httpd.serve_forever()


def main() -> None:
    # По условию сохраняем в tasks.txt. Удобно держать рядом со скриптом.
    storage = Path(__file__).resolve().parent / "tasks.txt"
    run_server(host="127.0.0.1", port=8080, storage_file=storage)


if __name__ == "__main__":
    main()