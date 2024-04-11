import streamlit as st
import matplotlib.pyplot as plt


def optimal_page_replacement(pages, capacity):
    page_faults = 0
    page_table = []
    faults = []

    for page_index, page in enumerate(pages):
        if page not in page_table:
            if len(page_table) < capacity:
                page_table.append(page)
            else:
                future_refs = {}
                for p in page_table:
                    try:
                        future_refs[p] = pages.index(p, pages.index(page) + 1)
                    except ValueError:
                        future_refs[p] = float('inf')
               
                page_to_replace = max(future_refs, key=future_refs.get)
                page_table[page_table.index(page_to_replace)] = page
                page_faults += 1
                faults.append(page_index)
                st.write(f"Page {page_to_replace} replaced by {page}. Page faults: {page_faults}")
        # Display current page table state
        st.write(f"Current page table: {page_table}")
    return page_faults, faults

def main():
    st.title('Optimal Page Replacement Algorithm Visualization')
    # Input for page reference sequence
    page_sequence = st.text_input('Enter the page reference sequence (comma-separated numbers):')
    if page_sequence:
        try:
            pages = [int(page.strip()) for page in page_sequence.split(",")]
        except ValueError:
            st.error("Invalid input! Please enter a valid sequence of comma-separated numbers.")
            return
    else:
        st.warning("Please enter a page reference sequence.")
        return

    # Input for memory capacity
    capacity = st.number_input('Enter the memory capacity:', min_value=1, step=1)


    if st.button('Visualize'):
        page_faults, faults = optimal_page_replacement(pages, capacity)
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(range(len(pages)), pages, marker='o', linestyle='-', color='b', label='Page References')
        ax.plot(faults, [pages[i] for i in faults], 'rx', label='Page Fault')
        ax.set_xlabel('Time')
        ax.set_ylabel('Page')
        ax.set_title('Optimal Page Replacement Algorithm')
        ax.legend()
        st.pyplot(fig)

if __name__ == "__main__":
    main()




