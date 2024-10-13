import heapq
from collections import Counter

# Define the Node class for the Huffman Tree
class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

# Function to build the Huffman Tree
def build_huffman_tree(chars, freq):
    priority_queue = [Node(char, f) for char, f in zip(chars, freq)]
    heapq.heapify(priority_queue)

    # Build the Huffman Tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

# Function to generate Huffman codes from the tree
def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)

    return huffman_codes

# Get input from the user
user_input = input("Enter a string: ")

# Calculate the frequency of each character
frequency = Counter(user_input)
chars = list(frequency.keys())
freq = list(frequency.values())

#  Build the Huffman Tree
root = build_huffman_tree(chars, freq)

# Generate Huffman codes
huffman_codes = generate_huffman_codes(root)

#Sort characters by frequency in descending order
sorted_by_freq = sorted(frequency.items(), key=lambda item: (-item[1], item[0]))

# Print Huffman codes based on frequency order
print("\nHuffman Codes for the entered string:")
for char, _ in sorted_by_freq:
    print(f"Character: {repr(char)}, Code: {huffman_codes[char]}")
