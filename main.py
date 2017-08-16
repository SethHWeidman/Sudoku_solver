from flask import Flask, render_template, request
from python.sudoku import get_boxes
app = Flask(__name__)

def try_read_int(cell):
    try:
        value = int(request.form[cell])
        return value
    except:
        message = "Please pass in only integer values between 0 and 9."
        render_template("index.html", message=message) # Change this to use flashed messages.

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
        
    print(cell_data)

if __name__ == '__main__':
    app.run(debug=True)
