"""Deterministic weighted-graph trace used by the teaching visual and tests."""

from __future__ import annotations

import heapq
import math
from typing import Any


class GraphValidationError(ValueError):
    """Raised when a teaching graph cannot be evaluated safely."""


def _finite_number(value: Any, field_name: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GraphValidationError(f"{field_name} must be numeric")
    if not math.isfinite(value):
        raise GraphValidationError(f"{field_name} must be finite")
    return value


def _build_adjacency(graph: dict[str, Any]) -> tuple[list[str], dict[str, dict[str, float]]]:
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not nodes:
        raise GraphValidationError("graph.nodes must be a non-empty list")
    if not isinstance(edges, list):
        raise GraphValidationError("graph.edges must be a list")

    node_ids: list[str] = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            raise GraphValidationError("each node must have a string id")
        node_id = node["id"].strip()
        if not node_id or node_id in node_ids:
            raise GraphValidationError("node ids must be non-empty and unique")
        node_ids.append(node_id)

    adjacency: dict[str, dict[str, float]] = {node_id: {} for node_id in node_ids}
    for edge in edges:
        if not isinstance(edge, dict):
            raise GraphValidationError("each edge must be an object")
        source = edge.get("from")
        target = edge.get("to")
        if source not in adjacency or target not in adjacency:
            raise GraphValidationError("each edge must connect known nodes")
        weight = _finite_number(edge.get("weight"), "edge.weight")
        if weight < 0:
            raise GraphValidationError("this teaching visual requires non-negative weights")

        previous_weight = adjacency[source].get(target)
        if previous_weight is None or weight < previous_weight:
            adjacency[source][target] = weight
            adjacency[target][source] = weight

    return node_ids, adjacency


def _distance_for_payload(distance: float) -> int | float | None:
    if math.isinf(distance):
        return None
    if float(distance).is_integer():
        return int(distance)
    return distance


def shortest_path_trace(
    graph: dict[str, Any],
    start: str,
    goal: str,
) -> dict[str, Any]:
    """Return Dijkstra's reachable state after each settlement.

    The trace is produced from the current graph on every request. It is not a
    prerecorded animation. Negative edges are rejected because the visual is
    specifically teaching the non-negative invariant.
    """

    node_ids, adjacency = _build_adjacency(graph)
    if start not in adjacency or goal not in adjacency:
        raise GraphValidationError("start and goal must be known node ids")

    distances: dict[str, float] = {node_id: math.inf for node_id in node_ids}
    predecessors: dict[str, str] = {}
    distances[start] = 0
    unsettled = set(node_ids)
    settled: list[str] = []

    steps: list[dict[str, Any]] = [
        {
            "current": None,
            "settled": [],
            "distances": {
                node_id: _distance_for_payload(distances[node_id])
                for node_id in node_ids
            },
            "relaxations": [],
        }
    ]

    if start != goal:
        while unsettled:
            current = None
            best_distance = math.inf
            for node_id in sorted(unsettled):
                if distances[node_id] < best_distance:
                    best_distance = distances[node_id]
                    current = node_id

            if current is None or math.isinf(best_distance):
                break

            unsettled.remove(current)
            settled.append(current)
            relaxations: list[dict[str, Any]] = []

            if current != goal:
                for neighbor in sorted(adjacency[current]):
                    if neighbor not in unsettled:
                        continue
                    weight = adjacency[current][neighbor]
                    previous_distance = distances[neighbor]
                    candidate = best_distance + weight
                    if candidate < previous_distance:
                        distances[neighbor] = candidate
                        predecessors[neighbor] = current
                        relaxations.append(
                            {
                                "from": current,
                                "to": neighbor,
                                "weight": _distance_for_payload(weight),
                                "previous": _distance_for_payload(previous_distance),
                                "distance": _distance_for_payload(candidate),
                            }
                        )

            steps.append(
                {
                    "current": current,
                    "settled": list(settled),
                    "distances": {
                        node_id: _distance_for_payload(distances[node_id])
                        for node_id in node_ids
                    },
                    "relaxations": relaxations,
                }
            )

            if current == goal:
                break

    distance = distances[goal]
    path: list[str] = []
    if math.isfinite(distance):
        cursor = goal
        while True:
            path.append(cursor)
            if cursor == start:
                break
            cursor = predecessors[cursor]
        path.reverse()

    return {
        "start": start,
        "goal": goal,
        "distance": _distance_for_payload(distance),
        "path": path,
        "steps": steps,
    }
