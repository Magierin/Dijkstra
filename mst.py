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
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue
import parse_csv as pc
import distance as dis
import duration as dur
import connection as con
import get_predicted_duration_new as gpd

V = TypeVar('V') # type of the vertices in the graph
WeightedPath = List[WeightedEdge] # type alias for paths


def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > (wg.vertex_count - 1) or start < 0:
        return None
    result: WeightedPath = [] # holds the final MST
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: List[bool] = [False] * wg.vertex_count # where we've been

    def visit(index: int):
        visited[index] = True # mark as visited
        for edge in wg.edges_for_index(index):
            # add all edges coming from here to pq
            if not visited[edge.v]:
                pq.push(edge)

    visit(start) # the first vertex is where everything begins

    while not pq.empty: # keep going while there are edges to process
        edge = pq.pop()
        if visited[edge.v]:
            continue # don't ever revisit
        # this is the current smallest, so add it to solution
        result.append(edge)
        visit(edge.v) # visit where this connects

    return result


def get_route_duration(ls):
    data = gpd.get_edges_predicted_duration_new(1)
    summe = 0
    for i in range(len(ls)-1):
        dic = con.get_connection(str(ls[i]), str(ls[i+1]))
        num = dic.get("number")
        summe += float(data[int(num)])
    t = float(round((round(summe, 2) - int(round(summe, 2))) * 60)) / 100 + int(round(summe, 2))
    return t


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    route = []
    for edge in wp:
        print(f"{wg.vertex_at(edge.u)} {edge.weight}> {wg.vertex_at(edge.v)}")
        route.append(str(wg.vertex_at(edge.u)))
    route.append('162')
    print("Path: ", route)
    print("Path Total weight: ", get_route_duration(route))
    print(f"Total Weight: {total_weight(wp)}")


if __name__ == "__main__":
    city_graph2: WeightedGraph[str] = WeightedGraph([str(i) for i in range(538)])

    graph = pc.parse_csv()
    # dist = dis.get_distance_list()
    for i in range(1, len(graph)):
        fro = graph[i].get('from')
        to = graph[i].get('to')
        # city_graph2.add_edge_by_vertices(str(fro), str(to), dist[i-1])  #Anfang, Ende, Gewichtung
        city_graph2.add_edge_by_vertices(str(fro), str(to), dur.get_edges_duration()[i])

    result: Optional[WeightedPath] = mst(city_graph2)
    if result is None:
        print("No solution found!")
    else:
        print_weighted_path(city_graph2, result)
