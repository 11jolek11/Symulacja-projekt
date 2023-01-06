from kolejki import *
from pasazer import Pasazer
from miejsca import Miejsca
from main import Worker
import pandas as pd
import plotly.express as px



def simulate_and_drop_to_excel(file_name):
    queues = [Fifo, PlaceFirst, WindowFirst, RowFirst, BestFirst, Pulse ]
    plane_capacities = [50,100,150]
    jumps = [0.1,0.2,0.3,0.4,0.5]
    avg_walking_speeds =[1+_ for _ in jumps]
    avg_get_up_speeds = [6+_ for _ in jumps]
    output_list = [[],[],[],[],[]]
    fifo_df = pd.DataFrame()
    place_first_df = pd.DataFrame()
    window_first_df = pd.DataFrame()
    row_first_df = pd.DataFrame()
    best_first_df = pd.DataFrame()
    pulse_df = pd.DataFrame()
    queue_data_frames = [fifo_df,place_first_df,window_first_df,row_first_df,best_first_df,pulse_df]
    z = 0
    for queue in queues:
        for plane_capacity in plane_capacities:
            for avg_get_up_speed in avg_get_up_speeds:
                for avg_walking_speed in avg_walking_speeds:
                    output_list[0].append(str(queue.__name__))
                    output_list[1].append(str(plane_capacity))
                    output_list[2].append(avg_get_up_speed)
                    output_list[3].append(avg_walking_speed)
                    output_list[4].append(Worker(plane_capacity,avg_walking_speed,avg_get_up_speed,0.5, 0.005, queue).simulate()/60)
        
        queue_data_frames[z] = pd.DataFrame(output_list).transpose()
        queue_data_frames[z].columns=["queue","number_of_ppl","avg_get_up_speed","avg_walking_speed","time"]
        print(f"done {queue.__name__}")
        for _ in output_list: _.clear()
        z+=1
  
    with pd.ExcelWriter(f"{file_name}.xlsx") as writer:
        z = 0
        for _ in queue_data_frames:
            _.to_excel(writer, sheet_name=f"{queues[z].__name__}",index = False)
            z+=1
    return None

def take_from_excel_and_graph(file_name):
    fifo_df = pd.read_excel(f"{file_name}.xlsx",sheet_name = "Fifo")
    place_fist_df = pd.read_excel(f"{file_name}.xlsx",sheet_name = "PlaceFirst")
    window_first_df = pd.read_excel(f"{file_name}.xlsx",sheet_name = "WindowFirst")
    row_first_df = pd.read_excel(f"{file_name}.xlsx",sheet_name = "RowFirst")
    best_first_df = pd.read_excel(f"{file_name}.xlsx",sheet_name = "BestFirst")
    pulse_df = pd.read_excel(f"{file_name}.xlsx",sheet_name = "Pulse")
    print(pulse_df)

    pd.options.plotting.backend = "plotly"
    fig = pulse_df.plot(y=["time","avg_walking_speed","avg_get_up_speed"])
    fig.show()
    return None


simulate_and_drop_to_excel("nowy")
take_from_excel_and_graph("nowy")


# df = pd.read_excel('output.xls')

# df = df.astype(str)

# # pd.options.plotting.backend = "plotly"
# print(df)
# output_queues = df["queue"].tolist()
# output_times = df["time"].tolist()
# output_avg_get_up_speeds = df["avg_get_up_speed"].tolist()
# output_avg_walking_speeds = df["avg_walking_speed"].tolist()
# output_plane_capacities = df["plane_capacity"].tolist()

# fig = px.line()