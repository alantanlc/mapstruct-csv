import re
import argparse

class Mapper:

    def __init__(self):
        self.mappings = {}
        self.lines = []
        self.filename = None
        self.regex = {
            'method': '[a-zA-Z0-9_]*\([a-zA-Z0-9 ,.]*\);',
            'source': '(source|constant|expression)[ ]?=[ ]?[\"]?[a-zA-Z0-9. ()]*[\"]?',
            'target': '(target)[ ]?=[ ]?[\"]?[a-zA-Z0-9. ()]*[\"]?'
        }

    def load(self, filename):
        with open(filename, 'r') as f:
            self.filename = filename
            self.lines = f.readlines()
        return self

    def parse(self):
        mappings = []
        for line in self.lines:
            if re.search(self.regex['method'], line):
                method = re.search(self.regex['method'], line).group(0).replace(' ', '_')
                self.mappings[method] = mappings
                mappings = []
            elif line.__contains__('@Mapping('):
                target = re.search(self.regex['target'], line).group(0).split('=')[1].strip().strip('"')
                source = re.search(self.regex['source'], line).group(0).split('=')[1].strip().strip('"')
                if args.reverse:
                    mappings.append((target, source))
                else:
                    mappings.append((source, target))
        return self

    def get_filename(self, method):
        return method + '.csv'

    def get_heading_row(self):
        if args.reverse:
            return ','.join([args.target, args.source])
        else:
            return ','.join([args.source, args.target])

    def generate(self):
        if self.mappings is not None:
            print(f'Generated csv for {self.filename}:')
            for method, method_mappings in self.mappings.items():
                with open(self.get_filename(method), 'w') as f:
                    f.write(self.get_heading_row())
                    for m in method_mappings:
                        f.write('\n')
                        f.write(','.join(m))
                print(f'  {method} -> [{self.get_filename(method)}]')
        else:
            print(f'No mappings found. Did you load and parse an input file first?')

if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser(description='Parses a Java MapStruct interface and generates a csv that can be pasted on a Confluence page.')
    parser.add_argument('-f', '--filename', type=str, help='name of mapper interface file', default='./sample/CarMapper.java')
    parser.add_argument('-s', '--source', type=str, help='heading text of source column', default='source')
    parser.add_argument('-t', '--target', type=str, help='heading text of target column', default='target')
    parser.add_argument('-r', '--reverse', action='store_true', help='reverse the column output order')
    args = parser.parse_args()

    m = Mapper()
    m.load(args.filename).parse().generate()
