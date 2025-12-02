"""
Tree Simulator - BST, Red-Black, AVL, Splay, and 2-3 Trees
"""
import time
import random
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Base Node Classes
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class RBNode(BSTNode):
    def __init__(self, key):
        super().__init__(key)
        self.color = "RED"  # New nodes are red

class AVLNode(BSTNode):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1

class SplayNode(BSTNode):
    pass

class Node23:
    def __init__(self):
        self.keys = []
        self.children = []
        self.parent = None
    
    def is_leaf(self):
        return len(self.children) == 0

# Base Tree Class
class Tree(ABC):
    def __init__(self):
        self.root = None
        self.operations_log = []
    
    @abstractmethod
    def insert(self, key):
        pass
    
    @abstractmethod
    def delete(self, key):
        pass
    
    @abstractmethod
    def to_string(self):
        pass
    
    def find_leaf_nodes(self):
        """Find all leaf nodes"""
        leaves = []
        self._find_leaves(self.root, leaves)
        return leaves
    
    def _find_leaves(self, node, leaves):
        if node is None:
            return
        if hasattr(node, 'is_leaf') and node.is_leaf():
            leaves.extend(node.keys)
        elif hasattr(node, 'left'):
            if node.left is None and node.right is None:
                leaves.append(node.key)
            else:
                self._find_leaves(node.left, leaves)
                self._find_leaves(node.right, leaves)
        else:
            for child in node.children:
                self._find_leaves(child, leaves)
    
    def find_parent_nodes(self):
        """Find all parent nodes"""
        parents = []
        self._find_parents(self.root, parents)
        return parents
    
    def _find_parents(self, node, parents):
        if node is None:
            return
        if hasattr(node, 'children'):
            if len(node.children) > 0:
                parents.extend(node.keys)
                for child in node.children:
                    self._find_parents(child, parents)
        elif hasattr(node, 'left'):
            if node.left is not None or node.right is not None:
                parents.append(node.key)
            self._find_parents(node.left, parents)
            self._find_parents(node.right, parents)

