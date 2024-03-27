import streamlit as st

def shortest_remaining_time_first(processes):
    n = len(processes)
    remaining_time = [processes[i][2] for i in range(n)]
    completed = 0
    current_time = 0
    ready_queue = []
    schedule = []

    while completed != n:
        for i in range(n):
            if processes[i][1] <= current_time and remaining_time[i] > 0:
                ready_queue.append((i, remaining_time[i]))

        if len(ready_queue) == 0:
            current_time += 1
            continue

        ready_queue.sort(key=lambda x: x[1])
        index, burst_time = ready_queue.pop(0)
        schedule.append((processes[index][0], current_time))
        current_time += 1
        remaining_time[index] -= 1

        if remaining_time[index] == 0:
            completed += 1

    return schedule

def main():
    st.title("Shortest Remaining Time First (SRTF) Scheduling Algorithm")

    num_processes = st.number_input("Enter the number of processes:", min_value=1, step=1, value=1)

    processes = []
    for i in range(num_processes):
        name = st.text_input(f"Process Name {i + 1}")
        arrival_time = st.number_input(f"Arrival Time for Process {i + 1}", value=0)
        burst_time = st.number_input(f"Burst Time for Process {i + 1}", value=1)
        processes.append((name, arrival_time, burst_time))

    if st.button("Run SRTF Algorithm"):
        schedule = shortest_remaining_time_first(processes)
        st.subheader("Schedule:")
        for process, start_time in schedule:
            st.write(f"{process} starts at time {start_time}")

if __name__ == "__main__":
    main()

