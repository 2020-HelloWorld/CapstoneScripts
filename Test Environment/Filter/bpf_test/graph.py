import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_live_packet_presence(filename:str, src_ip:str, des_ip:str):
    fig, ax = plt.subplots()
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Packet Presence")

    def update(frame):
        try:
            data = pd.read_csv(filename)
            data = data[(data['src_ip'] == src_ip) & (data['des_ip'] == des_ip)]
            data['presence'] = (data['departure_time'].notna() | data['protocol']==UDP).cumsum()
            ax.clear()
            ax.plot(data['arrival_time'], data['presence'])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Packet Presence")
        except:
            pass
    
    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()
