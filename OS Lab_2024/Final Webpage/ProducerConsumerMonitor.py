import streamlit as st
import threading
from queue import Queue

# Class for managing the monitor
class Monitor:
    def __init__(self, buffer_size):
        # Initialise the buffer and synchronisation primitives
        self.buffer = Queue(maxsize=buffer_size)  # Create a Queue object with a maximum size
        self.lock = threading.Lock()  # Create a lock for thread synchronisation
        self.producer_condition = threading.Condition(self.lock)  # Condition variable for producer
        self.consumer_condition = threading.Condition(self.lock)  # Condition variable for consumer
        self.consumed_data = []  # List to store consumed data

    # Method for producing data and adding it to the buffer
    def produce(self, data):
        with self.lock:  # Acquire the lock
            # Wait if the buffer is full
            while len(data) > self.buffer.maxsize - self.buffer.qsize():
                st.warning("Buffer is full. Producer is waiting.")  # Display warning message
                self.producer_condition.wait()  # Wait for space in the buffer

            # Add each unit of data to the buffer
            for unit in data:
                self.buffer.put(unit)  # Put data into the buffer
                st.success(f"Produced: {unit}")  # Display success message
                # Notify consumer that new data is available
                self.consumer_condition.notify()

    # Method for consuming data from the buffer
    def consume(self):
        with self.lock:  # Acquire the lock
            # Wait if the buffer is empty
            while self.buffer.empty():
                st.warning("Buffer is empty. Consumer is waiting.")  # Display warning message
                self.consumer_condition.wait()  # Wait for data in the buffer

            # Retrieve data from the buffer
            data = self.buffer.get()  # Get data from the buffer
            self.consumed_data.append(data)  # Append consumed data to the list
            st.success(f"Consumed: {data}")  # Display success message
            # Notify producer that space is available in the buffer
            self.producer_condition.notify()

# Main function for the Streamlit app
def producer_consumer():
    # Streamlit UI components
    st.title("Producer-Consumer Problem using Monitors")

    buffer_size = st.slider("Clipboard size:", min_value=1, max_value=10, value=5)

    # Get or create the Monitor object
    monitor = get_monitor(buffer_size)

    data_input = st.text_input("Enter data to produce:")

    if st.button("Copy"):
        if data_input:
            monitor.produce(data_input)

    if st.button("Paste"):
        consumed_data = monitor.consume()
        if consumed_data:
            st.table([consumed_data])

    st.subheader("Clipboard Data:")
    buffer_contents = list(monitor.buffer.queue)
    st.table(buffer_contents)

    st.subheader("Pasted Data:")
    st.table(monitor.consumed_data)

# Cache the Monitor object with Streamlit to preserve state across reruns
@st.cache(allow_output_mutation=True)
def get_monitor(buffer_size):
    return Monitor(buffer_size)

if __name__ == "__main__":
    producer_consumer()
