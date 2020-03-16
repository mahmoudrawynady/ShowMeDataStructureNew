# Explanation for Problem 3: Huffman Coding

This document provides an explanation for the design decisions and implementation.

## Summary

1. Efficiency: worst case of O(n log n) time and a O(n) space.
2. Data structures include: dictionary, list, and a priority queue that leverages a binary heap tree.

## Data Structures

This problem uses multiple data structures for different purposes:

| Purpose | Data Structure |
| ------- | -------------- |
| Priority queue | Python's Priority Queue using heap |
| Frequencies | dictionary |
| Frequencies map | list of tuples |
| Tree | Binary heap tree |
| Code map | dictionary|

## Efficiencies

The overall efficiencies is O(n log n) time and O(n) space.

The `huffman_encoding` function is O(n log n) time and O(n) space, where n is the number of characters in the given data string.

```python
def huffman_encoding(data):
    if not bool(data):
        return '', None

    # Step 1: Map the frequencies.
    frequencies = map_frequency(data)               # O(n) time and space

    # Step 2: Build the Huffman Tree.
    tree = build_tree(frequencies)                  # O(n log n) time and O(n) space

    # Step 3: Map the codes from the Huffman Tree.
    code_mappings = map_codes(tree, '', dict())     # O(n) time and space

    # Step 4: Encode the original data using the code mappings from the Huffman Tree.
    encoding = ''
    for char in data:                               # O(n), where n is the number of characters in the given data string.
        encoding += code_mappings[char]

    return encoding, tree
```

The `huffman_decoding` function is O(n) time and space, where n is the number of characters in the given data string.

```python
def huffman_decoding(data, tree):
    decoded = ''
    node = tree

    for bit in data:                                # O(n), where n is the number of characters in the given data string.   

        # Walk to the left child.
        if int(bit) == 0:
            if type(node.left_child) is HuffmanNode:
                node = node.left_child

        # Walk to the right child.
        else:
            if type(node.right_child) is HuffmanNode:
                node = node.right_child

        # If leaf, capture the char and rewind to the root.
        if node.left_child is None and node.right_child is None:
            decoded += node.char
            node = tree

    return decoded
```

### `map_frequency`

The efficiency for this function is:

* O(n) time
* O(n) space

where `n` is the number of characters in the given `data` string.

```python
def map_frequency(data):
    frequencies = dict()

    if not bool(data):
        return frequencies

    total = 0
    for char in data:                                           # O(c) where c is number of characters in the given `data` string.
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
        total += 1

    map = list()
    for char, freq in frequencies.items():                      # O(n)
        map.append((freq, char, HuffmanNode(freq, char)))       # O(1)

    return map
```

### `build_tree`

The efficiency for this function is:

* O(n log n) time
* O(n) space

The n x log n occurs when first loading the priority queue.  Each `put` is a `log n` times the number of times its invoked.

```python
def build_tree(frequencies):
    if len(frequencies) == 0:
        return

    queue = HuffmanQueue()
    for f in frequencies:                                       # O(n)
        queue.put(f)                                            #   O(n log n) as each put is (log n) x n

    p3 = 0
    while queue.qsize() > 1:
        # Pop the 1st 2 entries.
        lt_freq, lt_char, lt_node = queue.get()                 # O(n)
        rt_freq, rt_char, rt_node = queue.get()                 # O(n)

        # Build the parent node.
        p_freq = lt_freq + rt_freq
        parent = HuffmanNode(p_freq, None)
        parent.left_child = lt_node
        parent.right_child = rt_node

        # str(p3) is just in case the priority queue needs to compare parent to a leaf when sorting the binary tree.
        queue.put_items(p_freq, str(p3), parent)                # O(log n)
        p3 += 1

    root = queue.get()                                          # O(n)
    return root[3]
```

### `map_codes`

The efficiency for this function is:

* O(n) time
* O(n) space

where n is the number of nodes in the tree.


```python
def map_codes(node, code, map):
    """
    Map the codes of the Huffman Tree by recursively walking root to leaf.

    :param node: Current HuffmanNode
    :param code: The current code of 1s and 0s.
    :param map: Dictionary of code mappings
    :return: Dictionary of code mappings where char is the key and the code is the value.
    """

    if type(node.left_child) is HuffmanNode:
        map_codes(node.left_child, code + '0', map)
    else:
         map[node.char] = code

    if type(node.right_child) is HuffmanNode:
        map_codes(node.right_child, code + '1', map)
    else:
        map[node.char] = code

    return map
```

## Design Considerations

### Priority Queue

My initial implementation was with a list.  However, that required a separate sorting task after building the frequencies map O(n log n) and then each time a parent node was appended during the tree build O(n x (n log n)). Ouch.

I switched to the typical implementation with a heap.  What was the result?

1. The frequencies map no longer needed to be sorted.  That reduced its time efficiency from O(n log n) to O(n).
2. The tree building function still incurs a O(n log n), but only when first loading the frequencies map into it.  After that, each parent put into the queue is a O(log n) time.

### Mapping the Codes for Encoding

Before encoding begins, the tree is converted into a code map, which is a dictionary.  I chose this design to minimize repetitively walking the tree for the same character.  With the map, it's a O(1) lookup for each character. 
