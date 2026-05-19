"""SQLite-backed dict-shaped key-value store.

All rows are loaded into memory on startup and every mutation is mirrored to
disk in WAL mode. This is the minimum needed to let the Phase 3 façade and the
mock RP List survive a process restart — explicitly not a production database
layer.

Callers may mutate stored values *in place* (e.g. ``acct.status = "valid"``);
they must call ``store.save(key)`` afterwards so the change is persisted.
"""
from __future__ import annotations

import json
import os
import sqlite3
from typing import Any, Callable, Generic, Iterator, Optional, TypeVar

V = TypeVar("V")


class Store(Generic[V]):
    def __init__(
        self,
        db_path: str,
        table: str,
        to_dict: Callable[[V], dict],
        from_dict: Callable[[dict], V],
    ) -> None:
        self._table = table
        self._to_dict = to_dict
        self._from_dict = from_dict
        parent = os.path.dirname(db_path) or "."
        os.makedirs(parent, exist_ok=True)
        # isolation_level=None → autocommit; WAL → safe concurrent readers
        self._db = sqlite3.connect(db_path, check_same_thread=False,
                                   isolation_level=None)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute(
            f"CREATE TABLE IF NOT EXISTS {table} "
            "(k TEXT PRIMARY KEY, v TEXT NOT NULL)"
        )
        self._mem: dict[str, V] = {}
        for k, v in self._db.execute(f"SELECT k, v FROM {table}"):
            self._mem[k] = from_dict(json.loads(v))

    def __setitem__(self, key: str, value: V) -> None:
        self._mem[key] = value
        self._db.execute(
            f"INSERT OR REPLACE INTO {self._table} (k, v) VALUES (?, ?)",
            (key, json.dumps(self._to_dict(value))),
        )

    def save(self, key: str) -> None:
        """Re-persist a key after in-place mutation of its value."""
        if key not in self._mem:
            raise KeyError(key)
        self.__setitem__(key, self._mem[key])

    def __getitem__(self, key: str) -> V:
        return self._mem[key]

    def __delitem__(self, key: str) -> None:
        del self._mem[key]
        self._db.execute(f"DELETE FROM {self._table} WHERE k = ?", (key,))

    def __contains__(self, key: object) -> bool:
        return key in self._mem

    def __iter__(self) -> Iterator[str]:
        return iter(self._mem)

    def __len__(self) -> int:
        return len(self._mem)

    def get(self, key: str, default: Any = None) -> Optional[V]:
        return self._mem.get(key, default)

    def values(self) -> Iterator[V]:
        return iter(self._mem.values())
