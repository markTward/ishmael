# Welcome to Ishmael!
Ishmael is a prototype for a friendly malware identification and research service with a small collection of RESTful resources. Use them to check the status of a single URL or search more broadly across a domain and path.

## RESTful Resources Available
* Match Using URL's Exact Path and Parameters
* Search Across Partial Path and Parameter Pairs
* Find Record Using Known Ishmael Identifier

## Demonstration
You can try out Ishmael and learn more about the service at this URL:  
[https://ishmael-demo.herokuapp.com/](https://ishmael-demo.herokuapp.com/)

You can interact with the service directly from the browser or from the command line using curl.  Here's an example:  
`curl -i https://ishmael-demo.herokuapp.com/urlinfo/1/path/melville.io/helloishmael?call=me`

The small Heroku deployment may need to awaken upon the first home page or query access, but subsequent attempts should be well covered by the database indexes and perform crisply.

## Some Details
I've implemented Ishmael using Python and Flask to provide the core of the RESTful API, utilizing MongoDB as the datastore.

To help assess performance, I've generated nearly a million random urls, imported a public phishing data set, and created some fun character-based ones from Moby Dick.

In addition to the examples found on the home page, try the /urlinfo/1/search/ endpoint with 'abc', 'www.paypal', or 'the.whale.melville.net' to get a block of records to facilitate investigation of the service.
