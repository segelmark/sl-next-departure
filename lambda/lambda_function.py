# -*- coding: utf-8 -*-

# Handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.

import logging
import ask_sdk_core.utils as ask_utils

import requests
from collections import defaultdict

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_next_departure(stationID, buses_to_monitor, valid_destinatios):
    url = f'https://transport.integration.sl.se/v1/sites/{stationID}/departures'

    response = requests.get(url, headers={"Accept": "application/json", "Content-Type": "application/json"})
    data = response.json()
    
    # Initialize a dictionary to hold departure times for each bus
    departures_by_bus = defaultdict(list)
    
    for departure in data['departures']:
        bus_number = departure['line']['designation']
        display_time = departure['display']
        destination = departure['destination']

        if display_time == "Nu":
            display_time="now"
        elif ":" in display_time:  # Checks if the string is a time format
            display_time=f"at {display_time}"
        else:
            display_time=f"in {display_time}"
        
        # Check if the bus is one we're monitoring and its destination matches our criteria
        if bus_number in buses_to_monitor and any(destination == indicator for indicator in valid_destinatios):
            departures_by_bus[bus_number].append(display_time)
    
    return departures_by_bus

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can ask me when the bus, train or metro leaves. Do you want to give it a try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class DepartureInfoIntentHandler(AbstractRequestHandler):
    """Handler for Departure Info Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DepartureInfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots = handler_input.request_envelope.request.intent.slots
        
        speak_output = ""
        
        # Define the buses to monitor and their relevant destinations
        if 'linenumber' in slots and slots['linenumber'].value:
            buses_to_monitor = [slots['linenumber'].value]
        else:
            buses_to_monitor = ['72', '6', '3', '507']
        valid_destinations = ['Odenplan', 'Södersjukhuset', 'Liljeholmen','Frihamnen','Ropsten']

        
        # Select which bus station you want to
        stationID='3406'
        
        departures_by_bus = get_next_departure(stationID, buses_to_monitor, valid_destinations)
        
        # Iterate over each bus we're monitoring
        for bus in buses_to_monitor:
            if bus in departures_by_bus:
                # Get the first two departure times if they exist
                next_times = departures_by_bus[bus][:2]
                if len(next_times) == 1:
                    speak_output+="The next bus "+bus+" leaves "+next_times[0]+". <break time='250ms'/>"
                else:
                    speak_output+="The next bus "+bus+" leaves "+next_times[0]+" <break time='50ms'/> and the one after "+next_times[1]+". <break time='250ms'/>"
            else:
                # No departures found for this bus
                speak_output+="There is no bus "+bus+" in the near future. <break time='250ms'/>"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask me when the bus leaves"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can ask when does the bus leaves"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(DepartureInfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()