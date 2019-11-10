from flask import Flask
from anki_vector import audio
from anki_vector import behavior
import anki_vector

app = Flask(__name__)

# get account balance and last update
@app.route('/api/vector/hello')
def hello():

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("Hello, master.")

    return "executed"

# get account balance and last update
@app.route('/api/vector/say-door-opened')
def say_door_opened():

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("Front door has been opened")

    return "executed"



# get account balance and last update
@app.route('/api/vector/say-door-closed')
def say_door_closed():

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("Front door has been closed")

    return "executed"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')