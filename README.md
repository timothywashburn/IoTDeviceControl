# IoTDeviceControl

IoTDeviceControl is a simple python script that controls the speed of my fan (might get around to doing other IoT experiments with it) based on the temperature of the house and AC, ensuring that my fan is never on when the AC is on. Entirely impractical but surprisingly it works fairly well for what I'm doing

## Usage

To use this project, you can follow these steps:

1. Clone the repository:
   git clone https://github.com/your-username/IoTDeviceControl.git

2. Install the required dependencies:

   `pip install -r requirements.txt`

3. Set up a google actions project

4. Place your `Project ID` of the actions project in the `project_id` variable

5. Register your computer as a device of any type to connect it to your Google Home using: https://console.actions.google.com/u/0/project/{project-id}/deviceregistration

6. Place your `Model Id` of the device (yes the capitalization is inconsistent) in the `model_id` variable

7. Run the project:

   `python main.py`

If someone actually decides to try to get this working for some reason, and I inevitably didn't explain how to do something you can reference the Google documentation I followed [here](https://developers.google.com/assistant/sdk/guides/service/python#embed)

## Configuration

Before running the project, you need to set up your credentials and configuration. Refer to the code comments for details on how to do this.

## Contributing

This isn't a project I'm anticipating anyone contribute to. I just felt like posting it because I like making small random scripts and in the off case my ~~extremely inefficient~~ code can help someone.