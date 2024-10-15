import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node(char={self.char}, freq={self.freq})"

nodes = []
frames = []  # To store the intermediate steps for animation

def calculate_frequencies(word):
    global nodes
    frequencies = {}
    for char in word:
        if char not in frequencies:
            freq = word.count(char)
            frequencies[char] = freq
            nodes.append(Node(char, freq))
    print("Frequencies:", frequencies)

def build_huffman_tree():
    global frames
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        
        left = nodes.pop(0)
        right = nodes.pop(0)

        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        nodes.append(merged)
        
        # Capture the intermediate tree structure for animation
        frames.append(nodes.copy())
    
    return nodes[0]

def generate_huffman_codes(node, current_code, codes):
    if node is None:
        return

    if node.char is not None:
        codes[node.char] = current_code

    generate_huffman_codes(node.left, current_code + '0', codes)
    generate_huffman_codes(node.right, current_code + '1', codes)

def huffman_encoding(word):
    global nodes
    nodes = []
    frames.clear()  # Clear the frames for new input
    calculate_frequencies(word)
    root = build_huffman_tree()
    codes = {}
    generate_huffman_codes(root, '', codes)
    return root, codes

# Function to visualize the tree for a specific frame
def visualize_tree(frame_nodes, graph, pos=None, level=0, x=0.5, dx=0.1, parent=None, label=""):
    if pos is None:
        pos = {}

    for node in frame_nodes:
        pos[node] = (x, level)
        
        if node.left:
            pos = visualize_tree([node.left], graph, pos=pos, level=level-1, x=x-dx, dx=dx/2, parent=node, label='0')
        if node.right:
            pos = visualize_tree([node.right], graph, pos=pos, level=level-1, x=x+dx, dx=dx/2, parent=node, label='1')

        if parent:
            graph.add_edge(parent, node, label=label)

    return pos

# Animation function to update the plot at each frame
def update(frame_index):
    plt.clf()  # Clear the plot for each frame
    graph = nx.DiGraph()

    # Draw the Huffman tree for the current frame
    frame_nodes = frames[frame_index]
    pos = visualize_tree(frame_nodes, graph)

    nx.draw(graph, pos, with_labels=True, labels={node: f"{node.char or ''} ({node.freq})" for node in graph.nodes()}, 
            node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrows=False)

    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=12)
    plt.title(f"Huffman Tree Construction Step {frame_index + 1}")

# Function to handle the GUI input and display results
def run_huffman_encoding():
    word = input_entry.get()
    
    if not word:
        messagebox.showerror("Input Error", "Please enter a valid string.")
        return
    
    root, codes = huffman_encoding(word)

    # Show the Huffman codes
    result_label.config(text=f"Huffman Codes: {codes}")

    # Create the animation
    fig = plt.figure(figsize=(10, 8))
    anim = FuncAnimation(fig, update, frames=len(frames), interval=2500, repeat=False) # interval is for sleep of animation

    plt.show()

# Set up the GUI using tkinter
root_gui = tk.Tk()
root_gui.title("Huffman Encoding Animation")

# Create input field for user input
input_label = tk.Label(root_gui, text="Enter a word or sentence:")
input_label.pack()

input_entry = tk.Entry(root_gui, width=40)
input_entry.pack()

# Create a button to trigger Huffman encoding
encode_button = tk.Button(root_gui, text="Encode", command=run_huffman_encoding)
encode_button.pack()

# Label to display Huffman codes
result_label = tk.Label(root_gui, text="Huffman Codes will appear here.")
result_label.pack()

# Run the GUI loop
root_gui.mainloop()
