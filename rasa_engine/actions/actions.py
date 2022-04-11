# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.forms import FormValidationAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
logger = logging.getLogger(__name__)
logger.debug("Starting Action server")

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


class ValidateHealthForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_health_form"

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    async def validate_confirm_exercise(self,
                                        value: Text,
                                        dispatcher: CollectingDispatcher,
                                        tracker: Tracker,
                                        domain: Dict[Text, Any]) -> Dict[Text, Any]:
        print("validate confirm_exercise: ", value)
        if isinstance(value, bool):
            return {"confirm_exercise": True}
        else:
            return {"exercise": "None", "confirm_exercise": False}

    async def validate_exercise(self,
                                value: Text,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: Dict[Text, Any]) -> Dict[Text, Any]:
        print("validate exercise: ", value)
        if isinstance(value, str):
            return {"exercise": value}
        return {"exercise": None}

#   - stress
#   - diet
#   - goal
    async def validate_sleep(self, value: Text,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: Dict[Text, Any]) -> Dict[Text, Any]:
        print("validate hours of sleep")
        if self.is_int(value) and int(value) > 0:
            return {"sleep": value}
        else:
            dispatcher.utter_message(response="utter_wrong_sleeping_hours")
            # validation failed, set slot to None
            return {"sleep": None}


class ActionSubmitForm(Action):
    def name(self) -> Text:
        return "action_submit_form"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        confirm_exercise = tracker.get_slot("confirm_exercise")
        exercise = tracker.get_slot("exercise")
        sleep = tracker.get_slot("sleep")
        stress = tracker.get_slot("stress")
        diet = tracker.get_slot("diet")
        goal = tracker.get_slot("goal")

        print("confirm_exercise: ", confirm_exercise)
        print("exercise: ", exercise)
        print("sleep: ", sleep)
        print("stress: ", stress)
        print("diet: ", diet)

        dispatcher.utter_message("Thanks, your answers have been recorded!")
        return []
