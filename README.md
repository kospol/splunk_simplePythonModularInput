# Splunk Python Modular Input example and tutorial
Kostas Polychronis

### What is a modular input
Modular inputs are a very powerful tool that helps the process of putting data into a Splunk instance. It's used when the traditional input data solutions (monitoring files, listening for TCP or UDP data etc) are not viable or when there's need for more sophisticated processing of the data. For more imformation read [this](http://docs.splunk.com/Documentation/Splunk/latest/AdvancedDev/ModInputsIntro).

### What are we going to do in this example
The sole purpose of this project is to teach you how to develop a modular input with the Python Splunk SDK and create a simple app for that modular input.
More specifically we're going to create a modular input that will fetch the prices of stock symbols and send them to Splunk. Through the modular input configuration we will set the stock symbols.

### Why Python?
Python is the easiest and quickest way to write a modular input. It’s supported from Splunk and it is already available in the majority of the environments. Supporting multiple operating systems is also trivial. The biggest benefit is that since Splunk can call your script directly, you can avoid all the “hacks” to make your modular input work. Don’t forget that Splunk offers SDKs for the following languages Java, JavaScript, PHP, Ruby and C#. If Python is not your thing, great! Pick one of the others and start sending data ;) More information about the rest of the SDKs can be found [here](http://dev.splunk.com/sdks).

### What is needed
* [A Splunk instance](https://www.splunk.com/en_us/download/splunk-enterprise.html)
* [The Splunk Python SDK](http://dev.splunk.com/goto/sdk-python)
* Your favorite python editor (I used PyCharm for this example)
* 15 minutes (that’s the most difficult part)

### Project Structure
This repository is consisted of three main folders

* bin -contains our python application and the Splunk SDK
	* stocks_mod_input.py -contains our python program
	* splunklib -the Splunk SDK, copy the folder from the Python SDK files
* default
	* app.conf -contains configuration for our Splunk app
* inputs.conf -contains configuration for the inputs
* README
	* inputs.conf.spec -contains the specs for the inputs

### Project Build
#### Part 1: The Python program
We are going to build a simple modular input that it is going to fetch the stock data from Yahoo’s Stock API.
```http://finance.yahoo.com/webservice/v1/symbols/SPLK/quote?format=json```
The API returns the following JSON response:
```sh
{
list:
{
meta:
{
type: "resource-list",
start: 0,
count: 1
},
resources:
[
{
resource:
{
classname: "Quote",
fields:
{
name: "Splunk Inc.",
price: "49.509998",
symbol: "SPLK",
ts: "1459972800",
type: "equity",
utctime: "2016-04-06T20:00:00+0000",
volume: "1213184"
}
}
}
]
}
}
```

### The Python program is consisted of 4 main key parts:
### The getScheme method
The getScheme method is responsible to return the Scheme for the modular input. In this specific example we specify 1 argument, the stock symbol. The Scheme class will generate the XML to be parsed by Splunk for the modular input using the ```--scheme``` argument. When adding a new modular input we will be asked to provide these values. Splunk will then pass these arguments to our modular input and provide the APIs to read these values. Another example of these input values could be the username and the password of a twitter account. A modular input could read these values and fetch all the tweets of that user.

>To verify and check the XML Scheme, run the following command:
```sh
$ python stocks_mod_input.py --scheme
```

### The validateInput method
ValidateInput is an optional step used to validate that the value entered exists as a stock symbolIn this specific example we are fetching the requested symbol and make sure the ```count``` field is different than ```0```.

### The streamEvents method
You can use a modular input multiple times. For example you can fetch multiple stock values. Another example is to use the Twitter modular input to fetch data from multiple accounts. But remember, the modular input is ```one``` process. This is the reason why inside the streamEvents there is a for loop. During start (that happens once, when Splunk starts or when you start the modular input), it loops through the different setups and provides the values for each one of them. Then we have to run our worker that uses the information provided to create an event.

### The do_work
Think of the do_work as our worker function. Provided the stock symbols we got from Splunk, we have to do something with them, produce an output -in this case the current value- create an event and send it to Splunk. Our app is really simple, we are making a HTTP GET request to the constructed API call, parse the response and create our event in the format ```symbol=SPLK price=58```.

>All the output from the EventWritter.log can be found at ```$SPLUNK_HOME/Splunk/var/log/splunk/splunkd.log```


#### Part 2: The modular input app
A modular input in python does not require complicated configuration.

Let’s analyze the app’s ```default``` directory. This directory is used by Splunk to create the modular input app.

### app.conf
```sh
[install]
is_configured = 1
[ui]
is_visible = 0
label = Stock symbol modular input
[launcher]
author = Kostas Polychronis
description = A simple modular input in python
version = 1.0
```
The most important line here is the ```is_visible```. Since our modular input doesn’t have an accompanying app, we don’t want it to be visible with the other installed apps.

### indexes.conf

In this specific example we will not use an indexes.conf configuration file. That means that Splunk will write the data to the ```default``` index.

> More info on the ```indexes.conf``` can be found [here](http://docs.splunk.com/Documentation/Splunk/latest/Admin/Indexesconf)

### inputs.conf
```sh
[stocks_mod_input]
interval = 60
```
Inside inputs.conf we will not specify the index nor the sourcetype for out data. Splunk will assign these values automatically. We do though want to specify the interval for our modular input. In this specific example our script will run every ```1 minute```.

> More info on the ```inputs.conf``` can be found [here](http://docs.splunk.com/Documentation/Splunk/6.2.8/Data/Editinputs.conf)

# How to install it
Installing the example is trivial. Just copy and paste the main folder to the folder ```$SPLUNK_HOME/Splunk/etc/apps```.
Then in order for Splunk to refresh the apps list you have to restart Splunk.

In order to create a new configuration of the myinput modular input, go to ```Settings -> Data -> Data Inputs``` find the modular input under the ```Local Inputs``` section and click ```Add new```.

There you will be asked to input the configuration for the modular input. Then you will be able to see the stock values at your Search app.

# Notes
This example is not perfect nor ideal. It is based on the official documentation for the [Splunk Python SDK](http://dev.splunk.com/view/python-sdk/SP-CAAAER3)

License
----

MIT

