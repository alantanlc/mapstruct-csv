import pandas as pd

class Node:

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.children = []

    def add(self, node):
        self.children.append(node)

class MapperInterface:

    def __init__(self):
        self.filename = None
        self.lines = []
        self.root = None

    def load(self, filename, sheet):
        """Store texts from filename in self.lines as a list of lines"""
        with pd.ExcelFile(filename) as xlsx:
            df = pd.read_excel(xlsx, sheet)
            self.lines = [(x[1], x[2], x[3]) for x in df.values[5:]]
        return self

    def parse(self):
        """Parse self.lines to self.tree.
        Use self.load(self, filename) to load text from file into self.lines first.
        If successful, self.tree will contain a representation of 
        message and its corresponding mapping in the form of 
        a tree data structure.
        """
        self.root = Node(self.lines[0][0], self.lines[0][2])
        for line in self.lines[1:]:
            depth = self.get_depth_from_value(line[0])
            node = self.get_last_node_at_depth(self.root, depth - 1)
            node.add(Node('.'.join([node.input, line[0].strip()]), line[2]))

    def get_depth_from_value(self, value):
        """Return the node depth based on number of spaces in the beginning of value.
        Two consecutive spaces correspond to a depth of one.
        """
        return (len(value.split(' ')) - 1) // 2

    def get_last_node_at_depth(self, root, depth):
        """Return the last node at given depth in the tree"""
        curr = 0
        node = root
        while curr < depth:
            node = node.children[-1]
            curr += 1
        return node

if __name__ == '__main__':
    m = MapperInterface()
    m.load('./sample/message.xlsx', 'Mapping').parse()
    print('hello')