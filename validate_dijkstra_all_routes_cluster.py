import dijkstra as dij
import timestamp as ts
import quantity as quan

percentage = quan.get_edges_quan_per_hour_percentage(quan.get_routes())  # how often all edges appear in all historical routes

'''Takes a route and timestamp : (['94', '209', ...], '28 Mar 00_09_47'); returns percentage, where route matches 75% 
or above with historical routes taken in the same hour'''


def similar(ls_0, hour):
    counter = 0
    summe = 0
    for route in ts.get_timestamp_route_list(hour):
        dup = [x for x in ls_0 if x in route]
        summe += len(dup)/len(ls_0)
        if len(dup)/len(ls_0) >= 0.75:
            counter += 1

    return counter/len(ts.get_timestamp_route_list(hour))


'''Returns list with percentages, that show with how many historical routes the calculated route is 75% similar with;
Similarity is no cluster, just all routes, how often edges were found in historical routes'''


def get_seventy_five_percent_similarity_percent():
    per = percentage
    timestamp = ts.get_timestamp_all()  # [4267:]
    paths = []
    for time in timestamp:
        path = dij.dijkstra_1(time, per)
        paths.append(similar(path, time))
    return paths
