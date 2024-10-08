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
print('Algorithm running...')
import parse_csv as pc
import duration as dur
import hourly_percentages as hp

V = TypeVar('V')  # type of the vertices in the graph


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root)  # find starting index
    # distances are unknown at first
    distances: List[Optional[float]] = [None] * wg.vertex_count
    distances[first] = 0  # the root is 0 away from the root
    path_dict: Dict[int, WeightedEdge] = {}  # how we got to each vertex
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    pq.push(DijkstraNode(first, 0))

    while not pq.empty:
        u: int = pq.pop().vertex  # explore the next closest vertex
        dist_u: float = distances[u]  # should already have seen it
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


'''Takes timestamps and percentages in form of '28 Mr 00_09_47' and lists with length 1308; returns shortest/optimal 
path cin a particular timestamp with its length'''


def dijkstra_1(timestamp, per):
    city_graph2: WeightedGraph[str] = WeightedGraph([str(i) for i in range(538)])

    duration = dur.get_edges_predicted_duration_new(timestamp)

    graph = pc.graph
    for i in range(1, len(graph)):
        fro = graph[i].get('from')
        to = graph[i].get('to')
        percentage = 1 - (per[i - 1])
        city_graph2.add_edge_by_vertices(str(fro), str(to), duration[i-1] * percentage)

    distances, path_dict = dijkstra(city_graph2, "94")

    print("Shortest path from 94 to 162 at {}:".format(timestamp))
    path: WeightedPath = path_dict_to_path(city_graph2.index_of("94"), city_graph2.index_of("162"), path_dict)
    p = print_weighted_path(city_graph2, path, timestamp)
    return p


def dijkstra_main(timestamp):
    city_graph2: WeightedGraph[str] = WeightedGraph([str(i) for i in range(538)])

    duration = dur.get_edges_predicted_duration_new(timestamp)
    ind = int(timestamp.split()[2].split('_')[0])

    graph = pc.graph
    for i in range(1, len(graph)):
        fro = graph[i].get('from')
        to = graph[i].get('to')
        percentage = 1 - (hp.perc[ind][i - 1])
        city_graph2.add_edge_by_vertices(str(fro), str(to), duration[i - 1] * percentage)

    distances, path_dict = dijkstra(city_graph2, "94")

    print("Optimal shortest route from 94 to 162 at {}:".format(timestamp))
    path: WeightedPath = path_dict_to_path(city_graph2.index_of("94"), city_graph2.index_of("162"), path_dict)
    p = print_weighted_path(city_graph2, path, timestamp)
    return p
