from flask import abort
from flask import Flask
from flask import request,jsonify
from sudoku import sudoku 

app = Flask(__name__)

def prepare_response(puzzle, solution, status='OK', message=None):
    return {'puzzle':puzzle, 'solution':solution, \
            'status':status, 'message':message}

def solve_sudoku(puzzle):
    puzzle = puzzle.strip()

    if len(puzzle) != 81:
        msg = 'Invalid sudoku. Input must be 81 chars ({0} provided)'.\
                format(len(puzzle))
        return prepare_response(puzzle, None, 'Error', msg) 

    solution = sudoku.solve(puzzle)

    if not solution:
        return prepare_response(puzzle, None, 'error', 'Invalid sudoku provided')

    if solution and sudoku.is_solved(solution) \
                    and sudoku.is_valid_solution(solution):
        return prepare_response(puzzle, sudoku.grid_to_str(solution))
  
    return prepare_response(puzzle, None, 'error', 'Unable to solve this sudoku')
        
@app.route("/", methods=['POST'])
def solve():
    """ 
    Receive a HTTP POST request and unpack the payload (sudoku puzzles)
    based on the header Content-Type. Content-Type can be either 
    'application/x-www-form-urlencoded' (key-value pair in the HTTP form) or
    'application/json'. Key-value pair can only carry one sudoku puzzle whereas
    acceptable JSON format is a list of puzzle(s).
    Return value is always a JSON in the following format: 
    {
        data: [
            {
                'puzzle': <input>,
                'solution': <solution if one is found>,
                'status_code': [ok|error],
                'message': None if sudoku is solved else error message
            }
       ]
    }
    
    Raises HTTP 400 Bad Request if unacceptable Content-Type is provided. 
    """ 
    puzzles = [] 

    if request.content_type is None:
        abort(400, 'Content-Type should be application/x-www-form-urlencoded '\
                    'or application/json')

    if request.content_type == 'application/json':
        try:
            puzzles = request.json['sudoku']
        except KeyError, e:
            abort(400, 'Key sudoku missing in the input json. ' \
                        'Expected format: {"sudoku":[list of 81-char-strings]}') 
        
        if len(puzzles) == 0:
            abort(400, 'Missing list of sudoku puzzles. '\
                        'Expected format: {"sudoku":[list of 81-char-strings]}')

    elif request.content_type  == 'application/x-www-form-urlencoded':
        try:
            puzzles.append(request.form['sudoku'])
        except KeyError, e:
            abort(400, 'sudoku key missing in the input form. '\
                        'Expected format: sudoku=<81-char-string>')
    else:
        abort(400, 'Content-Type should be application/x-www-form-urlencoded '\
                    'or application/json')
    
    results = [solve_sudoku(p) for p in puzzles]
    return jsonify({'data':results})

