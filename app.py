from flask import abort
from flask import Flask
from flask import request,jsonify
from sudoku import sudoku 

app = Flask(__name__)

def prepare_response(puzzle, solution, status = 'OK', message=None):
    return {'puzzle': puzzle, 'solution': solution, \
            'status':status, 'message':message}

@app.route("/", methods=['POST'])
def solve():
	result = [] 
        puzzle = [] 

        if request.content_type is None:
            abort(400, 'Content-Type should be application/x-www-form-urlencoded '\
                        'or application/json')

        if request.content_type == 'application/json':
            try:
                puzzle = request.json['sudoku']
            except KeyError, e:
                abort(400, 'Key sudoku missing in the input json. ' \
                            'Expected format: {"sudoku":[list of 81-char-strings]}') 
            
            if len(puzzle) == 0:
                abort(400, 'Missing list of sudoku puzzles. '\
                            'Expected format: {"sudoku":[list of 81-char-strings]}')

        elif request.content_type  == 'application/x-www-form-urlencoded':
            try:
                puzzle.append(request.form['sudoku'])
            except KeyError, e:
                abort(400, 'sudoku key missing in the input form. '\
                            'Expected format: sudoku=<81-char-string>')
        else:
            abort(400, 'Content-Type should be application/x-www-form-urlencoded '\
                        'or application/json')

        for i in puzzle:
            i = i.strip()

            if len(i) != 81:
                result.append(prepare_response(i, None, 'Error', \
                                'Invalid sudoku. Input must be 81 chars '\
                                '({0} provided)'.format(len(i))))
                continue

            solution = sudoku.solve(i)

            if not solution:
                result.append(prepare_response(i, None, 'error', \
                                                'Invalid sudoku provided'))
                
            elif solution and sudoku.is_solved(solution) \
                            and sudoku.is_valid_solution(solution):
                result.append(prepare_response(i,sudoku.grid_to_str(solution)))
            else:
                result.append(prepare_response(i,None, 'error', \
                                                'Unable to solve this sudoku'))

        return jsonify({'data':result})

