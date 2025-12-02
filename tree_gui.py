"""
GUI for Tree Simulator
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
from tree_simulator import *

class TreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tree Simulator - BST, RB, AVL, Splay, 2-3 Trees")
        self.root.geometry("1200x800")
        
        self.current_tree = None
        self.current_tree_name = ""
        self.test_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tree selection
        tree_frame = ttk.LabelFrame(main_frame, text="Select Tree Type", padding="10")
        tree_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.tree_var = tk.StringVar(value="BST")
        trees = [("Binary Search Tree", "BST"), 
                 ("Red-Black Tree", "RBTree"),
                 ("AVL Tree", "AVLTree"),
                 ("Splay Tree", "SplayTree"),
                 ("2-3 Tree", "Tree23")]
        
        for i, (label, value) in enumerate(trees):
            ttk.Radiobutton(tree_frame, text=label, variable=self.tree_var, 
                           value=value).grid(row=0, column=i, padx=5)
        
        # Test case selection
        case_frame = ttk.LabelFrame(main_frame, text="Select Test Case", padding="10")
        case_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(case_frame, text="Case 1: 100 Random", 
                  command=lambda: self.load_case(1)).grid(row=0, column=0, padx=5)
        ttk.Button(case_frame, text="Case 2: 1000 (500 Inc + 500 Random)", 
                  command=lambda: self.load_case(2)).grid(row=0, column=1, padx=5)
        ttk.Button(case_frame, text="Case 3: 1000 (500 Random + 500 Dec)", 
                  command=lambda: self.load_case(3)).grid(row=0, column=2, padx=5)
        ttk.Button(case_frame, text="Custom Input", 
                  command=self.custom_input).grid(row=0, column=3, padx=5)
        
        # Operations
        op_frame = ttk.LabelFrame(main_frame, text="Operations", padding="10")
        op_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(op_frame, text="Build Tree", 
                  command=self.build_tree).grid(row=0, column=0, padx=5)
        ttk.Button(op_frame, text="Delete Leaf Node", 
                  command=self.delete_leaf).grid(row=0, column=1, padx=5)
        ttk.Button(op_frame, text="Delete Parent (1 Child)", 
                  command=self.delete_parent_one).grid(row=0, column=2, padx=5)
        ttk.Button(op_frame, text="Delete Parent (2 Children)", 
                  command=self.delete_parent_two).grid(row=0, column=3, padx=5)
        ttk.Button(op_frame, text="Save to Files", 
                  command=self.save_to_files).grid(row=0, column=4, padx=5)
        
        # Tree visualization
        viz_frame = ttk.LabelFrame(main_frame, text="Tree Structure", padding="10")
        viz_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        
        self.tree_text = scrolledtext.ScrolledText(viz_frame, width=60, height=30, font=("Courier", 9))
        self.tree_text.pack(fill=tk.BOTH, expand=True)
        
        # Info panel
        info_frame = ttk.LabelFrame(main_frame, text="Information & Logs", padding="10")
        info_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, width=60, height=30, font=("Courier", 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.log("Tree Simulator Ready!")
    
    def log(self, message):
        """Add message to info panel"""
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
    
    def load_case(self, case_num):
        """Load test case data"""
        case1, case2, case3 = generate_test_cases()
        cases = {1: case1, 2: case2, 3: case3}
        self.test_data = cases[case_num]
        self.log(f"Loaded Case {case_num}: {len(self.test_data)} numbers")
        self.log(f"First 10 numbers: {self.test_data[:10]}")
    
    def custom_input(self):
        """Get custom input from user"""
        input_str = simpledialog.askstring("Custom Input", 
                                           "Enter numbers separated by spaces:")
        if input_str:
            try:
                self.test_data = [int(x) for x in input_str.split()]
                self.log(f"Loaded custom data: {len(self.test_data)} numbers")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter numbers only.")
    
    def build_tree(self):
        """Build the selected tree with test data"""
        if not self.test_data:
            messagebox.showwarning("Warning", "Please load test data first!")
            return
        
        tree_type = self.tree_var.get()
        tree_classes = {
            "BST": BST,
            "RBTree": RBTree,
            "AVLTree": AVLTree,
            "SplayTree": SplayTree,
            "Tree23": Tree23
        }
        
        self.log(f"\n{'='*50}")
        self.log(f"Building {tree_type}...")
        
        tree_class = tree_classes[tree_type]
        self.current_tree = tree_class()
        self.current_tree_name = tree_type
        
        # Time insertion with high precision
        start = time.perf_counter()
        for key in self.test_data:
            self.current_tree.insert(key)
        insert_time = time.perf_counter() - start
        
        # Display timing with appropriate units
        if insert_time < 0.001:
            self.log(f"Insertion completed in {insert_time*1000:.3f} milliseconds ({insert_time*1000000:.1f} microseconds)")
        else:
            self.log(f"Insertion completed in {insert_time:.6f} seconds")
        
        avg_time = insert_time/len(self.test_data)
        if avg_time < 0.000001:
            self.log(f"Average time per node: {avg_time*1000000000:.2f} nanoseconds")
        elif avg_time < 0.001:
            self.log(f"Average time per node: {avg_time*1000000:.3f} microseconds")
        else:
            self.log(f"Average time per node: {avg_time*1000:.3f} milliseconds")
        
        # Display tree
        tree_str = self.current_tree.to_string()
        self.tree_text.delete(1.0, tk.END)
        self.tree_text.insert(1.0, tree_str)
        
        # Display node info
        leaves = self.current_tree.find_leaf_nodes()
        parents = self.current_tree.find_parent_nodes()
        
        if hasattr(self.current_tree.root, 'key'):
            root_key = self.current_tree.root.key
        elif hasattr(self.current_tree.root, 'keys'):
            root_key = self.current_tree.root.keys
        else:
            root_key = None
        
        self.log(f"\nRoot Node: {root_key}")
        self.log(f"Leaf Nodes ({len(leaves)}): {sorted(leaves)[:20]}{'...' if len(leaves) > 20 else ''}")
        self.log(f"Parent Nodes ({len(parents)}): {sorted(parents)[:20]}{'...' if len(parents) > 20 else ''}")
        
        # Store timing info
        self.insert_time = insert_time
    
    def delete_leaf(self):
        """Delete a leaf node"""
        if not self.current_tree:
            messagebox.showwarning("Warning", "Please build a tree first!")
            return
        
        leaves = self.current_tree.find_leaf_nodes()
        if not leaves:
            messagebox.showinfo("Info", "No leaf nodes found!")
            return
        
        self.log(f"\nAvailable leaf nodes: {sorted(leaves)[:20]}")
        key = simpledialog.askinteger("Delete Leaf", "Enter leaf node value to delete:")
        
        if key is None:
            return
        
        if key not in leaves:
            messagebox.showwarning("Warning", f"{key} is not a leaf node!")
            return
        
        self.log(f"\n{'='*50}")
        self.log(f"Operation: DELETE LEAF NODE")
        self.log(f"Node to delete: {key}")
        
        start = time.perf_counter()
        success = self.current_tree.delete(key)
        delete_time = time.perf_counter() - start
        
        if success:
            # Display timing with appropriate units
            if delete_time < 0.000001:
                self.log(f"Deletion completed in {delete_time*1000000000:.2f} nanoseconds")
            elif delete_time < 0.001:
                self.log(f"Deletion completed in {delete_time*1000000:.3f} microseconds")
            else:
                self.log(f"Deletion completed in {delete_time*1000:.3f} milliseconds")
            self.log(f"Node {key} (leaf) deleted successfully")
            
            # Update display
            tree_str = self.current_tree.to_string()
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(1.0, tree_str)
            
            # Update node info
            leaves = self.current_tree.find_leaf_nodes()
            parents = self.current_tree.find_parent_nodes()
            self.log(f"Remaining leaf nodes: {len(leaves)}")
            self.log(f"Remaining parent nodes: {len(parents)}")
        else:
            self.log("Deletion failed!")
    
    def delete_parent_one(self):
        """Delete a parent node with one child"""
        if not self.current_tree:
            messagebox.showwarning("Warning", "Please build a tree first!")
            return
        
        key = simpledialog.askinteger("Delete Parent", 
                                     "Enter parent node value (with 1 child) to delete:")
        if key is None:
            return
        
        self.log(f"\n{'='*50}")
        self.log(f"Operation: DELETE PARENT NODE (1 CHILD)")
        self.log(f"Node to delete: {key}")
        
        start = time.perf_counter()
        success = self.current_tree.delete(key)
        delete_time = time.perf_counter() - start
        
        if success:
            # Display timing with appropriate units
            if delete_time < 0.000001:
                self.log(f"Deletion completed in {delete_time*1000000000:.2f} nanoseconds")
            elif delete_time < 0.001:
                self.log(f"Deletion completed in {delete_time*1000000:.3f} microseconds")
            else:
                self.log(f"Deletion completed in {delete_time*1000:.3f} milliseconds")
            self.log(f"Node {key} (parent with 1 child) deleted successfully")
            
            tree_str = self.current_tree.to_string()
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(1.0, tree_str)
        else:
            self.log("Deletion failed!")
    
    def delete_parent_two(self):
        """Delete a parent node with two children"""
        if not self.current_tree:
            messagebox.showwarning("Warning", "Please build a tree first!")
            return
        
        key = simpledialog.askinteger("Delete Parent", 
                                     "Enter parent node value (with 2 children) to delete:")
        if key is None:
            return
        
        self.log(f"\n{'='*50}")
        self.log(f"Operation: DELETE PARENT NODE (2 CHILDREN)")
        self.log(f"Node to delete: {key}")
        
        start = time.perf_counter()
        success = self.current_tree.delete(key)
        delete_time = time.perf_counter() - start
        
        if success:
            # Display timing with appropriate units
            if delete_time < 0.000001:
                self.log(f"Deletion completed in {delete_time*1000000000:.2f} nanoseconds")
            elif delete_time < 0.001:
                self.log(f"Deletion completed in {delete_time*1000000:.3f} microseconds")
            else:
                self.log(f"Deletion completed in {delete_time*1000:.3f} milliseconds")
            self.log(f"Node {key} (parent with 2 children) deleted successfully")
            
            tree_str = self.current_tree.to_string()
            self.tree_text.delete(1.0, tk.END)
            self.tree_text.insert(1.0, tree_str)
        else:
            self.log("Deletion failed!")
    
    def save_to_files(self):
        """Save tree structure and timing info to files"""
        if not self.current_tree:
            messagebox.showwarning("Warning", "Please build a tree first!")
            return
        
        # File 1: Tree structure
        tree_str = self.current_tree.to_string()
        with open("tree_structure.txt", "w", encoding="utf-8") as f:
            f.write(f"Tree Type: {self.current_tree_name}\n")
            f.write(f"Number of nodes: {len(self.test_data)}\n")
            f.write("="*60 + "\n\n")
            f.write(tree_str)
        
        # File 2: Timing information
        with open("timing_info.txt", "w", encoding="utf-8") as f:
            f.write(f"Tree Type: {self.current_tree_name}\n")
            f.write(f"Number of nodes: {len(self.test_data)}\n")
            f.write("="*60 + "\n\n")
            f.write(f"Insertion Time: {self.insert_time:.6f} seconds\n")
            f.write(f"Average time per insertion: {self.insert_time/len(self.test_data):.8f} seconds\n")
            f.write("\nNote: Perform deletion operations and check logs for deletion times\n")
        
        # File 3: Node information
        leaves = self.current_tree.find_leaf_nodes()
        parents = self.current_tree.find_parent_nodes()
        
        if hasattr(self.current_tree.root, 'key'):
            root_key = self.current_tree.root.key
        elif hasattr(self.current_tree.root, 'keys'):
            root_key = self.current_tree.root.keys
        else:
            root_key = None
        
        with open("node_info.txt", "w", encoding="utf-8") as f:
            f.write(f"Tree Type: {self.current_tree_name}\n")
            f.write("="*60 + "\n\n")
            f.write(f"ROOT NODE:\n{root_key}\n\n")
            f.write(f"LEAF NODES ({len(leaves)}):\n")
            f.write(f"{sorted(leaves)}\n\n")
            f.write(f"PARENT NODES ({len(parents)}):\n")
            f.write(f"{sorted(parents)}\n\n")
            f.write("\nOperations Log:\n")
            f.write(self.info_text.get(1.0, tk.END))
        
        self.log("\nFiles saved successfully!")
        self.log("- tree_structure.txt")
        self.log("- timing_info.txt")
        self.log("- node_info.txt")
        
        messagebox.showinfo("Success", "Files saved successfully!")

def main():
    root = tk.Tk()
    app = TreeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
