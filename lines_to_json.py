import json
import os.path
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'ERROR: Missing file name as input'
        print 'Usage: python line_to_json.py <file_name>'
        sys.exit()

    if not os.path.isfile(sys.argv[1]):
        print 'Invalid file name/path provided:', sys.argv[1]
        sys.exit() 

    lines = None
    with open(sys.argv[1], 'rb') as read_handler:
        lines = read_handler.readlines()
   
    data = []
    for ndx, line in enumerate(lines):
        line = line.strip()
        if line.startswith('#'):
            continue

        if len(line) != 81:
            print 'Invalid sudoku input at line ', ndx+1
            sys.exit() 

        data.append(line)

    print json.dumps({'sudoku':data})

