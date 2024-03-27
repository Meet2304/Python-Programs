import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def shortest_remaining_time_first(processes):
    n = len(processes)
    burst_remaining = [processes[i][2] for i in range(n)]
    completed = 0
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    gantt_chart = []

    while completed != n:
        shortest_burst = float('inf')
        shortest_index = -1

        for i in range(n):
            if processes[i][1] <= current_time and burst_remaining[i] < shortest_burst and burst_remaining[i] > 0:
                shortest_burst = burst_remaining[i]
                shortest_index = i

        if shortest_index == -1:
            current_time += 1
            continue

        burst_remaining[shortest_index] -= 1

        if burst_remaining[shortest_index] == 0:
            completed += 1
            completion_time = current_time + 1
            turnaround_time = completion_time - processes[shortest_index][1]
            waiting_time = turnaround_time - processes[shortest_index][2]
            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
        else:
            completion_time = None

        gantt_chart.append((processes[shortest_index][0], current_time, completion_time))
        current_time += 1

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    return gantt_chart, avg_waiting_time, avg_turnaround_time

def plot_gantt_chart(gantt_chart):
    processed_data = []
    for i in range(len(gantt_chart)):
        if gantt_chart[i][2] is not None:
            processed_data.append(gantt_chart[i])

    plt.figure(figsize=(10, 3))
    for i in range(len(processed_data)):
        plt.barh(y=0.5, left=processed_data[i][1], width=processed_data[i][2]-processed_data[i][1], height=0.5, color='b', align='center', alpha=0.5)
        plt.text((processed_data[i][1]+processed_data[i][2])/2, 0.5, processed_data[i][0], ha='center', va='center')
        plt.xticks(range(0, max([p[2] for p in processed_data])+2, 1))
    plt.xlabel('Time')
    plt.title('Gantt Chart')
    plt.yticks([])
    plt.grid(axis='x')
    st.pyplot(plt)

def main():
    st.title('Shortest Remaining Time First (SRTF) Scheduling Algorithm')
    n = st.number_input('Enter the number of processes:', min_value=1, step=1, value=1)
    
    processes = []
    for i in range(n):
        st.write(f'Process {i+1}:')
        process_name = st.text_input(f'Enter process name for Process {i+1}:', key=f'process_name_{i}')
        arrival_time = st.number_input(f'Enter arrival time for Process {i+1}:', min_value=0, step=1, value=0, key=f'arrival_time_{i}')
        burst_time = st.number_input(f'Enter burst time for Process {i+1}:', min_value=1, step=1, value=1, key=f'burst_time_{i}')
        processes.append((process_name, arrival_time, burst_time))

    if st.button('Run SRTF'):
        gantt_chart, avg_waiting_time, avg_turnaround_time = shortest_remaining_time_first(processes)
        st.write('Average Waiting Time:', avg_waiting_time)
        st.write('Average Turnaround Time:', avg_turnaround_time)
        
        st.write("Input User Data:")
        input_data_df = pd.DataFrame(processes, columns=["Process Name", "Arrival Time", "Burst Time"])
        st.table(input_data_df)

        st.write("Final Process Details:")
        output_data = []
        output_data.append(["Process Name", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"])
        for process in processes:
            for gantt_process in gantt_chart:
                if process[0] == gantt_process[0]:
                    completion_time = gantt_process[2]
                    if completion_time is not None:
                        turnaround_time = completion_time - process[1]
                        waiting_time = turnaround_time - process[2]
                        output_data.append([process[0], process[1], process[2], completion_time, turnaround_time, waiting_time])
        st.table(output_data)

        plot_gantt_chart(gantt_chart)

if __name__ == '__main__':
    main()
