import dijkstra as dij
import quantity as quan
import connection as con
import test


def similar(ls_0, hour):
    counter = 0
    summe = 0
    for route in test.get_timestamp_route_list(hour):
        dup = [x for x in ls_0 if x in route]
        summe += len(dup)/len(ls_0)
        if len(dup)/len(ls_0) >= 0.75:
            counter += 1
    return counter/len(test.get_timestamp_route_list(hour))


def get_timestamp_route_list(timestamp):
    ts = timestamp.split()
    hour = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '20', '21', '22', '23']

    ls = []
    for i in hour:
        if ts[2].startswith(i):
            ls = quan.get_routes_quantity_per_hour()[hour.index(i)]
            break

    return ls


def get_edges_quan_per_hour_per(timestamp):
    routes = get_timestamp_route_list(timestamp)
    edges = []
    counter = []

    for i in range(len(routes)):
        for j in range(1, len(routes[i])):
            dic = con.get_connection(routes[i][j - 1], routes[i][j])
            num = dic.get('number')
            edges.append(int(num))

    for i in range(1308):
        c = edges.count(i)
        per = c / len(routes)
        counter.append(round(per, 4))

    return counter


def get_seventy_five_percent_similarity_percent():
    timestamp = test.get_timestamp_all()[4267:]
    paths = []
    for time in timestamp:
        per = get_edges_quan_per_hour_per(time)
        path = dij.dijkstra_main(time, per)
        paths.append(similar(path, time))
        print(paths)
    return paths


# print(get_seventy_five_percent_similarity_percent())

date = '12 Mai 23_56_09'
per = get_edges_quan_per_hour_per(date)
path = dij.dijkstra_main(date, per)
