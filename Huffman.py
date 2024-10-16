import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import tkinter as tk

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node(char={self.char}, freq={self.freq})"

nodes = []
steps = []

# Calculate the frequency of each character in the string
def frequencies(word):
    global nodes
    freq_dict = {}
    for char in word:
        if char not in freq_dict:
            freq = word.count(char)
            freq_dict[char] = freq
            nodes.append(Node(char, freq))
    print("Frequencies:", freq_dict)

# Build the Huffman tree 
def huffman_tree(switch=False):
    global steps
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        
        left = nodes.pop(0)
        right = nodes.pop(0)

        if switch and left.freq < right.freq:
            left, right = right, left

        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        nodes.append(merged)
        
        steps.append(nodes.copy())
    
    return nodes[0]

# Generate Huffman codes for each character in the tree
def huffman_codes(node, current_code, codes):
    if node is None:
        return

    if node.char is not None:
        codes[node.char] = current_code

    huffman_codes(node.left, current_code + '0', codes)
    huffman_codes(node.right, current_code + '1', codes)

# Encode the given word using Huffman coding.
def encoding_words(word, switch=False):
    global nodes
    nodes = []
    steps.clear()
    frequencies(word)
    root = huffman_tree(switch)
    codes = {}
    huffman_codes(root, '', codes)
    return root, codes

# Image the Huffman tree with default colors 
def imagine_tree(frame_nodes, graph, pos=None, level=0, x=0.5, dx=0.1, parent=None, label=""):
    if pos is None:
        pos = {}

    for node in frame_nodes:
        pos[node] = (x, level)
        
        if node.left:
            pos = imagine_tree([node.left], graph, pos=pos, level=level-1, x=x-dx, dx=dx/2, parent=node, label='0')
        if node.right:
            pos = imagine_tree([node.right], graph, pos=pos, level=level-1, x=x+dx, dx=dx/2, parent=node, label='1')

        if parent:
            graph.add_edge(parent, node, label=label)

    return pos

# Update animation frame based on the current frame index
def update_anime(frame_index):
    plt.clf()
    graph = nx.DiGraph()

    frame_nodes = steps[frame_index]
    pos = imagine_tree(frame_nodes, graph)

    # Assign colors: pink for leaf nodes and gray for merged nodes
    node_colors = []
    for node in graph.nodes():
        if node.char is not None:  
            node_colors.append('pink')  
        else:  
            node_colors.append('gray') 

    nx.draw(graph, pos, with_labels=True, labels={node: f"{node.char or ''} ({node.freq})" for node in graph.nodes()}, 
            node_size=3000, node_color=node_colors, font_size=10, font_weight='bold', arrows=False)

    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=12)
    plt.title(f"Huffman Tree Construction Step {frame_index + 1}")

anim = None

# Create a custom error box
def show_error(message):
    error_window = tk.Toplevel(root_gui)
    error_window.title("Error")
    error_window.configure(bg='lightgray')
    
    label = tk.Label(error_window, text=message, bg='lightgray', fg='black', font=('Arial', 12))
    label.pack(pady=10)

    button = tk.Button(error_window, text="OK", command=error_window.destroy, bg='pink', fg='black', font=('Arial', 12))
    button.pack(pady=10)

# Show result
def result():
    global anim
    word = input_entry.get()
    
    if not word:
        show_error("Please enter a string.")
        return
    
    root, codes = encoding_words(word)

    result_label.config(text=f"Huffman Codes: {codes}")

    fig = plt.figure(figsize=(10, 8))
    anim = FuncAnimation(fig, update_anime, frames=len(steps), interval=1000, repeat=False)

    plt.show()

# Run Huffman encoding with the left child switch option enabled
def switching():
    global anim
    word = input_entry.get()
    
    if not word:
        show_error("Please enter a valid string.")
        return
    
    root, codes = encoding_words(word, switch=True)

    result_label.config(text=f"Huffman Codes (switched): {codes}")

    fig = plt.figure(figsize=(10, 8))
    anim = FuncAnimation(fig, update_anime, frames=len(steps), interval=1000, repeat=False)

    plt.show()

root_gui = tk.Tk()
root_gui.title("Huffman Encoding Animation")

input_label = tk.Label(root_gui, text="Enter a word or sentence:", bg='#D3D3D3', fg='black', font=('Arial', 12))
input_label.pack(pady=10)

input_entry = tk.Entry(root_gui, width=40, font=('Arial', 12), bg='#f0f0f0')
input_entry.pack(pady=5)

encode_button = tk.Button(root_gui, text="Encode", command=result, bg='#FFC0CB', fg='black', font=('Arial', 12), width=20)
encode_button.pack(pady=10)

switch_button = tk.Button(root_gui, text="Switch Left Child", command=switching, bg='#FFC0CB', fg='black', font=('Arial', 12), width=20)
switch_button.pack(pady=10)

result_label = tk.Label(root_gui, text="Huffman Codes will appear here.", bg='#D3D3D3', fg='black', font=('Arial', 12))
result_label.pack(pady=20)

root_gui.configure(bg='#D3D3D3')

root_gui.mainloop()
