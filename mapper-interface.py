import argparse
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
        self.mappings = []

    def load(self, filename, sheet):
        """Store texts from filename in self.lines as a list of lines"""
        with pd.ExcelFile(filename) as xlsx:
            df = pd.read_excel(xlsx, sheet, na_filter='')
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
            if line[2]:
                self.mappings.append(('.'.join([node.input, line[0].strip()]), line[2]))
        return self

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

    def generate(self):
        with open('/'.join(['.', args.output, 'mappings.csv']), 'w') as f:
            for mapping in self.mappings:
                f.write(','.join(mapping))
                f.write('\n')

if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser(description='Parses a mapping excel and generates a list of mappings in CSV')
    parser.add_argument('-f', '--filename', type=str, default='./sample/mapping.xlsx', help='name of mapping excel file')
    parser.add_argument('-s', '--sheet', type=str, default='Sheet 2', help='name of sheet to parse in excel file')
    parser.add_argument('-o', '--output', type=str, default='output', help='name of output directory')
    args = parser.parse_args()

    m = MapperInterface()
    m.load(args.filename, args.sheet).parse().generate()