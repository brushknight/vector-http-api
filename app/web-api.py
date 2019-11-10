from flask import Flask
from flask import request
import anki_vector
import json
from anki_vector import audio

app = Flask(__name__)


# get account balance and last update
@app.route('/api/vector/say')
def say_text():
    text = request.args.get('text')

    if not text:
        return "text required"

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text(text)

    return "executed"

# get account balance and last update
@app.route('/api/vector/volume/<level>')
def set_volume(level):
    if int(level) < 0 or int(level) > 4:
        return "level should be from 0 to 4"

    levels = {
        0: audio.RobotVolumeLevel.LOW,
        1: audio.RobotVolumeLevel.MEDIUM_LOW,
        2: audio.RobotVolumeLevel.MEDIUM,
        3: audio.RobotVolumeLevel.MEDIUM_HIGH,
        4: audio.RobotVolumeLevel.HIGH,
    }

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.audio.set_master_volume(levels[int(level)])

    return "executed"

# get account balance and last update
@app.route('/api/vector/battery')
def get_battery_state():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        print("Connecting to a cube...")
        robot.world.connect_cube()
        battery_state = robot.get_battery_state()
        if battery_state:
            response = {}

            response['robot'] = {
                'volts': battery_state.battery_volts,
                'level': battery_state.battery_level,
                'is_charging': battery_state.is_charging,
                'is_on_charger_platform': battery_state.is_on_charger_platform,
                'suggested_charger_sec': battery_state.suggested_charger_sec,
            }
            response['cube'] = {
                'volts': battery_state.cube_battery.battery_volts,
                'level': battery_state.cube_battery.level,
                'time_since_last_reading_sec': battery_state.cube_battery.time_since_last_reading_sec,
                'factory_id': battery_state.cube_battery.factory_id,
            }

    return str(json.dumps(response))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