# Binary Search Tree
class BST(Tree):
    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert_recursive(self.root, key)
    
    def _insert_recursive(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
                node.left.parent = node
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = BSTNode(key)
                node.right.parent = node
            else:
                self._insert_recursive(node.right, key)
    
    def delete(self, key):
        node = self._search(self.root, key)
        if node is None:
            return False
        self._delete_node(node)
        return True
    
    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    
    def _delete_node(self, node):
        if node.left is None and node.right is None:
            self._replace_node(node, None)
        elif node.left is None:
            self._replace_node(node, node.right)
        elif node.right is None:
            self._replace_node(node, node.left)
        else:
            successor = self._find_min(node.right)
            node.key = successor.key
            self._delete_node(successor)
    
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def _replace_node(self, node, new_node):
        if node.parent is None:
            self.root = new_node
        elif node == node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node
        if new_node is not None:
            new_node.parent = node.parent
    
    def to_string(self):
        lines = []
        self._build_tree_string(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _build_tree_string(self, node, prefix, is_tail, lines):
        if node is not None:
            lines.append(prefix + ("└── " if is_tail else "├── ") + str(node.key))
            children = [node.left, node.right]
            for i, child in enumerate(children):
                if child is not None:
                    extension = "    " if is_tail else "│   "
                    self._build_tree_string(child, prefix + extension, i == len([c for c in children if c]) - 1, lines)

# AVL Tree
class AVLTree(Tree):
    def insert(self, key):
        self.root = self._insert(self.root, key)
    
    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
            node.left.parent = node
        else:
            node.right = self._insert(node.right, key)
            node.right.parent = node
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)
        
        # Left Left
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        # Right Right
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        # Left Right
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right Left
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _get_height(self, node):
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        y.parent = z.parent
        z.parent = y
        if T2:
            T2.parent = z
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def _rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        y.parent = z.parent
        z.parent = y
        if T3:
            T3.parent = z
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def delete(self, key):
        self.root = self._delete(self.root, key)
        return True
    
    def _delete(self, node, key):
        if node is None:
            return node
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        
        if node is None:
            return node
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)
        
        # Left Left
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        # Left Right
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right Right
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        # Right Left
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def to_string(self):
        lines = []
        self._build_tree_string(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _build_tree_string(self, node, prefix, is_tail, lines):
        if node is not None:
            lines.append(prefix + ("└── " if is_tail else "├── ") + f"{node.key}(h={node.height})")
            children = [node.left, node.right]
            for i, child in enumerate(children):
                if child is not None:
                    extension = "    " if is_tail else "│   "
                    self._build_tree_string(child, prefix + extension, i == len([c for c in children if c]) - 1, lines)

# Splay Tree
class SplayTree(Tree):
    def insert(self, key):
        if self.root is None:
            self.root = SplayNode(key)
        else:
            self.root = self._splay(self.root, key)
            if key < self.root.key:
                new_node = SplayNode(key)
                new_node.left = self.root.left
                new_node.right = self.root
                if self.root.left:
                    self.root.left.parent = new_node
                self.root.left = None
                self.root.parent = new_node
                self.root = new_node
            elif key > self.root.key:
                new_node = SplayNode(key)
                new_node.right = self.root.right
                new_node.left = self.root
                if self.root.right:
                    self.root.right.parent = new_node
                self.root.right = None
                self.root.parent = new_node
                self.root = new_node
    
    def _splay(self, node, key):
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            if node.left is None:
                return node
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._rotate_right(node)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right:
                    node.left = self._rotate_left(node.left)
            return self._rotate_right(node) if node.left else node
        else:
            if node.right is None:
                return node
            if key > node.right.key:
                node.right.right = self._splay(node.right.right, key)
                node = self._rotate_left(node)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left:
                    node.right = self._rotate_right(node.right)
            return self._rotate_left(node) if node.right else node
    
    def _rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.right = node
        left_child.parent = node.parent
        node.parent = left_child
        return left_child
    
    def _rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.left = node
        right_child.parent = node.parent
        node.parent = right_child
        return right_child
    
    def delete(self, key):
        if self.root is None:
            return False
        self.root = self._splay(self.root, key)
        if self.root.key != key:
            return False
        
        if self.root.left is None:
            self.root = self.root.right
            if self.root:
                self.root.parent = None
        else:
            right = self.root.right
            self.root = self.root.left
            self.root.parent = None
            self.root = self._splay(self.root, key)
            self.root.right = right
            if right:
                right.parent = self.root
        return True
    
    def to_string(self):
        lines = []
        self._build_tree_string(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _build_tree_string(self, node, prefix, is_tail, lines):
        if node is not None:
            lines.append(prefix + ("└── " if is_tail else "├── ") + str(node.key))
            children = [node.left, node.right]
            for i, child in enumerate(children):
                if child is not None:
                    extension = "    " if is_tail else "│   "
                    self._build_tree_string(child, prefix + extension, i == len([c for c in children if c]) - 1, lines)

# Red-Black Tree (simplified)
class RBTree(BST):
    def insert(self, key):
        new_node = RBNode(key)
        if self.root is None:
            self.root = new_node
            self.root.color = "BLACK"
        else:
            self._insert_node(self.root, new_node)
            self._fix_insert(new_node)
    
    def _insert_node(self, root, node):
        if node.key < root.key:
            if root.left is None:
                root.left = node
                node.parent = root
            else:
                self._insert_node(root.left, node)
        else:
            if root.right is None:
                root.right = node
                node.parent = root
            else:
                self._insert_node(root.right, node)
    
    def _fix_insert(self, node):
        while node != self.root and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left_rb(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_right_rb(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right_rb(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._rotate_left_rb(node.parent.parent)
        self.root.color = "BLACK"
    
    def _rotate_left_rb(self, node):
        right = node.right
        node.right = right.left
        if right.left:
            right.left.parent = node
        right.parent = node.parent
        if node.parent is None:
            self.root = right
        elif node == node.parent.left:
            node.parent.left = right
        else:
            node.parent.right = right
        right.left = node
        node.parent = right
    
    def _rotate_right_rb(self, node):
        left = node.left
        node.left = left.right
        if left.right:
            left.right.parent = node
        left.parent = node.parent
        if node.parent is None:
            self.root = left
        elif node == node.parent.right:
            node.parent.right = left
        else:
            node.parent.left = left
        left.right = node
        node.parent = left
    
    def to_string(self):
        lines = []
        self._build_tree_string_rb(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _build_tree_string_rb(self, node, prefix, is_tail, lines):
        if node is not None:
            color = "R" if node.color == "RED" else "B"
            lines.append(prefix + ("└── " if is_tail else "├── ") + f"{node.key}({color})")
            children = [node.left, node.right]
            for i, child in enumerate(children):
                if child is not None:
                    extension = "    " if is_tail else "│   "
                    self._build_tree_string_rb(child, prefix + extension, i == len([c for c in children if c]) - 1, lines)

# 2-3 Tree (simplified)
class Tree23(Tree):
    def insert(self, key):
        if self.root is None:
            self.root = Node23()
            self.root.keys = [key]
        else:
            result = self._insert(self.root, key)
            if result:
                self.root = result
    
    def _insert(self, node, key):
        # Don't insert duplicates
        if key in node.keys:
            return None
        
        if node.is_leaf():
            node.keys.append(key)
            node.keys.sort()
            if len(node.keys) > 2:
                return self._split(node)
            return None
        else:
            # Find correct child
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            
            # Ensure children list is properly sized
            while len(node.children) <= i:
                node.children.append(None)
            
            # If child doesn't exist, create it
            if node.children[i] is None:
                node.children[i] = Node23()
                node.children[i].parent = node
            
            result = self._insert(node.children[i], key)
            
            if result:
                # Child was split, need to insert into this node
                mid_key = result.keys[0]
                node.keys.append(mid_key)
                node.keys.sort()
                
                # Update children
                key_index = node.keys.index(mid_key)
                node.children[key_index] = result.children[0]
                node.children.insert(key_index + 1, result.children[1])
                
                result.children[0].parent = node
                result.children[1].parent = node
                
                if len(node.keys) > 2:
                    return self._split(node)
            
            return None
    
    def _split(self, node):
        mid_key = node.keys[1]
        
        left = Node23()
        left.keys = [node.keys[0]]
        
        right = Node23()
        right.keys = [node.keys[2]]
        
        if not node.is_leaf():
            left.children = node.children[:2]
            right.children = node.children[2:4]
            
            for child in left.children:
                if child:
                    child.parent = left
            for child in right.children:
                if child:
                    child.parent = right
        
        new_parent = Node23()
        new_parent.keys = [mid_key]
        new_parent.children = [left, right]
        left.parent = new_parent
        right.parent = new_parent
        
        return new_parent
    
    def delete(self, key):
        # Simplified deletion - not fully implemented
        return False
    
    def to_string(self):
        lines = []
        self._build_tree_string_23(self.root, "", True, lines)
        return "\n".join(lines)
    
    def _build_tree_string_23(self, node, prefix, is_tail, lines):
        if node is not None:
            lines.append(prefix + ("└── " if is_tail else "├── ") + str(node.keys))
            for i, child in enumerate(node.children):
                if child is not None:
                    extension = "    " if is_tail else "│   "
                    self._build_tree_string_23(child, prefix + extension, i == len(node.children) - 1, lines)

def generate_test_cases():
    """Generate three test cases"""
    # Case 1: 100 random numbers
    case1 = random.sample(range(1, 1001), 100)
    
    # Case 2: First 500 increasing, next 500 random
    case2 = list(range(1, 501)) + random.sample(range(501, 2001), 500)
    
    # Case 3: First 500 random, next 500 decreasing
    case3 = random.sample(range(1, 501), 500) + list(range(1000, 500, -1))
    
    return case1, case2, case3

def test_tree(tree_class, name, data):
    """Test a tree with given data"""
    tree = tree_class()
    
    # Insertion timing
    start = time.time()
    for key in data:
        tree.insert(key)
    insert_time = time.time() - start
    
    # Get tree structure
    tree_str = tree.to_string()
    
    # Find nodes
    leaves = tree.find_leaf_nodes()
    parents = tree.find_parent_nodes()
    root_key = tree.root.key if hasattr(tree.root, 'key') else tree.root.keys[0] if tree.root else None
    
    return tree, insert_time, tree_str, leaves, parents, root_key

if __name__ == "__main__":
    print("Tree Simulator - Use GUI for full functionality")
    print("Run: python tree_simulator.py")
