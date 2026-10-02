# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License
from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Iterable


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(slots=True)
class Event:
    id: str
    timestamp: str
    source_ip: str
    source_port: int | None = None
    sensor: str = "unknown"
    event_type: str = "generic"
    severity: str = Severity.LOW.value
    details: dict[str, Any] = field(default_factory=dict)
    mitre_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "source_ip": self.source_ip,
            "source_port": self.source_port,
            "sensor": self.sensor,
            "event_type": self.event_type,
            "severity": self.severity,
            "details": self.details,
            "mitre_ids": self.mitre_ids,
        }


class EventBus:
    def __init__(self) -> None:
        self._subscribers: list[Callable[[Event], None]] = []
        self._queue: asyncio.Queue[Event] = asyncio.Queue()

    def subscribe(self, callback: Callable[[Event], None]) -> None:
        self._subscribers.append(callback)

    def publish(self, event: Event) -> None:
        self._queue.put_nowait(event)
        for callback in self._subscribers:
            try:
                callback(event)
            except Exception:
                pass

    async def consume(self) -> Event:
        return await self._queue.get()


class BaseSensor:
    def __init__(self, name: str, event_bus: EventBus | None = None) -> None:
        self.name = name
        self.event_bus = event_bus
        self._started = False

    def start(self) -> None:
        self._started = True

    def stop(self) -> None:
        self._started = False

    def on_event(self, event: Event) -> None:
        if self.event_bus is not None:
            self.event_bus.publish(event)


def make_event(
    *,
    source_ip: str,
    source_port: int | None = None,
    sensor: str,
    event_type: str,
    severity: str = Severity.LOW.value,
    details: dict[str, Any] | None = None,
    mitre_ids: Iterable[str] | None = None,
) -> Event:
    return Event(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        source_ip=source_ip,
        source_port=source_port,
        sensor=sensor,
        event_type=event_type,
        severity=severity,
        details=dict(details or {}),
        mitre_ids=list(mitre_ids or []),
    )
