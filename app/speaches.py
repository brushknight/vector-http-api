import anki_vector
import time
from anki_vector import audio
from anki_vector import behavior
def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        print("Set eyes to evil")
        robot.behavior.set_head_angle(angle=behavior.MIN_HEAD_ANGLE,duration=0)
        robot.behavior.set_eye_color(hue=1, saturation=1)
        time.sleep(1)
        robot.behavior.set_head_angle(angle=behavior.MAX_HEAD_ANGLE,duration=0)
        robot.audio.set_master_volume(audio.RobotVolumeLevel.LOW)
        robot.behavior.set_eye_color(hue=0.42, saturation=1)

if __name__ == "__main__":
    main()
