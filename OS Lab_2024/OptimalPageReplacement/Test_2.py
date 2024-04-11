
import matplotlib.pyplot as plt


def optimal_page_replacement_visualization(pages, capacity):
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
                        future_refs[p] = pages.index(p, page_index + 1)
                    except ValueError:
                        future_refs[p] = float('inf')
               
                page_to_replace = max(future_refs, key=future_refs.get)
                page_table[page_table.index(page_to_replace)] = page
                page_faults += 1
                faults.append(page_index)


    return page_faults, faults


# Example usage
pages = [1, 3, 0, 3, 5, 6, 3]
capacity = 3
page_faults, faults = optimal_page_replacement_visualization(pages, capacity)


# Plotting
fig, ax = plt.subplots(figsize=(10, 6))


# Plotting the sequence of page references
ax.plot(range(len(pages)), pages, marker='o', linestyle='-', color='b', label='Page References')


# Marking the first page fault
if faults:
    ax.plot(faults[0], pages[faults[0]], marker='x', markersize=10, color='r', label='Page Fault')


# Marking the subsequent page faults without label
for fault_index in faults[1:]:
    ax.plot(fault_index, pages[fault_index], marker='x', markersize=10, color='r')


# Adding labels and legend
ax.set_xlabel('Time')
ax.set_ylabel('Page')
ax.set_title('Optimal Page Replacement Algorithm')
ax.legend()


plt.grid(True)
plt.tight_layout()
plt.show()
