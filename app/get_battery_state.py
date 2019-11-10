import anki_vector

with anki_vector.Robot() as robot:
    print("Connecting to a cube...")
    robot.world.connect_cube()

    battery_state = robot.get_battery_state()
    if battery_state:
        print("Robot battery voltage: {0}".format(battery_state.battery_volts))
        print("Robot battery Level: {0}".format(battery_state.battery_level))
        print("Robot battery is charging: {0}".format(battery_state.is_charging))
        print("Robot is on charger platform: {0}".format(battery_state.is_on_charger_platform))
        print("Robot suggested charger time: {0}".format(battery_state.suggested_charger_sec))
        print("Cube battery level: {0}".format(battery_state.cube_battery.level))
        print("Cube battery voltage: {0}".format(battery_state.cube_battery.battery_volts))
        print("Cube battery seconds since last reading: {0}".format(battery_state.cube_battery.time_since_last_reading_sec))
        print("Cube battery factory id: {0}".format(battery_state.cube_battery.factory_id))