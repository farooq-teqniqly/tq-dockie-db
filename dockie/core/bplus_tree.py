"""
bplus_tree.py: A basic implementation of a B+ tree data structure.

This module provides a B+ tree implementation with insert and search operations. It can be used to store
ordered data efficiently and perform ordered traversal.

The primary difference between a B+ tree and a Binary Search Tree (BST) is in the number of children a parent can have.
In a BST, each parent must have two children. In a B+ tree a parent can have between 2 and N children where N is the
degree of the tree. The root node is the only node that can have zero children. B+ trees are generally shallow and wide.
The benefit of this is that a search requires less node traversals. Also, nodes can be read in blocks, taking
advantage of cache lines.

Classes:
    BPlusTreeNode: Represents a node in the B+ tree.
    BPlusTree: Represents the B+ tree data structure.

Example:
    tree = BPlusTree(degree=4)
    tree.insert(5)
    tree.insert(10)
    tree.insert(15)
    tree.insert(20)
    tree.insert(25)

    print(tree.search(15))  # True
    print(tree.search(30))  # False

"""
from typing import Callable, Any


# pylint: disable=too-few-public-methods
class BPlusTreeNode:
    """A node in a B+ tree.

        Attributes:
            degree (int): The degree of the B+ tree.
            keys (list): The list of keys in the node.
            children (list): The list of children nodes.
            is_leaf (bool): True if the node is a leaf, otherwise False.
            next_leaf (BPlusTreeNode): The next leaf node in the tree.
    """

    def __init__(self, degree):
        """
                Initializes a B+ tree node.

                Args:
                    degree (int): The degree of the B+ tree.
        """
        self.degree = degree
        self.keys = []
        self.children = []
        self.is_leaf = True
        self.next_leaf = None

    def split(self):
        """
                Splits the node into two nodes if it is full.

                Returns:
                    tuple: A tuple containing the new node and its first key.
        """
        mid = self.degree // 2
        new_node = BPlusTreeNode(self.degree)
        new_node.keys = self.keys[mid:]
        new_node.children = self.children[mid:]
        self.keys = self.keys[:mid]
        self.children = self.children[:mid]

        if not self.is_leaf:
            new_node.is_leaf = False

        return new_node, new_node.keys[0]


# pylint: disable=too-few-public-methods
class BPlusTree:
    """A B+ tree data structure.

        Attributes:
            root (BPlusTreeNode): The root node of the tree.
            degree (int): The degree of the B+ tree.
            on_split (Callable[[str, Any], None], optional): A function that takes a string and key as
                    an argument and returns None. This function is called when a split occurs during the insertion
                    process. Defaults to None, in which case no callback is executed.
    """

    def __init__(self, degree=5, on_split: Callable[[str, Any], None] = None):
        """
                Initializes a B+ tree with the given degree.

                Args:
                    degree (int, optional): The degree of the B+ tree. Defaults to 5.
        """
        self.root = BPlusTreeNode(degree)
        self.degree = degree

        def noop(_, __):
            pass

        self.on_split = on_split or noop

    def _insert(self, node, key):
        """
                Recursively inserts a key into the tree, starting at the given node.

                Args:
                    node (BPlusTreeNode): The node to start the insertion process.
                    key (int): The key to insert.

                Returns:
                    tuple: A tuple containing the new node and its first key, if a split occurs.
        """
        if node.is_leaf:
            i = 0
            while i < len(node.keys) and node.keys[i] < key:
                i += 1
            node.keys.insert(i, key)
            node.children.insert(i, None)

            # Split if leaf node is full.
            if len(node.keys) >= node.degree:
                self.on_split("leaf", key)
                return node.split()

            return None, None

        i = 0
        while i < len(node.keys) and node.keys[i] <= key:
            i += 1

        new_node, new_key = self._insert(node.children[i], key)

        if new_key is not None:
            node.keys.insert(i, new_key)
            node.children.insert(i + 1, new_node)

            # Split if non-leaf node is full.
            if len(node.keys) >= node.degree:
                self.on_split("non-leaf", key)
                return node.split()

            return None, None

        return None, None

    def insert(self, key):
        """
                Inserts a key into the B+ tree.

                Args:
                    key (int): The key to insert.
        """
        new_node, new_key = self._insert(self.root, key)

        if new_key is not None:
            new_root = BPlusTreeNode(self.degree)
            new_root.keys = [new_key]
            new_root.children = [self.root, new_node]
            new_root.is_leaf = False
            self.root = new_root

    def search(self, key):
        """
                Searches for a key in the B+ tree.

                Args:
                    key (int): The key to search for.

                Returns:
                    bool: True if the key is found, otherwise False.
        """
        current = self.root

        while not current.is_leaf:
            i = 0
            while i < len(current.keys) and current.keys[i] <= key:
                i += 1
            current = current.children[i]

        return key in current.keys
