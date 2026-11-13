import unittest

from sourceloop.graph import GraphValidationError, shortest_path_trace


CAMPUS_GRAPH = {
    "start": "LIB",
    "goal": "LAB",
    "nodes": [
        {"id": "LIB", "label": {"en": "Library", "zh": "图书馆"}},
        {"id": "STA", "label": {"en": "Station", "zh": "车站"}},
        {"id": "CAN", "label": {"en": "Canteen", "zh": "食堂"}},
        {"id": "LAB", "label": {"en": "Lab", "zh": "实验室"}},
        {"id": "HALL", "label": {"en": "Hall", "zh": "宿舍"}},
    ],
    "edges": [
        {"from": "LIB", "to": "STA", "weight": 4},
        {"from": "LIB", "to": "CAN", "weight": 2},
        {"from": "STA", "to": "CAN", "weight": 1},
        {"from": "STA", "to": "LAB", "weight": 8},
        {"from": "STA", "to": "HALL", "weight": 9},
        {"from": "CAN", "to": "LAB", "weight": 7},
        {"from": "CAN", "to": "HALL", "weight": 6},
        {"from": "LAB", "to": "HALL", "weight": 2},
    ],
}


class ShortestPathTraceTests(unittest.TestCase):
    def test_finds_minimum_weight_route_not_fewest_edges(self):
        trace = shortest_path_trace(CAMPUS_GRAPH, "LIB", "LAB")

        self.assertEqual(trace["distance"], 9)
        self.assertEqual(trace["path"], ["LIB", "CAN", "LAB"])

    def test_exposes_real_relaxations_for_the_ui(self):
        trace = shortest_path_trace(CAMPUS_GRAPH, "LIB", "LAB")
        all_relaxations = [
            relaxation
            for step in trace["steps"]
            for relaxation in step["relaxations"]
        ]

        self.assertTrue(
            any(
                relaxation["from"] == "CAN"
                and relaxation["to"] == "STA"
                and relaxation["previous"] == 4
                and relaxation["distance"] == 3
                for relaxation in all_relaxations
            )
        )
        self.assertEqual(trace["steps"][0]["current"], None)
        self.assertEqual(trace["steps"][-1]["current"], "LAB")

    def test_start_and_goal_may_be_the_same_node(self):
        trace = shortest_path_trace(CAMPUS_GRAPH, "LIB", "LIB")

        self.assertEqual(trace["distance"], 0)
        self.assertEqual(trace["path"], ["LIB"])

    def test_reports_unreachable_goal_without_fabricating_a_path(self):
        graph = {
            "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
            "edges": [{"from": "A", "to": "B", "weight": 1}],
        }

        trace = shortest_path_trace(graph, "A", "C")

        self.assertIsNone(trace["distance"])
        self.assertEqual(trace["path"], [])

    def test_rejects_negative_weights_for_this_teaching_visual(self):
        graph = {
            "nodes": [{"id": "A"}, {"id": "B"}],
            "edges": [{"from": "A", "to": "B", "weight": -1}],
        }

        with self.assertRaises(GraphValidationError):
            shortest_path_trace(graph, "A", "B")


if __name__ == "__main__":
    unittest.main()
