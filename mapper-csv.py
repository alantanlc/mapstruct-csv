import re
import argparse
import yaml
import os

class Mapper:

    def __init__(self):
        self.filename = None
        self.lines = []
        self.mappings = {}
        self.inherits = {}
        self.regex = {
            'method': r'[a-zA-Z0-9]+\([a-zA-Z0-9 ,.]*\);',
            'source': r'(source|constant|expression)[ ]*=[ ]*[\"]?[a-zA-Z0-9._ ()]*[\"]?',
            'target': r'(target)[ ]*=[ ]*\"[a-zA-Z0-9]*\"',
            'name': r'(name)[ ]*=[ ]*\"[a-zA-Z0-9]*\"',
            'camelCaseWord': r'^[a-z0-9]+|[A-Z][a-z0-9]+',
        }

    def load(self, filename):
        """Store texts from filename in self.lines as a list of lines"""
        with open(filename, 'r') as f:
            self.filename = filename
            self.lines = f.readlines()
        return self

    def parse(self):
        """Parse self.lines to self.mappings.
        Use self.load(self, filename) to load text from file into self.lines first.
        If successful, self.mappings will contain a dictionary of 
        mapping method name mapped to a list of tuples of source and target.
        """
        mappings = []
        inherits = []
        for line in self.lines:
            if re.search(self.regex['method'], line):
                method = re.search(self.regex['method'], line).group(0).replace(' ', '_')
                self.mappings[method] = mappings
                self.inherits[method] = inherits
                mappings = []
                inherits = []
            elif line.__contains__('@InheritConfiguration('):
                name = re.search(self.regex['name'], line).group(0).split('=')[1].strip().strip('"')
                inherits.append(name)
            elif line.__contains__('@Mapping('):
                source = re.search(self.regex['source'], line).group(0).split('=')[1].strip().strip('"')
                target = re.search(self.regex['target'], line).group(0).split('=')[1].strip().strip('"')
                if args.join:
                    s = line.split('//')
                    if len(s) > 1:
                        source += s[1].strip()
                if args.database:
                    target = self.get_db_column_name(target)
                if args.reverse:
                    mappings.append((target, source))
                else:
                    mappings.append((source, target))
        return self

    def get_db_column_name(self, variable):
        """Convert camelcase or pascalcase names to database column names.
        Split camelcase or pascalcase names into words by uppercase letters, 
        capitalize words and then join words using underscore (_).
        """
        camelCaseWords = re.findall(self.regex['camelCaseWord'], variable)
        camelCaseWords = [str.upper(x) for x in camelCaseWords]
        return '_'.join(camelCaseWords)

    def get_filename(self, method):
        """Return the output mapping method filename with file extension appended."""
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        return args.output + '/' + method + '.csv'

    def get_heading_row(self):
        """Return the heading row csv."""
        result = []
        if args.reverse:
            result.append(args.target)
            result.append(args.source)
        else:
            result.append(args.source)
            result.append(args.target)
        if args.comment:
            result.append(args.comment)
        return ','.join(result)

    def get_full_method_by_name(self, name):
        for m in self.mappings.keys():
            if m.startswith(name + '('):
                return m

    def write_mapping_to_file(self, mapping, f):
        f.write('\n')
        if args.comment:
            f.write(','.join(mapping) + ',')
        else:
            f.write(','.join(mapping))

    def generate(self):
        """Generate a CSV for each mapping method from self.mappings.
        Use self.parse() to parse self.lines into self.mappings first.
        Name of each CSV is the mapping method definition itself.
        """
        if self.mappings is not None:
            print(f'Generated csv for {self.filename}:')
            for method, method_mappings in self.mappings.items():
                with open(self.get_filename(method), 'w') as f:
                    f.write(self.get_heading_row())
                    for mapping in method_mappings:
                        self.write_mapping_to_file(mapping, f)
                    if args.inherit:
                        queue = self.inherits[method].copy()
                        visited = set()
                        while len(queue) > 0:
                            n = queue.pop(0)
                            visited.add(n)
                            n_method = self.get_full_method_by_name(n)
                            for mapping in self.mappings[n_method]:
                                self.write_mapping_to_file(mapping, f)
                            for inherit in self.inherits[n_method]:
                                if inherit not in visited:
                                    queue.append(inherit)
                print(f'  {method} -> [{self.get_filename(method)}]')
        else:
            print(f'No mappings found. Did you load and parse an input file first?')

if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser(description='Parses a Java MapStruct interface file and generates CSV that can be pasted on confluence pages')
    parser.add_argument('-y', '--yaml', type=str, default='./config.yaml', help='name of yaml config file')
    parser.add_argument('-f', '--filename', type=str, default='./sample/CarMapper.java', help='name of mapper interface file')
    parser.add_argument('-s', '--source', type=str, default='Source', help='heading text of source column')
    parser.add_argument('-t', '--target', type=str, default='Target', help='heading text of target column')
    parser.add_argument('-d', '--database', action='store_true', help='format target names as database column names')
    parser.add_argument('-r', '--reverse', action='store_true', help='reverse the column output order')
    parser.add_argument('-c', '--comment', nargs='?', const='Comment', help='include a comment column at the end')
    parser.add_argument('-i', '--inherit', action='store_true', help='include @InheritConfiguration mappings')
    parser.add_argument('-j', '--join', action='store_true', help='join source with additional mapping defined as a comment on the same line')
    parser.add_argument('-o', '--output', type=str, default='output', help='name of output directory')
    args = parser.parse_args()

    if args.yaml:
        with open(args.yaml) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for k, v in data.items():
                args.__setattr__(k, v)

    m = Mapper()
    m.load(args.filename).parse().generate()
