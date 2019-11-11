from flask import Flask
from flask import request
import anki_vector
import json
from anki_vector import audio

app = Flask(__name__)


@app.route('/api/say')
def say_text():
    text = request.args.get('text')

    if not text:
        return "text required"

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text(text)

    return "executed"


@app.route('/api/volume/<level>')
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

    lavels_labels = {
        0: "low (0)",
        1: "medium low (1)",
        2: "medium (2)",
        3: "medium high (3)",
        4: "high (4)",
    }

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.audio.set_master_volume(levels[int(level)])

    return "Volume set to " + lavels_labels[int(level)]


@app.route('/api/battery')
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


@app.route('/api/behavior/drive_on_charger')
def behavior_drive_on_charger():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.drive_on_charger()

    return "executed"


@app.route('/api/behavior/drive_off_charger')
def behavior_drive_off_charger():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.drive_off_charger()

    return "executed"


@app.route('/api/animation/list')
def animation_list():
    args = anki_vector.util.parse_command_args()
    with anki_vector.AsyncRobot(args.serial) as robot:
        anim_request = robot.anim.load_animation_list()
        anim_request.result()
        anim_names = robot.anim.anim_list
        return str(json.dumps(anim_names))


#@TODO should be post
@app.route('/api/animation/<animation_id>')
def animation_play(animation_id):
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.anim.play_animation(animation_id)
        return "executed"



@app.route('/api/animation-trigger/list')
def animation_trigger_list():
    args = anki_vector.util.parse_command_args()
    with anki_vector.AsyncRobot(args.serial) as robot:
        anim_trigger_request = robot.anim.load_animation_trigger_list()
        anim_trigger_request.result()
        anim_trigger_names = robot.anim.anim_trigger_list
        return str(json.dumps(anim_trigger_names))


#@TODO should be post
@app.route('/api/animation-trigger/<animation_id>')
def animation_trigger_play(animation_id):
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.anim.play_animation_trigger(animation_id)
        return "executed"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
