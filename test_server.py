import json
import unittest
from collections import namedtuple
from app import app

Sudoku = namedtuple('Sudoku', ['puzzle', 'solution'])

class SudokuAPITesT(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.sudoku = Sudoku(
                '.1...8...3.472169...6....1....9.253..421.378..358.6....9....1...213874.9...5...2.',
                '719638254354721698286495317678942531942153786135876942893264175521387469467519823')
        self.client = app.test_client()

    
    def assert_response(self, response, data_length, puzzles, solutions, \
                        status, messages):
        ''' Given a response, unpack the payload and test that client receives
            the right format and contents. Sudoku API will return a response
            of the format:

            {
                data: [
                    {
                        'puzzle': <input>,
                        'solution': <solution if one is found>,
                        'status_code': [ok|error], 
                        'message': None if sudoku is solved else error message 
                ]
            }
        '''
        response_data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data)
        self.assertTrue('data' in response_data)
        self.assertTrue(len(response_data['data']) == data_length)

        for ndx, data in enumerate(response_data['data']):
            self.assertEqual(puzzles[ndx], data['puzzle'])
            self.assertEqual(solutions[ndx], data['solution'])
            self.assertEqual(status[ndx].lower(), data['status'].lower())
            if messages[ndx] is None:
                self.assertEqual(messages[ndx], data['message'])
            else:
                self.assertIn(messages[ndx], data['message'])

   
    def test_missing_key_in_form(self):
        # Send an invalid key 'sudoku1' instead of 'sudoku'
        response = self.client.post('/', data={'sudoku1':self.sudoku.puzzle})
        self.assertEqual(response.status_code, 400)
        self.assertIn('sudoku', response.data)

    def test_form_post(self):
        response = self.client.post('/', data={'sudoku':self.sudoku.puzzle})
        self.assert_response(response, 1, [self.sudoku.puzzle], 
                            [self.sudoku.solution], ['ok'], [None])
    
    def test_invalid_len_in_form(self):
        # Append an extra char to our 81-chars input
        invalid_puzzle = self.sudoku.puzzle + '.'
        response = self.client.post('/', data={'sudoku':invalid_puzzle})
        self.assert_response(response, 1, [invalid_puzzle], [None], ['error'], \
                            ['Invalid'])

    def test_empty_puzzle_in_form(self):
        response = self.client.post('/',data={'sudoku':''})
        self.assert_response(response,1 , [''], [None], ['error'], ['Invalid'])

    def test_empty_post(self):
       # No form data provided
       response = self.client.post('/')
       self.assertEqual(response.status_code, 400)

    def test_invalid_content_type(self):
       response = self.client.post('/', content_type='blah')
       self.assertEqual(response.status_code, 400)

    def test_json_post(self):
        json_data = json.dumps({'sudoku':[self.sudoku.puzzle]})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assert_response(response, 1, [self.sudoku.puzzle], [self.sudoku.solution], 
                            ['ok'], [None])

    def test_missing_key_in_json(self):
        json_data = json.dumps({'sudoku1':[self.sudoku.puzzle]})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('sudoku', response.data)

    def test_invalid_len_in_json(self):
        invalid_puzzle = self.sudoku.puzzle + '.'
        json_data = json.dumps({'sudoku':[invalid_puzzle]})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assert_response(response, 1, [invalid_puzzle], [None], ['error'], \
                            ['Invalid'])

    def test_missing_list_in_json(self):
        json_data = json.dumps({'sudoku':''})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_empty_puzzle_in_json(self):
        json_data = json.dumps({'sudoku':['']})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assert_response(response, 1, [''], [None], ['error'], \
                            ['Invalid'])

    def test_multiple_puzzles_in_json(self):
        json_data = json.dumps({'sudoku':[self.sudoku.puzzle, self.sudoku.puzzle]})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assert_response(response, 2, [self.sudoku.puzzle, self.sudoku.puzzle], \
                            [self.sudoku.solution, self.sudoku.solution], \
                            ['ok', 'ok'], [None, None])
        
    def test_multiple_invalid_puzzles_in_json(self):
        invalid_puzzle = self.sudoku.puzzle + '.'
        json_data = json.dumps({'sudoku':[self.sudoku.puzzle, invalid_puzzle]})
        response = self.client.post('/', data=json_data, content_type='application/json')
        self.assert_response(response, 2, [self.sudoku.puzzle, invalid_puzzle], \
                            [self.sudoku.solution, None], \
                            ['ok', 'error'], [None, 'Invalid'])
       

if __name__ == '__main__':
    unittest.main()
