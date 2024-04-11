import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def findClosest(queue, head):
    l = len(queue)
    diff = [0] * l
    for i in range(l):
        diff[i] = abs(queue[i] - head)
    minimumDistIndex = diff.index(min(diff))  # Find the index of the minimum absolute difference
    return queue[minimumDistIndex]  # Return the value at that index


def sstf_disk_scheduling(queue, head):
    total_movement = 0  # Initialize total head movement to 0
    current_position = head  # Initialize current head position
    sequence = []  # Initialize list to store sequence of head movements


    while queue:  # Continue loop until all requests are serviced
        closest = findClosest(queue, current_position)
        total_movement += abs(closest - current_position)  # Calculate head movement for this request
        current_position = closest  # Move head to the closest request
        sequence.append(current_position)  # Add current head position to the sequence
        queue.remove(current_position)  # Remove serviced request from the queue


    return total_movement, sequence  # Return total head movement and sequence of head movements


def main():
    st.title('SSTF Disk Scheduling')


    # Sidebar for input parameters
    st.sidebar.header('Input Parameters')
    request_queue = st.sidebar.text_input('Request Queue (comma-separated)', '98, 183, 37, 122, 14, 124, 65, 67')
    initial_head_position = st.sidebar.number_input('Initial Head Position', value=53)


    # Processing the inputs
    request_queue = list(map(int, request_queue.split(',')))


    # Call the SSTF scheduling function with the provided queue and head position
    total_movement, sequence = sstf_disk_scheduling(request_queue, initial_head_position)


    # Display results
    st.header('Results')
    st.write("Total head movement:", total_movement)


    # Display sequence of head movements in a table
    df_sequence = pd.DataFrame({'Time (Order of Access)': range(len(sequence)), 'Track Number': sequence})
    st.write("Sequence of head movements:")
    st.write(df_sequence)


    # Plotting the head movements
    st.header('Visualization')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(range(len(sequence)), sequence, color='blue')
    ax.plot(range(len(sequence)), sequence, linestyle='dotted', color='red')
    ax.set_title('Sequence of Head Movements (SSTF Disk Scheduling)')
    ax.set_xlabel('Time (Order of Access)')
    ax.set_ylabel('Track Number')
    ax.grid(True)
    st.pyplot(fig)


if __name__ == "__main__":
    main()