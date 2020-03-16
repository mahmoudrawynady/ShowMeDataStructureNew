import sys
from queue import PriorityQueue


def huffman_encoding(data):
    """
    Encodes the given string data using the Huffman Coding algorithm.
    :param data: String to be encoded.
    :return: tuple - encoded data, Huffman Tree
    """
    if not bool(data):
        return '', None

    # Step 1: Map the frequencies.
    frequencies = map_frequency(data)

    # Step 2: Build the Huffman Tree.
    tree = build_tree(frequencies)

    # Step 3: Map the codes from the Huffman Tree.
    code_mappings = map_codes(tree, '', dict())

    # Step 4: Encode the original data using the code mappings from the Huffman Tree.
    encoding = ''
    for char in data:
        encoding += code_mappings[char]

    return encoding, tree


def huffman_decoding(data, tree):
    """
    Decode the given encoded (compressed) data using the given Huffman Tree.
    :param data: the encoded data to be decoded.
    :param tree: the Huffman Tree used to encode the original, uncompressed data
    :return: string - the decoded data string
    """
    decoded = ''
    node = tree

    for bit in data:

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


class HuffmanNode:
    def __init__(self, freq, char):
        self.freq = freq
        self.char = char
        self.left_child = None
        self.right_child = None


def map_frequency(data):
    """
    Maps the character frequencies (counts) into a dictionary (hashtable).
    :param data: String to be mapped.
    :return: list of tuples, e.g. (frequency, probability, character)
    """
    frequencies = dict()

    if not bool(data):
        return frequencies

    total = 0
    for char in data:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
        total += 1

    map = list()

    # When there's a single character, set a dummy node to ensure we can build the tree.
    if len(frequencies) == 1:
        map.append((0, None, HuffmanNode(0, None)))

    for char, freq in frequencies.items():
        map.append((freq, char, HuffmanNode(freq, char)))

    return map


def build_tree(frequencies):
    """
    Builds the Huffman tree from the given frequencies list.
    :param frequencies: list of frequencies.
    :return: root of the binary tree
    """
    if len(frequencies) == 0:
        return

    queue = PriorityQueue()
    for f in frequencies:
        queue.put(f)

    p3 = 0
    while queue.qsize() > 1:
        # Pop the 1st 2 entries.
        lt_freq, lt_char, lt_node = queue.get()
        rt_freq, rt_char, rt_node = queue.get()

        # Build the parent node.
        p_freq = lt_freq + rt_freq
        parent = HuffmanNode(p_freq, None)
        parent.left_child = lt_node
        parent.right_child = rt_node

        # str(p3) is just in case the priority queue needs to compare parent to a leaf when sorting the binary tree.
        queue.put((p_freq, str(p3), parent))
        p3 += 1

    root = queue.get()
    return root[2]


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


if __name__ == '__main__':

    def run_edge_case_no_data():
        print('Running no data given edge case...')
        test_data = [
            '',
            None,
            False,
            {},
        ]
        for data in test_data:
            print(huffman_encoding(data))    # ('', None)

    def run_edge_case_repeating_char():
        print('\nRunning single repeating character edge case...')
        test_data = [
            'aaaaaa',
            'bbbbbb',
            '1111111',
        ]

        for data in test_data:
            print("Data: {}".format(data))
            print ("Data size: {}".format(sys.getsizeof(data)))

            encoded_data, tree = huffman_encoding(data)
            print("Encoded: {}".format(encoded_data))
            print ("Encoded size: {}".format(sys.getsizeof(int(encoded_data, base=2))))

            decoded_data = huffman_decoding(encoded_data, tree)
            print("Decoded: {}\n".format(decoded_data))
            print ("Decoded size: {}".format(sys.getsizeof(decoded_data)))

    def run_test_cases():
        print('\nRunning multiple strings...')
        test_data = [
            'n',
            'ab ba',
            'abc123'
            'Huffman coding',
            'ABRACADABRA',
            'Mississippi',
            'Sally sells seashells down by the seashore.'
        ]

        for data in test_data:
            print("Data: {}".format(data))
            print ("Data size: {}".format(sys.getsizeof(data)))

            encoded_data, tree = huffman_encoding(data)
            print("Encoded: {}".format(encoded_data))
            print ("Encoded size: {}".format(sys.getsizeof(int(encoded_data, base=2))))

            decoded_data = huffman_decoding(encoded_data, tree)
            print("Decoded: {}\n".format(decoded_data))
            print ("Decoded size: {}".format(sys.getsizeof(decoded_data)))

    run_edge_case_no_data()
    run_edge_case_repeating_char()
    run_test_cases()
