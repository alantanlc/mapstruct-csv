import re
import argparse

class Mapper:

    def __init__(self):
        self.mappings = {}
        self.lines = []
        self.filename = None
        self.regex = {
            'method': r'[a-zA-Z0-9_]*\([a-zA-Z0-9 ,.]*\);',
            'source': r'(source|constant|expression)[ ]?=[ ]?[\"]?[a-zA-Z0-9._ ()]*[\"]?',
            'target': r'(target)[ ]?=[ ]?[\"]?[a-zA-Z0-9. ()]*[\"]?',
            'camelCaseWord': r'^[a-z]+|[A-Z][a-z0-9]+'
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
        for line in self.lines:
            if re.search(self.regex['method'], line):
                method = re.search(self.regex['method'], line).group(0).replace(' ', '_')
                self.mappings[method] = mappings
                mappings = []
            elif line.__contains__('@Mapping('):
                source = re.search(self.regex['source'], line).group(0).split('=')[1].strip().strip('"')
                target = re.search(self.regex['target'], line).group(0).split('=')[1].strip().strip('"')
                
                if args.db:
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
        return method + '.csv'

    def get_heading_row(self):
        """Return the heading row csv in normal or reverse order."""
        if args.reverse:
            return ','.join([args.target, args.source])
        else:
            return ','.join([args.source, args.target])

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
                    for m in method_mappings:
                        f.write('\n')
                        f.write(','.join(m))
                print(f'  {method} -> [{self.get_filename(method)}]')
        else:
            print(f'No mappings found. Did you load and parse an input file first?')

if __name__ == '__main__':
    # argparse
    parser = argparse.ArgumentParser(description='Parses a Java MapStruct interface file and generates CSV that can be pasted on confluence pages')
    parser.add_argument('-f', '--filename', type=str, help='name of mapper interface file', default='./sample/CarMapper.java')
    parser.add_argument('-s', '--source', type=str, help='heading text of source column', default='source')
    parser.add_argument('-t', '--target', type=str, help='heading text of target column', default='target')
    parser.add_argument('-d', '--db', action='store_true', help='format target names as database column names')
    parser.add_argument('-r', '--reverse', action='store_true', help='reverse the column output order')
    args = parser.parse_args()

    m = Mapper()
    m.load(args.filename).parse().generate()
