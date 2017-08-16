from flask import Flask, render_template, request
from python.sudoku import get_boxes
from python.sudoku import solve_values
app = Flask(__name__)

def try_read_int(cell):
    try:
        acceptable_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        value = int(request.form[cell])
        if value in acceptable_values:
            return value
        else:
            return render_template("index.html", message=message) # Change this to use flashed messages.
    except:
        message = "Please pass in only integer values between 0 and 9."
        return render_template("index.html", message=message) # Change this to use flashed messages.

'''
Sudoku setup
'''

ROWS = 'ABCDEFGHI'
COLS = '123456789'
boxes = get_boxes(ROWS, COLS)

ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
UNIT_LIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/solve_sudoku/', methods=['GET', 'POST'])
def solve_sudoku():
    cell_data = {}
    for box in boxes:
        cell_data[box] = try_read_int(box)
    final_values = solve_values(cell_data)
    print(final_values)
    return render_template("solved_sudoku.html", sudoku=final_values)





if __name__ == '__main__':
    app.run(debug=True)
