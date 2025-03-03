import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.path import Path
import matplotlib.patches as patches

# Load hanzi data from the Make Me a Hanzi file
def load_hanzi_data(character, filename='test\\graphics.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data['character'] == character:
                    print(f"Found data for character '{character}'")
                    print(f"Number of strokes: {len(data['strokes'])}")
                    return data
        print(f"No data found for character '{character}'")
        return None
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

# Parse stroke data into matplotlib-compatible format
def parse_strokes(hanzi_data):
    strokes = []
    bounds = hanzi_data['bounds']  # [x_min, y_min, x_max, y_max]
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    commands = {'M', 'L', 'Q', 'C'}  # Add lowercase 'm', 'l', 'q', 'c' if needed

    def is_command(token):
        return token in commands

    for stroke in hanzi_data['strokes']:
        tokens = stroke.split()
        vertices = []
        codes = []
        i = 0
        current_command = None

        while i < len(tokens):
            if is_command(tokens[i]):
                current_command = tokens[i]
                i += 1
                if current_command == 'M' and i + 1 < len(tokens):
                    x = float(tokens[i])
                    y = float(tokens[i+1])
                    vertices.append((x, y))
                    codes.append(Path.MOVETO)
                    i += 2
                # Handle 'L', 'Q', 'C' if present
                elif current_command == 'L' and i + 1 < len(tokens):
                    x = float(tokens[i])
                    y = float(tokens[i+1])
                    vertices.append((x, y))
                    codes.append(Path.LINETO)
                    i += 2
            else:
                # Process coordinates based on current_command
                if current_command in ('M', 'L') and i + 1 < len(tokens):
                    x = float(tokens[i])
                    y = float(tokens[i+1])
                    vertices.append((x, y))
                    codes.append(Path.LINETO)
                    i += 2
                else:
                    i += 1  # Skip if insufficient tokens

        if vertices:
            # Normalize coordinates
            for j in range(len(vertices)):
                x, y = vertices[j]
                x = (x - bounds[0]) / width
                y = 1 - (y - bounds[1]) / height
                vertices[j] = (x, y)
            strokes.append((vertices, codes))

    if not strokes:
        print("No valid strokes to animate.")
    return strokes


# Create animation to display stroke order
def create_animation(character):
    hanzi_data = load_hanzi_data(character)
    if not hanzi_data:
        return None
    
    strokes = parse_strokes(hanzi_data)
    if not strokes:
        print("No valid strokes to animate.")
        return None
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"Stroke Order of '{character}'", fontsize=20)
    
    # Pre-create all stroke patches, initially invisible
    path_patches = []
    for vertices, codes in strokes:
        path = Path(vertices, codes)
        patch = patches.PathPatch(path, facecolor='none', edgecolor='black', linewidth=3, alpha=0.8)
        patch.set_visible(False)
        ax.add_patch(patch)
        path_patches.append(patch)
    
    # Animation initialization: all patches invisible
    def init():
        for patch in path_patches:
            patch.set_visible(False)
        return path_patches
    
    # Animation update: make strokes visible one by one
    def update(frame):
        if frame < len(path_patches):
            path_patches[frame].set_visible(True)
        return path_patches
    
    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(strokes) + 10,
                                  init_func=init, blit=True, interval=500)
    
    return ani

# Example usage
character = '永'  # Replace with any Chinese character
ani = create_animation(character)
if ani:
    # Save as GIF
    ani.save(f'{character}_strokes.gif', writer='pillow', fps=2)
    # Display the animation
    plt.show()