
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted
import re 
import numpy
import pandas as pd

data=pd.read_csv(r"ipl_data.csv")

def redirectToSlot(slot, value, dispatcher, tracker, remapping):
    response = {slot: value} # default response

    if (slot == "pnr"):
        
        if len(value) == 6:
            response = {slot: value}
        else:
            dispatcher.utter_message(template="utter_wrong_pnr")
            response = {slot: None}
            
    if (type(remapping) == str):
        response[remapping] = None

    return response

class FlightStatusForm(FormAction):
   

    def name(self):
        return "action_get_flight_status"
    @staticmethod
    def required_slots(tracker):
        return [
            "pnr",]

    def validate_pnr(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""
        value=tracker.get_slot("pnr")

        print("validate_pnr() method  ", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        
        if (requestedSlot['value'] == 'pnr'): # If requested slot was pnr and value also corresponds to the pnr 
            return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
        else: # If value corresponds to the wrong slot
            return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'pnr')
        
            
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        value = str(tracker.get_slot("pnr"))
        if value==None:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            
        flight_status=""
        flight_number=""
        for i,j,k in zip(data["PNR"],data["flight_status"],data["flight_number"]):
            if (i==value):
                flight_status=j
                flight_number=k
        message="Dear Traveller, Your flight "+str(flight_number)+" is "+str(flight_status)
        dispatcher.utter_message(message)
       
        return []


class FlightScheduleForm(FormAction):
   

    def name(self):
        return "action_get_flight_schedule"
  
    @staticmethod
    def required_slots(tracker):
        return [
            "pnr",]

    def validate_pnr(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""
        value=tracker.get_slot("pnr")

        print("validate_phone_number() method  ", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot'):
            if (requestedSlot['value'] == 'pnr'): # If requested slot was pnr and value also corresponds to the pnr 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'pnr')
        else:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        value = str(tracker.get_slot("pnr"))
        if value==None:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            
        departure_time=""
        flight_number=""
        for i,j,k,m in zip(data["PNR"],data["departure_time"],data["arrival_time"],data["flight_number"]):
            if (i==value):
                departure_time=j
                arrival_time=k
                flight_number=m
        
        message="Dear Traveller your flight "+str(flight_number)+" will be departing at "+str(departure_time)+" and will be arriving at the destination at "+str(arrival_time)
        dispatcher.utter_message(message)
        return [] 
        
class FlightGateForm(FormAction):
   

    def name(self):
        return "action_get_gate_number"
    
    @staticmethod
    def required_slots(tracker):
        return [
            "pnr",]

    def validate_pnr(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""
        value=tracker.get_slot("pnr")

        print("validate_phone_number() method  ", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot'):
            if (requestedSlot['value'] == 'pnr'): # If requested slot was pnr and value also corresponds to the pnr 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'pnr')
        else:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        value = str(tracker.get_slot("pnr"))
        if value==None:
            return redirectToSlot('pnr', value, dispatcher, tracker, None)
        gate_number=""
        flight_number=""            
        for i,j,k in zip(data["PNR"],data["flight_number"],data["boarding_gate"]):
            if (i==value):
                flight_number=j
                gate_number=k
        message="Dear Traveller, gate number for your flight "+str(flight_number)+" is "+str(gate_number)
        dispatcher.utter_message(message)
        return []
        
class FlightBaggageForm(FormAction):
   

    def name(self):
        return "action_get_baggage_detail"
  

    @staticmethod
    def required_slots(tracker):
        return [
            "pnr",]

    def validate_pnr(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""
        value=tracker.get_slot("pnr")

        print("validate_phone_number() method  ", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot'):
            if (requestedSlot['value'] == 'pnr'): # If requested slot was pnr and value also corresponds to the pnr 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'pnr')
        else:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        value = str(tracker.get_slot("pnr"))
        if value==None:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            
        baggage_detail="" 
        for i,j in zip(data["PNR"],data["baggage_detail"]):
            if (i==value):
                baggage_detail=j
        message="Dear Traveller your baggage will be arriving at "+str(baggage_detail)
        dispatcher.utter_message(message)
        return []
        
class FlightBoardingStatusForm(FormAction):
   

    def name(self):
        return "action_get_boarding_status"
    
    @staticmethod
    def required_slots(tracker):
        return [
            "pnr",]

    def validate_pnr(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""
        value=tracker.get_slot("pnr")

        print("validate_phone_number() method  ", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot'):
            if (requestedSlot['value'] == 'pnr'): # If requested slot was pnr and value also corresponds to the pnr 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'pnr')
        else:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
            


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        value = str(tracker.get_slot("pnr"))
        if value==None:
            return redirectToSlot('pnr', value, dispatcher, tracker, None) 
        
        boarding_status="" 
        flight_number="" 
        for i,j,k in zip(data["PNR"],data["boarding_status"],data["flight_number"]):
            if (i==value):
                boarding_status=j
                flight_number=k
        message="Dear Traveller the boarding for your flight "+str(flight_number)+ " has "+str(boarding_status)
        dispatcher.utter_message(message)
        return []

class ActionBookFlight(Action):
    def name(self):
        return "action_book_flight"
    def run(self,dispatcher,tracker,domain):
        start=tracker.get_slot("start")
        destination=tracker.get_slot("destination")
  
        output="https://www.makemytrip.com/flights/"+str(start)+"-"+str(destination)+"-fare-calendar.html"
        dispatcher.utter_message(output)
        return []

## action_hi   
class ActionHi(Action):
    def name(self):
        return "action_greet"
    def run(self,dispatcher,tracker,domain):
        msg="Hello! I am Airobot."

        dispatcher.utter_message(text=msg)
        
       
        
        #dispatcher.utter_message(template="utter_ask_what_next")
        return []
        
        
  
class AskHelp(Action):
    def name(self):
        return "action_ask_help"
    def run(self,dispatcher,tracker,domain):
        output="Action help triggered"
        dispatcher.utter_message(output)
        return []
        
