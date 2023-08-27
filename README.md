# IoTDeviceControl

IoTDeviceControl is a simple Python script that controls the speed of my fan (might get around to doing other IoT experiments with it) based on the temperature of the house and AC using the Google Assistant SDK, ensuring that my fan is never on when the AC is on. Entirely impractical but surprisingly it works fairly well for what I'm doing.

## Usage

To use this project, you can follow these steps:

1. Clone this repository:

   `git clone https://github.com/your-username/IoTDeviceControl.git`

4. Install the required dependencies:

   `pip install -r requirements.txt`

5. Set up a Google Actions project

6. Place your `Project ID` of the actions project in the `project_id` variable

7. Register your computer as a device of any type to connect it to your Google Home using: https://console.actions.google.com/u/0/project/{project-id}/deviceregistration

8. Place your `Model Id` of the device (yes the capitalization is inconsistent) in the `model_id` variable

9. Generate the credentials necessary for the project ([documentation](https://developers.google.com/assistant/sdk/guides/service/python/embed/install-sample#generate_credentials))

10. Run the project:

    `python main.py`

If someone actually decides to try to get this working for some reason, and I inevitably didn't explain how to do something you can reference the [documentation](https://developers.google.com/assistant/sdk/guides/service/python#embed) I followed

## Contributing

This isn't a project I'm anticipating anyone to contribute to. I just felt like posting it because I like making small random scripts and in the off case my ~~extremely inefficient~~ code can help someone.