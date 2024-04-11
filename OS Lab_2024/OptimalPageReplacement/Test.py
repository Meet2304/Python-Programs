import streamlit as st  # Import the Streamlit library for building web apps
import matplotlib.pyplot as plt  # Import the pyplot module from Matplotlib for plotting

# Define a function for the Optimal Page Replacement Algorithm
def optimal_page_replacement(pages, capacity):
    page_faults = 0  # Initialize page fault counter
    page_table = []  # Initialize page table to store pages currently in memory

    # Iterate over each page in the sequence of page references
    for page in pages:
        # Check if the current page is not in the page table (indicating a page fault)
        if page not in page_table:
            # If there is space in the page table, add the current page
            if len(page_table) < capacity:
                page_table.append(page)
            else:
                future_refs = {}  # Dictionary to store future references of pages in the page table
                # Iterate over each page currently in the page table
                for p in page_table:
                    try:
                        # Find the index of the next occurrence of the current page in the page references sequence
                        future_refs[p] = pages.index(p, pages.index(page) + 1)
                    except ValueError:
                        # If the page is not found in the future references, assign infinity
                        future_refs[p] = float('inf')

                # Find the page in the page table with the maximum future reference
                page_to_replace = max(future_refs, key=future_refs.get)
                # Replace the page with the maximum future reference with the current page
                page_table[page_table.index(page_to_replace)] = page
                # Increment the page fault counter
                page_faults += 1
                # Write a message indicating the page replacement and current page faults to the Streamlit app
                st.write(f"Page {page_to_replace} replaced by {page}. Page faults: {page_faults}")
        # Write the current state of the page table to the Streamlit app
        st.write(f"Current page table: {page_table}")
    
    # Return the total number of page faults
    return page_faults

# Define the main function for the Streamlit app
def main():
    st.title('Optimal Page Replacement Algorithm Visualization')  # Set the title of the app

    # Input for page reference sequence
    page_sequence = st.text_input('Enter the page reference sequence (comma-separated numbers):')
    if page_sequence:
        try:
            pages = [int(page.strip()) for page in page_sequence.split(",")]  # Convert input to list of integers
        except ValueError:
            st.error("Invalid input! Please enter a valid sequence of comma-separated numbers.")
            return
    else:
        st.warning("Please enter a page reference sequence.")
        return

    # Input for memory capacity
    capacity = st.number_input('Enter the memory capacity:', min_value=1, step=1)

    # Button to visualize the algorithm
    if st.button('Visualize'):
        # Call the optimal_page_replacement function to perform the page replacement algorithm
        page_faults = optimal_page_replacement(pages, capacity)

        # Plotting the page references over time
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(range(len(pages)), pages, marker='o', linestyle='-', color='b', label='Page References')

        ax.set_xlabel('Time')  # Set the x-axis label
        ax.set_ylabel('Page')  # Set the y-axis label
        ax.set_title('Optimal Page Replacement Algorithm')  # Set the plot title
        ax.legend()  # Show the legend

        st.pyplot(fig)  # Display the plot in the Streamlit app

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
