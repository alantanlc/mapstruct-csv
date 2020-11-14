import re
import argparse

class Mapper:

    def __init__(self):
        self.mappings = {}
        self.lines = []
        self.filename = None

    def load(self, filename):
        with open(filename, 'r') as f:
            self.filename = filename
            self.lines = f.readlines()
        return self

    def parse(self):
        mappings = []
        for line in self.lines:
            if re.search(r'[a-zA-Z0-9_]*\([a-zA-Z0-9 ]*\);', line):
                method = re.search(r'[a-zA-Z0-9_]*\([a-zA-Z0-9 ]*\)', line).group(0).replace(' ', '_'
                )
                self.mappings[method] = mappings
                mappings = []
            elif line.__contains__('@Mapping('):
                m = re.findall(r'\"[a-zA-Z0-9]*\"', line)
                mappings.append((m[0].strip('"'), m[1].strip('"')))
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
