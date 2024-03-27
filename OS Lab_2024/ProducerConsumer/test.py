import streamlit as st
import threading
import time
from queue import Queue

class Monitor:
    def __init__(self, buffer_size):
        self.buffer = Queue(maxsize=buffer_size)
        self.lock = threading.Lock()
        self.producer_condition = threading.Condition(self.lock)
        self.consumer_condition = threading.Condition(self.lock)
        self.consumed_data = []

    def produce(self, data):
        with self.lock:
            while self.buffer.full():
                self.producer_condition.wait()

            for unit in data:
                self.buffer.put(unit)
                self.consumer_condition.notify()

    def consume(self):
        with self.lock:
            while self.buffer.empty():
                self.consumer_condition.wait()

            data = self.buffer.get()
            self.consumed_data.append(data)
            self.producer_condition.notify()
            return data

def producer_consumer(buffer_size):
    monitor = get_monitor(buffer_size)

    st.title("Producer-Consumer Problem using Monitors")

    data_input = st.text_input("Enter data to produce:")
    buffer_size = st.slider("Clipboard size:", min_value=1, max_value=10, value=5)

    if st.button("Copy"):
        if data_input:
            monitor.produce(data_input)
            st.success(f"Produced: {data_input}")

    if st.button("Paste"):
        consumed_data = monitor.consume()
        if consumed_data:
            st.success(f"Consumed: {consumed_data}")

    st.subheader("Clipboard Data:")
    buffer_contents = list(monitor.buffer.queue)
    st.table(buffer_contents)

    st.subheader("Pasted Data:")
    st.table(monitor.consumed_data)

@st.cache(allow_output_mutation=True)
def get_monitor(buffer_size):
    return Monitor(buffer_size)

if __name__ == "__main__":
    producer_consumer(10)
