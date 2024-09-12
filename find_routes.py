import dijkstra as dij
import timestamp as ts
import quantity as quan


'''Returns list with routes from 12 Mai'''


def compute_all_routes():
    timestamp = ts.get_timestamp_all()[4267:]  # all timestamps from 12th Mai
    routes = quan.get_routes_quantity_per_hour()
    perc = []
    paths = []

    for i in range(24):
        percentages = quan.get_edges_quan_per_hour_percentage(routes[i])
        perc.append(percentages)

    for time in timestamp:
        ind = int(time.split()[2].split('_')[0])
        path = dij.dijkstra_1(time, perc[ind])
        paths.append(path)

    return paths


'''Creates the routes-last-day.csv file, with all missing routes'''


def create_csv_last_day_routes():
    ls = compute_all_routes()
    timestamp = ts.get_timestamp_all()[4267:]
    csv = open('routes-last-day.csv', 'w')

    for i in range(len(ls)):
        print(ls[i], timestamp[i].split())
        ls1 = ls[i] + timestamp[i].split()
        csv.writelines(','.join([str(x) for x in ls1]) + "\n")
    csv.close()
