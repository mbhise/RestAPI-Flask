Static website = http://gsd-auth-callinfo.s3-website.us-east-2.amazonaws.com/
The phone number complaint data from this static website is parsed via a RESTful API.

We can view the results in browser:

JSON for all results
http://localhost:5000/results
You can limit the results by appending /<limit> to the url
  
JSON for results for a specific area code
http://localhost:5000/resultsForArea/<area_code>
You can limit the results by appending /<limit> to the url


