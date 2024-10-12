import heapq
from collections import Counter

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(chars, freq):
    priority_queue = [Node(char, f) for char, f in zip(chars, freq)]
    heapq.heapify(priority_queue)

    # Build the Huffman tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code="", huffman_codes={}):
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)

    return huffman_codes

# Step 1: Get user input
user_input = input("Enter a string (Persian, numbers, and spaces are allowed): ")

# Step 2: Calculate frequency of each character in the user input
frequency = Counter(user_input)
chars = list(frequency.keys())
freq = list(frequency.values())

# Step 3: Build the Huffman tree
root = build_huffman_tree(chars, freq)

# Step 4: Generate Huffman codes
huffman_codes = generate_huffman_codes(root)

# Step 5: Print Huffman codes
print("\nHuffman Codes for the entered string:")
for char, code in huffman_codes.items():
    print(f"Character: {repr(char)}, Code: {code}")
