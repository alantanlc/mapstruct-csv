import re
import argparse

class Mapper:

    def __init__(self):
        self.mappings = {}
        self.lines = []
        self.filename = None
        self.regex = {
            'method': '[a-zA-Z0-9_]*\([a-zA-Z0-9 ,]*\);',
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
                method = re.search(self.regex['method'], line).group(0).replace(' ', '_'
                )
                self.mappings[method] = mappings
                mappings = []
            elif line.__contains__('@Mapping('):
                source = re.search(self.regex['source'], line).group(0).split('=')[1].strip().strip('"')
                target = re.search(self.regex['target'], line).group(0).split('=')[1].strip().strip('"')
                mappings.append((source, target))
        return self

    def get_filename(self, method):
        return method + '.csv'

    def generate(self):
        if self.mappings is not None:
            print(f'Generated csv for {self.filename}:')
            for method, method_mappings in self.mappings.items():
                with open(self.get_filename(method), 'w') as f:
                    f.write('source,target\n')
                    for m in method_mappings:
                        f.write(','.join(m))
                        f.write('\n')
                    f.write('\n')
                print(f'  {method} -> [{self.get_filename(method)}]')
        else:
            print(f'No mappings found')

if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser(description='Parses a Java MapStruct interface and generates a csv that can be pasted on a Confluence page.')
    parser.add_argument('-f', '--filename', type=str, help='name of mapper interface file', default='./sample/CarMapper.java')
    args = parser.parse_args()

    m = Mapper()  
    m.load(args.filename).parse().generate()
