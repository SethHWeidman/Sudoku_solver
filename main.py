from flask import Flask, render_template, request
app = Flask(__name__)

def try_read_int(cell):
    try:
        value = int(request.form[cell])
        return value
    except:
        message = "Please pass in only integer values between 0 and 9."
        render_template("index.html", message=message) # Change this to use flashed messages.

assignments = []
ROWS = 'ABCDEFGHI'
COLS = '123456789'
def cross(A, B):
    '''Combinations of concatenations of all the strings in a list of strings.'''
    return [s+t for s in A for t in B]
boxes = cross(ROWS, COLS)


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
