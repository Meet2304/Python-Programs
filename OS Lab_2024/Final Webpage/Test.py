import streamlit as st
from SSTF import main as sstf_main
from SRTF import main as srtf_main
from OptimalPageReplacement import main as optimal_page_replacement_main
from ProducerConsumerMonitor import producer_consumer as producer_consumer_main

def main():
    st.title('Algorithm Visualizations')

    # Highlighted dropdown selector for algorithm choice
    st.markdown('<style>div.Widget.row-widget.stSelectbox {background-color: #f0f0f5;}</style>', unsafe_allow_html=True)
    algorithm = st.selectbox('Select an algorithm:', ['Shortest Remaining Time First (SRTF)', 'SSTF Disk Scheduling', 'Optimal Page Replacement', 'Producer-Consumer using Monitors'])

    if algorithm == 'Shortest Remaining Time First (SRTF)':
        srtf_main()
    elif algorithm == 'SSTF Disk Scheduling':
        sstf_main()
    elif algorithm == 'Optimal Page Replacement':
        optimal_page_replacement_main()
    elif algorithm == 'Producer-Consumer using Monitors':
        producer_consumer_main()

if __name__ == '__main__':
    main()
