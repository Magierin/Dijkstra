# mst.py
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
from typing import TypeVar, List, Optional
import duration as dur
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue
import connection as con


V = TypeVar('V')  # type of the vertices in the graph
WeightedPath = List[WeightedEdge]  # type alias for paths


def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > (wg.vertex_count - 1) or start < 0:
        return None
    result: WeightedPath = []  # holds the final MST
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: List[bool] = [False] * wg.vertex_count  # where we've been

    def visit(index: int):
        visited[index] = True  # mark as visited
        for edge in wg.edges_for_index(index):
            # add all edges coming from here to pq
            if not visited[edge.v]:
                pq.push(edge)

    visit(start)  # the first vertex is where everything begins

    while not pq.empty:  # keep going while there are edges to process
        edge = pq.pop()
        if visited[edge.v]:
            continue  # don't ever revisit
        # this is the current smallest, so add it to solution
        result.append(edge)
        visit(edge.v)  # visit where this connects

    return result


'''Returns the duration of the dijkstra computed route; Input: (['94', '209', ...], '28 Mar 00_09_27')'''


def get_route_duration(ls, timestamp):
    data = dur.get_edges_predicted_duration_new(timestamp)
    summe = 0
    for i in range(len(ls)-1):
        dic = con.get_connection(str(ls[i]), str(ls[i+1]))
        num = dic.get("number")
        summe += float(data[int(num)])
    t = float(round((round(summe, 2) - int(round(summe, 2))) * 60)) / 100 + int(round(summe, 2))
    return t


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath, timestamp):
    route = []
    for edge in wp:
        route.append(str(wg.vertex_at(edge.u)))
    route.append('162')
    print("Route: ", route)
    print("Total Duration In Minutes: ", get_route_duration(route, timestamp))
    return get_route_duration(route, timestamp)
