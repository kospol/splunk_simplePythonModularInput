import sys
import requests
import logging

from splunklib.modularinput import *


def do_work(input_name, ew, symbol):
    EventWriter.log(ew, EventWriter.INFO, "Started getting price for symbol %s" % symbol)
    r = requests.get('http://finance.yahoo.com/webservice/v1/symbols/%s/quote?format=json' % symbol)
    resources = r.json().get('list', {}).get('resources', [])

    for i in resources:
        event = Event()
        event.stanza = input_name
        data = "symbol=%s price=%s" % (i['resource']['fields']['symbol'], i['resource']['fields']['price'])
        event.data = data
        ew.write_event(event)


class MyScript(Script):

    def get_scheme(self):
        scheme = Scheme("Stock symbols Input")
        scheme.description = "Send the price of a stock symbol to Splunk"
        scheme.use_external_validation = True
        scheme.use_single_instance = True

        symbol_argument = Argument("symbol")
        symbol_argument.data_type = Argument.data_type_string
        symbol_argument.description = "The symbol of the stock. Example: SPLK"
        symbol_argument.required_on_create = True
        scheme.add_argument(symbol_argument)

        return scheme

    def validate_input(self, validation_definition):
        logging.error("lala: im in")
        symbol = str(validation_definition.parameters["symbol"])
        logging.error("lala: symbol %s" % symbol)
        if len(symbol) < 1:
            raise ValueError("The symbol has to be at least 1 character long!")

        r = requests.get('http://finance.yahoo.com/webservice/v1/symbols/%s/quote?format=json' % symbol)
        count = r.json().get('list', {}).get('meta', {}).get('count', 0)
        if count == 0:
            raise ValueError("The symbol %s doesn't exist" % symbol)

    def stream_events(self, inputs, ew):
        for input_name, input_item in inputs.inputs.iteritems():
            symbol = str(input_item["symbol"])
            do_work(input_name, ew, symbol)


if __name__ == "__main__":
    MyScript().run(sys.argv)