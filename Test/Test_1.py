def min_operations_to_equal_price(prices, queries):
    result = []
    for query in queries:
        total_operations = 0
        for price in prices:
            total_operations += abs(price - query)
        result.append(total_operations)
    return result

# Example usage:
prices = [1, 2, 3]
queries = [3, 2, 1, 5]
print(min_operations_to_equal_price(prices, queries))
