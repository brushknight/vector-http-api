import anki_vector
from anki_vector import audio

def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.audio.set_master_volume(audio.RobotVolumeLevel.HIGH)
        robot.behavior.say_text("Exploring time!")
        robot.behavior.drive_off_charger()

if __name__ == "__main__":
    main()
