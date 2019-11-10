import anki_vector
from anki_vector import audio

def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text("It's time to go home")
        robot.behavior.drive_on_charger()
        robot.audio.set_master_volume(audio.RobotVolumeLevel.LOW)

if __name__ == "__main__":
    main()
