from __future__ import annotations

from typing import Any

from backend.exceptions import InvalidAPIUsage


class TodoCustomSerializer:
    def __init__(self, todos: list[Any] | tuple[Any]):
        self.todos = todos

    def get_todos(self) -> list[dict[str | int]]:
        results = []
        for i in range(len(self.todos)):
            todo = {
                "id": self.todos[i][0],
                "title": self.todos[i][1],
                "description": self.todos[i][2],
                "created_at": self.todos[i][3].isoformat(),
            }
            results.append(todo)

        return results

    def get_todo(self) -> dict[str | int]:
        if self.todos is None:
            raise InvalidAPIUsage("Todo not found", status_code=404)
        todo = {
            "id": self.todos[0],
            "title": self.todos[1],
            "description": self.todos[2],
            "created_at": self.todos[3].isoformat(),
        }
        return todo
