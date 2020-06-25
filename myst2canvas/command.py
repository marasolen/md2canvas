from os import path
import click
from configparser import ConfigParser
import myst2canvas.myst2canvas as m2c

NOT_SET = "NOT_SET"

@click.command()
@click.argument("notebook_file", type=str, nargs=1)
@click.option("-t", "--token", type=str, default=None)
@click.option("-f", "--token-file", type=str, default=None)
@click.option("-c", "--course-id", type=str, default=None)
@click.option("-q", "--quiz-id", type=str, default=None)
@click.option("-s", "--save-settings", "save_settings", flag_value=True,
              default=False)
def myst2canvas(notebook_file, token, token_file, course_id, quiz_id,
                save_settings):
    """
    Parse file into quiz and upload to Canvas.
    """
    # Check argument validity
    if not notebook_file or not path.exists(notebook_file):
        print("Invalid notebook file.")
        return

    if token and token_file:
        print("Only one of token or token file can be used.")
        return

    if token_file and not path.exists(token_file):
        print("Invalid token file.")
        return

    # Get/Set configuration
    if token_file:
        with open(token_file, mode="r") as tf:
            token = tf.read()

    config_file = path.join(path.dirname(path.realpath(__file__)), "config.ini")

    config = ConfigParser()
    config.read(config_file)

    if save_settings:
        if token:
            config.set("settings", "token", token)
        if course_id:
            config.set("settings", "course_id", course_id)
        if quiz_id:
            config.set("settings", "quiz_id", quiz_id)

        with open(config_file, "w") as cf:
            config.write(cf)

    if not token:
        token = config.get("settings", "token")
        if token == NOT_SET:
            print("No token given or in config file.")
            return
    if not course_id:
        course_id = config.get("settings", "course_id")
        if course_id == NOT_SET:
            print("No course ID given or in config file.")
            return
    if not quiz_id:
        quiz_id = config.get("settings", "quiz_id")
        if quiz_id == NOT_SET:
            print("No quiz ID given or in config file.")
            return

    print("Running myst2canvas with following settings:")
    print("  Token = ****" + token[-4:])
    print("  Course ID = " + course_id)
    print("  Quiz ID = " + quiz_id)

    quiz = m2c.parse(notebook_file)
    res = m2c.upload(quiz, token, course_id, quiz_id)
