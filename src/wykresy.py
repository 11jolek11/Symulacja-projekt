from kolejki import *
from pasazer import Pasazer
from miejsca import Miejsca
from algo import zapelnij_kolejke, korytarz
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

kolejka = zapelnij_kolejke(150, 9, 6, Fifo)


print(f'{korytarz(kolejka)/(60)} minut')

queues = [Fifo, PlaceFirst, WindowFirst, RowFirst, BestFirst, Pulse ]
plane_capacities = [50,100,150]
avg_walking_speeds =[6+_ for _ in range(5)]
avg_get_up_speeds = [3+_ for _ in range(3)]
output_list = [[],[],[],[],[]]

def simulations_stack():
    for queue in queues:
        for plane_capacity in plane_capacities:
            for avg_get_up_speed in avg_get_up_speeds:
                for avg_walking_speed in avg_walking_speeds:
                    output_list[0].append(str(queue.__name__))
                    output_list[1].append(str(plane_capacity))
                    output_list[2].append(avg_get_up_speed)
                    output_list[3].append(avg_walking_speed)
                    output_list[4].append(korytarz(zapelnij_kolejke(plane_capacity, 9, avg_get_up_speed, queue))/60)
                    #print(f"{queue.__name__} -- plane_cap: {plane_capacity} -- avg_gtup_spd: {avg_get_up_speed} -- avg_wlk_spd {avg_walking_speed} -------- {korytarz(zapelnij_kolejke(plane_capacity, 9, avg_get_up_speed, queue))/60}")
    return None



simulations_stack()

df = pd.DataFrame(output_list).transpose()
df.columns = ['queue','plane_capacity','avg_get_up_speed','avg_walking_speed','time']

df.to_excel("output.xls")


# df = pd.read_excel('output.xls')

# print(df)

# sns.pairplot(data = df, hue = 'time')
# plt.show()