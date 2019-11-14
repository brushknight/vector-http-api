import sys
import time
from flask import Response

from flask import Flask
from flask import request
import anki_vector
import json
from anki_vector import audio

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

app = Flask(__name__)

args = anki_vector.util.parse_command_args()


@app.route('/api/say')
def say_text():
    text = request.args.get('text')

    if not text:
        return "text required"

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

    with anki_vector.Robot(args.serial) as robot:
        robot.audio.set_master_volume(levels[int(level)])

    return "Volume set to " + lavels_labels[int(level)]


@app.route('/api/battery')
def get_battery_state():
    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:
        print("Connecting to a cube...")
        # robot.world.connect_cube()
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
            # response['cube'] = {
            #     'volts': battery_state.cube_battery.battery_volts,
            #     'level': battery_state.cube_battery.level,
            #     'time_since_last_reading_sec': battery_state.cube_battery.time_since_last_reading_sec,
            #     'factory_id': battery_state.cube_battery.factory_id,
            # }

    return Response((json.dumps(response)), mimetype='application/json')


@app.route('/api/behavior/drive_on_charger')
def behavior_drive_on_charger():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.drive_on_charger()

    return "executed"


@app.route('/api/behavior/drive_off_charger')
def behavior_drive_off_charger():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.drive_off_charger()
    return "executed"


@app.route('/api/animation/list')
def animation_list():
    with anki_vector.AsyncRobot(args.serial, behavior_control_level=None) as robot:
        anim_request = robot.anim.load_animation_list()
        anim_request.result()
        anim_names = robot.anim.anim_list
    return str(json.dumps(anim_names))


# @TODO should be post
@app.route('/api/animation/<animation_id>')
def animation_play(animation_id):
    with anki_vector.Robot(args.serial) as robot:
        robot.anim.play_animation(animation_id)
    return "executed"


@app.route('/api/animation-trigger/list')
def animation_trigger_list():
    with anki_vector.AsyncRobot(args.serial, behavior_control_level=None) as robot:
        anim_trigger_request = robot.anim.load_animation_trigger_list()
        anim_trigger_request.result()
        anim_trigger_names = robot.anim.anim_trigger_list
    return Response((json.dumps(anim_trigger_names)), mimetype='application/json')


# @TODO should be post
@app.route('/api/animation-trigger/<animation_id>')
def animation_trigger_play(animation_id):
    with anki_vector.Robot(args.serial) as robot:
        robot.anim.play_animation_trigger(animation_id)
    return "executed"


@app.route('/api/status/')
def get_status():
    current_states = []

    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:

        if robot.status.is_on_charger: current_states.append("is_on_charger")
        if robot.status.are_motors_moving: current_states.append("are_motors_moving")
        if robot.status.are_wheels_moving: current_states.append("are_wheels_moving")
        if robot.status.is_animating: current_states.append("is_animating")
        if robot.status.is_being_held: current_states.append("is_being_held")
        if robot.status.is_button_pressed: current_states.append("is_button_pressed")
        if robot.status.is_carrying_block: current_states.append("is_carrying_block")
        if robot.status.is_charging: current_states.append("is_charging")
        if robot.status.is_cliff_detected: current_states.append("is_cliff_detected")
        if robot.status.is_docking_to_marker: current_states.append("is_docking_to_marker")
        if robot.status.is_falling: current_states.append("is_falling")
        if robot.status.is_head_in_pos: current_states.append("is_head_in_pos")
        if robot.status.is_in_calm_power_mode: current_states.append("is_in_calm_power_mode")
        if robot.status.is_lift_in_pos: current_states.append("is_lift_in_pos")
        if robot.status.is_pathing: current_states.append("is_pathing")
        if robot.status.is_picked_up: current_states.append("is_picked_up")
        if robot.status.is_robot_moving: current_states.append("is_robot_moving")
    return Response((json.dumps(current_states)), mimetype='application/json')


@app.route('/api/fancy/gitlab-build-finished')
def fancy_gitlab_build_success():
    robot = anki_vector.Robot(args.serial)
    robot.connect()

    robot.anim.play_animation_trigger("ReactToTriggerWordOffChargerFrontLeft")
    robot.screen.set_screen_to_color(anki_vector.color.Color(rgb=[50, 119, 168]), duration_sec=6.0)
    robot.behavior.say_text("Gitlab build finished, check your app.")
    robot.disconnect()
    return "executed"


@app.route('/api/fancy/status')
def fancy_status():
    response = {}
    robot = anki_vector.Robot(args.serial, behavior_control_level=None)
    robot.connect()

    if robot.status.is_charging:
        response['status'] = 'charging'
    if robot.status.is_robot_moving and robot.status.are_wheels_moving:
        response['status'] = 'exploring'
    if robot.status.is_on_charger \
            and robot.status.is_head_in_pos \
            and robot.status.is_in_calm_power_mode \
            and robot.status.is_lift_in_pos:
        response['status'] = 'sleeping'
    else:
        response['status'] = 'active'

    robot.disconnect()

    return Response(json.dumps(response), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
