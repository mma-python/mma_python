import willie
import random
import os
from willie import module
import requests
import operator
from willie.formatting import bold, underline

@willie.module.commands('events')
def events(bot, trigger):
	results = build_fancy_dict_from_json(events_decoded)
	bot.say(bold(underline("NEXT TEN UPCOMING EVENTS")))
        for item in results:
                bot.say("%s. %s" % (item, results[item]))
        
@willie.module.commands('event')
def event(bot, trigger):
	build_counter = 1
	output_fight_card = return_card_info(trigger.group(2))
	event_name = output_fight_card.split("-")[0].strip()
	event_card = output_fight_card.split("-")[1]
	output_fight_card_list = event_card.split(",")
	bot.say(bold(event_name) + " " +  "has the following %s fights (A vs. B):" % len(output_fight_card_list))
	for fight in output_fight_card_list:
		bot.say(bold(str(build_counter)) + "." + " " + fight.strip())
		build_counter = build_counter + 1


def return_events_list():
        grab_mma_info = requests.get("http://127.0.0.1:5000/mma/events")
        events_decoded = grab_mma_info.json()
        return events_decoded

def build_fancy_dict_from_json(input_json):
        event_catalog = {}
        build_counter = 1
        for x in input_json["mma_events"]:
                event_number = build_counter
                event_name = str(events_decoded["mma_events"][x]["event_name"])
                event_time = str(events_decoded["mma_events"][x]["event_time"])
                event_location = events_decoded["mma_events"][x]["event_location"]
                event_catalog[events_decoded["mma_events"][x]["event_id"]] = "%s - %s - %s" % (event_name, event_location, event_time)
                #sorted_x = sorted(event_catalog.items(), key=operator.itemgetter(0))
                build_counter = build_counter + 1
        return event_catalog

def main():
        results = build_fancy_dict_from_json(events_decoded)
        for item in results:
                print "%s. %s" % (item, results[item])

events_decoded = return_events_list()

def return_card_info(event_id):
        event = requests.get("http://127.0.0.1:5000/mma/event/%s" % event_id)
        return event.text

