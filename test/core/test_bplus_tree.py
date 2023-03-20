from dockie.core.bplus_tree import BPlusTree


def test_degree_is_set():
    degree = 4
    tree = BPlusTree(degree=degree)
    assert tree.degree == degree


def test_insert():
    tree = BPlusTree(degree=4)
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)

    assert tree.root.keys == [3]
    assert len(tree.root.children) == 2

    child1 = tree.root.children[0]
    assert child1.keys == [1, 2]
    assert child1.children == [None, None]

    child2 = tree.root.children[1]
    assert child2.keys == [3, 4, 5]
    assert child2.children == [None, None, None]


def test_search_found():
    tree = BPlusTree(degree=4)
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)

    assert tree.search(4) is True


def test_search_not_found():
    tree = BPlusTree(degree=4)
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)

    assert tree.search(10) is False


def test_split():
    split_notifications = []

    def on_split(msg, key):
        split_notifications.append((msg, key))

    tree = BPlusTree(degree=4, on_split=on_split)

    for i in range(1, 1000):
        tree.insert(i)

    leaf_splits = [tup for tup in split_notifications if tup[0] == "leaf"]
    non_leaf_splits = [tup for tup in split_notifications if tup[0] == "non-leaf"]

    leaf_split_count = len(leaf_splits)

    assert leaf_split_count == 498
    assert len(non_leaf_splits) == len(split_notifications) - leaf_split_count
