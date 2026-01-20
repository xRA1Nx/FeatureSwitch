from __future__ import annotations

import enum


class HealthCheckReason(enum.Enum):
    KAFKA = "KAFKA"
    DATABASE = "DATABASE"
