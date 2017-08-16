from flask import Flask, render_template, request
from python.sudoku import get_boxes
from python.sudoku import solve_values
app = Flask(__name__)

def try_read_int(cell, default_value='123456789'):
    acceptable_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    try:
        value = int(request.form[cell])
        if value in acceptable_values:
            return str(value)
        else:
            "Please enter an integer between 0 and 9"
    except:
        return default_value
'''
Sudoku setup
'''

ROWS = 'ABCDEFGHI'
COLS = '123456789'
boxes = get_boxes(ROWS, COLS)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/solve_sudoku_new/', methods=['GET', 'POST'])
def solve_sudoku():
    cell_data = {}
    for box in boxes:
        cell_data[box] = ''
        cell_data[box] = try_read_int(box)
    final_values = solve_values(cell_data)
    return render_template("solved_sudoku.html", sudoku=final_values)


if __name__ == '__main__':
    app.run(debug=True)
