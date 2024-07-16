# dijkstra.py
# From Classic Computer Science Problems in Python Chapter 4
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass
from mst import WeightedPath, print_weighted_path
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue
import parse_csv as pc
import distance as dis
import duration as dur
import get_predicted_duration_new as gpd
import quantity as quan
import connection as con
import test


V = TypeVar('V') # type of the vertices in the graph


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root) # find starting index
    # distances are unknown at first
    distances: List[Optional[float]] = [None] * wg.vertex_count
    distances[first] = 0 # the root is 0 away from the root
    path_dict: Dict[int, WeightedEdge] = {} # how we got to each vertex
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    pq.push(DijkstraNode(first, 0))

    while not pq.empty:
        u: int = pq.pop().vertex # explore the next closest vertex
        dist_u: float = distances[u] # should already have seen it
        # look at every edge/vertex from the vertex in question
        for we in wg.edges_for_index(u):
            # the old distance to this vertex
            dist_v: float = distances[we.v]
            # no old distance or found shorter path
            if dist_v is None or dist_v > we.weight + dist_u:
                # update distance to this vertex
                distances[we.v] = we.weight + dist_u
                # update the edge on the shortest path to this vertex
                path_dict[we.v] = we
                # explore it soon
                pq.push(DijkstraNode(we.v, we.weight + dist_u))

    return distances, path_dict


# Helper function to get easier access to dijkstra results
def distance_array_to_vertex_dict(wg: WeightedGraph[V], distances: List[Optional[float]]) -> Dict[V, Optional[float]]:
    distance_dict: Dict[V, Optional[float]] = {}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]
    return distance_dict


# Takes a dictionary of edges to reach each node and returns a list of
# edges that goes from `start` to `end`
def path_dict_to_path(start: int, end: int, path_dict: Dict[int, WeightedEdge]) -> WeightedPath:
    if len(path_dict) == 0:
        return []
    edge_path: WeightedPath = []
    e: WeightedEdge = path_dict[end]
    edge_path.append(e)
    while e.u != start:
        e = path_dict[e.u]
        edge_path.append(e)
    return list(reversed(edge_path))


def get_route_duration(ls):
    data = gpd.get_edges_predicted_duration_new(1)
    summe = 0
    for i in range(len(ls)-1):
        dic = con.get_connection(str(ls[i]), str(ls[i+1]))
        num = dic.get("number")
        summe += float(data[int(num)])
    t = float(round((round(summe, 2) - int(round(summe, 2))) * 60)) / 100 + int(round(summe, 2))
    return t


