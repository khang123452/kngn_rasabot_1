# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Example: Simulated robot control interface
class RobotController:
    @staticmethod
    def move(direction: str, distance: float, speed: str) -> bool:
        # Simulate sending a move command to the robot
        print(f"Robot moving {direction} for {distance} meters at {speed} speed.")
        return True  # Simulate success

    @staticmethod
    def stop() -> bool:
        # Simulate stopping the robot
        print("Robot stopped.")
        return True

    @staticmethod
    def goto(location: str) -> bool:
        # Simulate navigating to a location
        print(f"Robot going to {location}.")
        return True

    @staticmethod
    def pickup(object_to_pickup: str) -> bool:
        # Simulate picking up an object
        print(f"Robot picking up {object_to_pickup}.")
        return True

    @staticmethod
    def place(object_to_place: str, location: str) -> bool:
        # Simulate placing an object
        print(f"Robot placing {object_to_place} at {location}.")
        return True

    @staticmethod
    def get_battery_level() -> int:
        # Simulate checking the battery level
        return 75  # Example dummy value

    @staticmethod
    def get_current_location() -> str:
        # Simulate getting current location
        return "living room"

    @staticmethod
    def get_current_status() -> str:
        # Simulate checking robot's current task
        return "moving to the kitchen"


# Action to move the robot
class ActionMove(Action):
    def name(self) -> Text:
        return "action_move"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract slots
        direction = tracker.get_slot("direction")
        distance = tracker.get_slot("distance")
        speed = tracker.get_slot("speed")

        # Validate slots
        if not direction or not distance or not speed:
            dispatcher.utter_message(text="I need direction, distance, and speed to move.")
            return []

        # Send command to the robot
        if RobotController.move(direction, float(distance), speed):
            dispatcher.utter_message(text=f"Moving {direction} for {distance} meters at {speed} speed.")
        else:
            dispatcher.utter_message(text="Failed to move the robot.")

        return []


# Action to navigate to a location
class ActionGoto(Action):
    def name(self) -> Text:
        return "action_goto"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")

        if not location:
            dispatcher.utter_message(text="I need to know where to go.")
            return []

        if RobotController.goto(location):
            dispatcher.utter_message(text=f"Heading to {location}.")
        else:
            dispatcher.utter_message(text="Failed to navigate to the location.")

        return []


# Action to stop the robot
class ActionStop(Action):
    def name(self) -> Text:
        return "action_stop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if RobotController.stop():
            dispatcher.utter_message(text="Stopping now.")
        else:
            dispatcher.utter_message(text="Failed to stop the robot.")

        return []


# Action to pick up an object
class ActionPickup(Action):
    def name(self) -> Text:
        return "action_pickup"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        object_to_pickup = tracker.get_slot("object")

        if not object_to_pickup:
            dispatcher.utter_message(text="I need to know what to pick up.")
            return []

        if RobotController.pickup(object_to_pickup):
            dispatcher.utter_message(text=f"Picking up the {object_to_pickup}.")
        else:
            dispatcher.utter_message(text="Failed to pick up the object.")

        return []


# Action to place an object
class ActionPlace(Action):
    def name(self) -> Text:
        return "action_place"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        object_to_place = tracker.get_slot("object")
        location_to_place = tracker.get_slot("location")

        if not object_to_place or not location_to_place:
            dispatcher.utter_message(text="I need to know what and where to place.")
            return []

        if RobotController.place(object_to_place, location_to_place):
            dispatcher.utter_message(text=f"Placing the {object_to_place} at {location_to_place}.")
        else:
            dispatcher.utter_message(text="Failed to place the object.")

        return []


# Action to check the battery status
class ActionBatteryStatus(Action):
    def name(self) -> Text:
        return "action_battery_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        battery_level = RobotController.get_battery_level()
        dispatcher.utter_message(text=f"Battery level is {battery_level}%.")
        return []


# Action to report the current location
class ActionLocationStatus(Action):
    def name(self) -> Text:
        return "action_location_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = RobotController.get_current_location()
        dispatcher.utter_message(text=f"I am currently at {location}.")
        return []


# Action to report the robot's status
class ActionStatusReport(Action):
    def name(self) -> Text:
        return "action_status_report"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        status = RobotController.get_current_status()
        dispatcher.utter_message(text=f"I am currently {status}.")
        return []
