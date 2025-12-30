import time
from pathlib import Path
from behave import given, when, then
from src.core.driver import MobileDriver
from src.core.recorder import ScreenRecorder
from src.utils.time_utils import get_file_safe_timestamp

@given('the iOS device is connected and ready')
def step_impl(context):
    context.driver = MobileDriver.get_driver()
    context.recorder = ScreenRecorder(context.driver)

@when('I start the screen recording')
def step_impl(context):
    context.recorder.start_recording()

@when('I wait for "{seconds}" seconds')
def step_impl(context, seconds):
    time.sleep(int(seconds))

@then('I stop the recording and save it to "{output_dir_name}"')
def step_impl(context, output_dir_name):
    timestamp = get_file_safe_timestamp()
    context.output_dir = Path(output_dir_name)
    context.output_path = context.output_dir / f"bdd_recording_{timestamp}.mp4"
    context.saved_path = context.recorder.stop_recording(context.output_path)
    MobileDriver.quit_driver()

@then('the recorded video file should exist')
def step_impl(context):
    assert context.saved_path.exists(), "BDD Video file was not created"
    assert context.saved_path.stat().st_size > 0, "BDD Video file is empty"
