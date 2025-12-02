# Tree Simulator

A comprehensive tree data structure simulator supporting:
- Binary Search Trees (BST)
- Red-Black Trees
- AVL Trees
- Splay Trees
- 2-3 Trees

## Features

- Visual GUI for tree operations
- Three predefined test cases:
  - Case 1: 100 random nodes
  - Case 2: 1000 nodes (500 increasing + 500 random)
  - Case 3: 1000 nodes (500 random + 500 decreasing)
- Custom input support
- Timing analysis for insertions and deletions
- Node classification (leaf, parent, root)
- Export to text files

## Installation

```bash
pip install tkinter
```

Note: tkinter usually comes pre-installed with Python

## Usage

### Run the GUI:
```bash
python tree_gui.py
```

### GUI Operations:

1. **Select Tree Type**: Choose from BST, Red-Black, AVL, Splay, or 2-3 Tree
2. **Load Test Case**: Select one of the predefined cases or enter custom data
3. **Build Tree**: Constructs the tree and displays timing information
4. **Delete Operations**:
   - Delete Leaf Node: Remove a node with no children
   - Delete Parent (1 Child): Remove a node with one child
   - Delete Parent (2 Children): Remove a node with two children
5. **Save to Files**: Export tree structure, timing info, and node information

### Output Files:

- `tree_structure.txt`: Visual representation of the tree
- `timing_info.txt`: Insertion and deletion timing data
- `node_info.txt`: Root, leaf, and parent node information with operation logs

## Example

```python
from tree_simulator import BST, generate_test_cases

# Create a BST
tree = BST()

# Generate test data
case1, case2, case3 = generate_test_cases()

# Insert nodes
for key in case1:
    tree.insert(key)

# Print tree structure
print(tree.to_string())

# Delete a node
tree.delete(50)
```

## Tree Implementations

### Binary Search Tree (BST)
- Basic binary tree with left < parent < right property
- No balancing

### Red-Black Tree
- Self-balancing BST
- Each node has a color (red or black)
- Maintains balance through color properties and rotations

### AVL Tree
- Self-balancing BST
- Maintains height balance factor of -1, 0, or 1
- Uses rotations to maintain balance

### Splay Tree
- Self-adjusting BST
- Recently accessed elements are quick to access again
- Uses splaying operation to move nodes to root

### 2-3 Tree
- Each node can have 1-2 keys and 2-3 children
- Always balanced
- All leaves at same level

## Performance Analysis

The program measures:
- Total insertion time for all nodes
- Average insertion time per node
- Deletion time for different node types
- Tree height and structure

## Notes

- 2-3 Tree deletion is simplified in this implementation
- Red-Black Tree uses a simplified implementation
- All trees support the basic operations: insert, delete, search
- Tree visualization uses ASCII art for clarity