if __name__ == "__main__":
    city_graph2: WeightedGraph[str] = WeightedGraph([str(i) for i in range(538)])

    per = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0037, 0.0037, 0.0077, 0.0077, 0.0077, 0.0077, 0.0077, 0.023, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0237, 0.0237, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0042, 0.0042, 0.0042, 0.0042, 0.0042, 0.0042, 0.0042, 0.027, 0.0506, 0.0, 0.0, 0.0, 0.0002, 0.0408, 0.0, 0.2908, 0.0, 0.0506, 0.0438, 0.0, 0.0173, 0.0, 0.0, 0.0, 0.0527, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0237, 0.0, 0.0, 0.0002, 0.0, 0.0007, 0.0019, 0.0, 0.0, 0.0656, 0.0, 0.0, 0.0, 0.0, 0.0005, 0.0005, 0.0, 0.0, 0.0, 0.003, 0.003, 0.0, 0.0, 0.0949, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0007, 0.0007, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0649, 0.1289, 0.1289, 0.1537, 0.1537, 0.1537, 0.0206, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0042, 0.063, 0.0007, 0.0, 0.0014, 0.0007, 0.0, 0.0, 0.0007, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005, 0.0005, 0.0, 0.0, 0.0, 0.0602, 0.0, 0.0148, 0.0551, 0.0, 0.0846, 0.0, 0.0, 0.0905, 0.0202, 0.0084, 0.2105, 0.0, 0.0, 0.0, 0.0452, 0.0, 0.0, 0.0, 0.0028, 0.0, 0.4654, 0.0, 0.0122, 0.0, 0.0005, 0.1455, 0.0, 0.0, 0.0, 0.0059, 0.0, 0.0, 0.0, 0.0, 0.011, 0.0277, 0.1455, 0.0, 0.0, 0.0935, 0.0368, 0.0, 0.0098, 0.0262, 0.0452, 0.6285, 0.0, 0.0, 0.0002, 0.0, 0.0028, 0.0091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0874, 0.0, 0.3131, 0.0, 0.6285, 0.0206, 0.027, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0098, 0.0014, 0.0005, 0.0, 0.2147, 0.0028, 0.0007, 0.0, 0.0237, 0.2641, 0.1411, 0.0, 0.0989, 0.0, 0.0009, 0.0227, 0.0, 0.0, 0.0696, 0.0098, 0.0, 0.0014, 0.0, 0.0, 0.0, 1.0, 0.0007, 0.0293, 0.0026, 0.4617, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.023, 0.0007, 0.0, 0.0026, 0.0, 0.0, 0.0002, 0.0129, 0.8378, 0.0, 0.011, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0091, 0.0642, 0.0, 0.0, 0.0, 0.0, 0.0077, 0.2641, 0.3122, 0.6691, 0.0, 0.0, 0.0045, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0084, 0.0293, 0.0002, 0.0, 0.0, 0.0, 0.0, 0.0457, 0.0293, 0.0, 0.0, 0.0262, 0.0, 0.0, 0.0, 0.0, 0.0352, 0.0014, 0.0084, 0.0005, 0.0516, 0.0098, 0.0757, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0098, 0.0, 0.1111, 0.0019, 0.0295, 0.0, 0.0028, 0.4654, 0.0112, 0.0312, 0.0, 0.0, 0.0012, 0.2112, 0.0, 0.2112, 0.6285, 0.0, 0.0, 0.0005, 0.0905, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0098, 0.0, 0.0, 0.0, 0.0, 0.7345, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0553, 0.6285, 0.0, 0.0, 0.0, 0.0183, 0.0005, 0.0183, 0.0197, 0.0277, 0.0, 0.011, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0696, 0.1455, 0.1029, 0.0026, 0.0, 0.0042, 0.0012, 0.1155, 0.0, 0.0, 0.0, 0.0335, 0.011, 0.0, 0.0, 0.6285, 0.2105, 0.0281, 0.0, 0.0, 0.0905, 0.0, 0.0, 0.0, 0.0183, 0.0, 0.0262, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0708, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.7345, 0.0, 0.2105, 0.0262, 0.1008, 0.8378, 0.0084, 0.0288, 0.0002, 0.0042, 0.023, 0.0, 0.0103, 0.0, 0.0, 0.0227, 0.0, 0.0, 0.0, 0.0005, 0.0288, 0.0337, 0.0007, 0.0, 0.0, 0.0197, 0.0042, 0.0028, 0.0, 0.0, 0.0, 0.0028, 0.0, 0.0, 0.0, 0.1029, 0.0, 0.1174, 0.8378, 0.0026, 0.0166, 0.0129, 0.0, 0.0923, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6285, 0.0, 0.0042, 0.0, 0.0, 0.0028, 0.003, 0.0, 0.0103, 0.0, 0.0, 0.0, 0.1411, 0.0007, 0.0, 0.0042, 0.0, 0.0, 0.0295, 0.0162, 0.0375, 0.0, 0.0096, 0.0, 0.8378, 0.0206, 0.0, 0.0, 0.0, 0.1455, 0.0, 0.0, 0.0, 0.0506, 0.0, 0.0, 0.0258, 0.0002, 0.0045, 0.0, 0.0293, 0.0905, 0.0, 0.0077, 0.0, 0.0197, 0.0, 0.0197, 0.0, 0.0162, 0.0178, 0.0173, 0.0014, 0.0042, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009, 0.0, 0.0, 0.0, 0.3122, 0.0, 0.0009, 0.0, 0.0, 0.0002, 0.0408, 0.0, 0.0, 0.153, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0227, 0.0, 0.3131, 0.0178, 0.2641, 0.0, 0.0977, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0696, 0.0452, 0.0, 0.0, 0.0005, 0.0, 0.0, 0.0, 0.018, 0.0012, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6285, 0.0, 0.0173, 0.0506, 0.0, 0.0, 0.0, 0.0002, 0.0, 0.0, 0.0, 0.0, 0.0047, 0.0293, 0.0005, 0.3122, 0.0, 0.0, 0.0, 0.0005, 0.0, 0.0, 0.0, 0.0, 0.0047, 0.2641, 0.2105, 0.0028, 0.0, 0.0, 0.0007, 0.0009, 0.0209, 0.0, 0.0935, 0.0, 0.0, 0.0033, 0.2641, 0.0, 0.0134, 0.0, 0.0, 0.0, 0.0042, 0.0005, 0.0197, 0.0068, 0.153, 0.0, 0.1036, 0.0, 0.0014, 0.0551, 0.2105, 0.0, 0.6285, 0.0002, 0.0, 0.1111, 0.0, 0.0, 0.0002, 0.0206, 0.0211, 0.0091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0368, 0.0211, 0.0, 0.3436, 0.0, 0.0977, 0.2112, 0.0, 0.0002, 0.0084, 0.0063, 0.0, 0.1158, 0.0295, 0.0002, 0.0, 0.0, 0.2339, 0.0, 0.0, 0.0, 0.0, 0.2112, 0.0183, 0.0, 0.0457, 0.0, 0.0, 0.0, 0.0, 0.0206, 0.0002, 0.0178, 0.0014, 0.0005, 0.0, 0.0675, 0.0, 0.0, 0.0, 0.0166, 0.0, 0.0419, 0.0005, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0935, 0.011, 0.0007, 0.0, 0.0209, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4143, 0.0424, 0.0012, 0.0696, 0.0, 0.0211, 0.0, 0.0, 0.0, 0.0084, 0.0, 0.0016, 0.0, 0.6285, 0.0, 0.0, 0.0, 0.0, 0.0094, 0.0, 0.0, 0.0, 0.0, 0.0134, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8378, 0.0, 0.1465, 0.0, 0.0007, 0.0, 0.0, 0.0, 0.1411, 0.0, 0.0237, 0.0, 0.0, 0.0, 0.6285, 0.0, 0.0, 0.0, 0.0, 0.0262, 0.0237, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2105, 0.0, 0.0, 0.0457, 0.0091, 0.0, 0.0, 0.0, 0.6285, 0.0098, 0.0, 0.153, 0.0, 0.0, 0.0, 0.138, 0.0, 0.3478, 0.2775, 0.0, 0.0, 0.0, 0.0, 0.0162, 0.101, 0.0, 0.0, 0.0026, 0.0, 0.0007, 0.0, 0.0007, 0.0424, 0.0, 0.0, 0.0005, 0.0, 0.0258, 0.0, 0.0007, 0.0, 0.0042, 0.0002, 0.0, 0.0, 0.0042, 0.0, 0.0, 0.1336, 0.0087, 0.0905, 0.0, 0.0012, 0.0, 0.0, 0.0002, 0.0, 0.0026, 0.0, 0.0002, 0.0094, 0.0129, 0.0, 0.0, 0.0492, 0.0103, 0.0002, 0.0087, 0.0197, 0.0, 0.0, 0.0, 0.0012, 0.0, 0.0007, 0.0, 0.0002, 0.0, 0.0675, 0.0002, 0.0783, 0.0202, 0.0, 0.0012, 0.0, 0.0, 0.0237, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0281, 0.3131, 0.0, 0.0014, 0.0, 0.2147, 0.0077, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0319, 0.0, 0.0, 0.0279, 0.3827, 0.0, 0.4617, 0.0, 0.0, 0.0, 0.0005, 0.0891, 0.0, 0.0345, 0.0, 0.0134, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0349, 0.0757, 0.0183, 0.0143, 0.0, 0.0, 0.034, 0.0279, 0.0014, 0.0, 0.7345, 0.0, 0.0, 0.0, 0.0103, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0098, 0.0, 0.6285, 0.0, 0.0084, 0.0, 0.0492, 0.0007, 0.0178, 0.0, 0.0, 0.0, 0.1411, 0.0, 0.0103, 0.0007, 0.0, 0.0028, 0.0, 0.0, 0.2641, 0.0007, 0.0, 0.0607, 0.0, 0.0014, 0.0, 0.0, 0.0, 0.0246, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0173, 0.0033, 0.0, 0.0977, 0.0, 0.0, 0.0, 0.1901, 0.0, 0.0, 0.1174, 0.0, 0.6285, 0.0, 0.0, 0.0, 0.0026, 0.0921, 0.0534, 0.0419, 0.0, 0.0, 0.0293, 0.0, 0.0005, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0237, 0.0696, 0.0, 0.0248, 0.0, 0.0, 0.0042, 0.0, 0.0, 0.0012, 0.0, 0.0, 0.0005, 0.0424, 0.0002, 0.0935, 0.0, 0.0607, 0.0002, 0.0, 0.0206, 0.0197, 0.0, 0.0277, 0.0206, 0.0, 0.0, 0.0084, 0.0002, 0.0, 0.0, 0.0103, 0.0045, 0.0, 0.0, 0.0, 0.0, 0.153, 0.0, 0.0, 0.0, 0.0007, 0.0, 0.0312, 0.0183, 0.0143, 0.0, 0.0, 0.0352, 0.0096, 0.0, 0.0295, 0.0, 0.0237, 0.0, 0.8378, 0.0, 0.3715, 0.0, 0.0, 0.0129, 0.0933, 0.0, 0.0007, 0.0, 0.0237, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6285, 0.0, 0.0002, 0.0014, 0.0, 0.0, 0.1411, 0.0, 0.0668, 0.0, 0.0206, 0.0, 0.0134, 0.0, 0.0, 0.0, 0.0, 0.0424, 0.0, 0.0, 0.0, 0.0492, 0.153, 0.0, 0.1111, 0.0, 0.0, 0.0905, 0.0122, 0.0295, 0.0, 0.0016, 0.0, 0.0, 0.0492, 0.0002, 0.0, 0.0162, 0.0173, 0.0, 0.0701, 0.0, 0.0, 0.3827, 0.0, 0.1008, 0.0, 0.0, 0.0, 0.0457, 0.2147, 0.0, 0.0, 0.0, 0.0077, 0.0002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0002, 0.0, 0.0368, 0.0, 0.0, 0.0, 0.4617, 0.0091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0696, 0.0, 0.0, 0.0, 0.003, 0.0, 0.0, 0.0122, 0.0166, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0002, 0.2112, 0.0, 0.0, 0.0, 0.0783, 0.0, 0.3131, 0.0989, 0.3136, 0.0, 0.0012, 0.0009, 0.0, 0.0, 0.0, 0.0005, 0.0319, 0.0, 0.0, 0.0005, 0.0007, 0.109, 0.0002, 0.0, 0.0002, 0.0, 0.0045, 0.0005, 0.0, 0.0098, 0.0, 0.0037, 0.0298, 0.0, 0.0019, 0.0016, 0.0534, 0.1411, 0.0005, 0.2351, 0.3541, 0.0084, 0.0005, 0.0244, 0.0, 0.0801, 0.0, 0.0, 0.0984, 0.019, 0.0, 0.0042, 0.0, 0.3136, 0.3143, 0.0, 0.0007, 0.0, 0.0, 0.0002, 0.0014, 0.0045, 0.0, 0.0, 0.0, 0.0023, 0.0, 0.0511, 0.0, 0.1392, 0.0169, 0.0, 0.1162, 0.033, 0.0, 0.4617, 0.131, 0.0, 0.0, 0.0, 0.0157, 0.0, 0.3274, 0.0, 0.0497, 0.0005, 0.1577, 0.2775, 0.0002, 0.0, 0.0152, 0.0687, 0.0, 0.0]

    graph = pc.parse_csv()
    # dist = dis.get_distance_list()
    for i in range(1, len(graph)):
        fro = graph[i].get('from')
        to = graph[i].get('to')
        if per[i - 1] >= 0.40:
            percentage = 1 - per[i - 1]
        else:
            percentage = 1
        # city_graph2.add_edge_by_vertices(str(fro), str(to), dist[i-1])  #Anfang, Ende, Gewichtung
        city_graph2.add_edge_by_vertices(str(fro), str(to), test.get_edges_predicted_duration_new('28 Mr 00_09_46')[i-1] * percentage)

    distances, path_dict = dijkstra(city_graph2, "94")
    name_distance: Dict[str, Optional[int]] = distance_array_to_vertex_dict(city_graph2, distances)
    print("Distances from 94:")
    for key, value in name_distance.items():
        print(f"{key} : {value}")
    print("") # blank line

    print("Shortest path from 94 to 162:")
    path: WeightedPath = path_dict_to_path(city_graph2.index_of("94"), city_graph2.index_of("162"), path_dict)
    print_weighted_path(city_graph2, path)
