# opencorporates

In the `config.ini` file we have the parameters that will be used by our program. Please notice that we will need all of them to run our program successfully

## Automated unit tests
The testing that I have developed for this project is really basic, I just wanted to make sure the URL is being built correctly (but without including any regex validation that could be enabled if the scope of the project was different).
## Error handling if the API returns error codes
I have designed the error handling to be very simple in this project.
I will let the users know what failed with the request, by showing them the status code and the reason.
If we get the status code `403`, this means that we are not properly authenticated or we have exceeded the API rate limits. It doesn't make any sense to keep the program running, hence it will stop immediately.
## Handling of API rate limiting
I have been using Postman to get familiar and play around with the API, and I have seen that the daily API calls limit is 10000 and the montly limit is 50000. The number of companies that have the word "smart" in their name is 109731, so we would need 1098 API calls to retrieve all of them (assuming that we use the biggest page size, which is 100).

In the case we reached those limits, the program would inform the user and it would stop, as stated in the section above.
## Handling API keys/secrets
We can use a few methods to manage credentials and/or other sensitive information. I will list some of them from least to most secure:

1. Hard-coding the secrets
2. Decoupling the secrets using config files
3. Use (v)environment variables
4. Rely on the user to input the credentials

I chose the second option in this case, as this is a mock project and the secrets won't be publicly available, so this method it will be very quick to implement as I can reuse the code that I have been using for other personal projects. I will be using the config file to manage other variables, so this option is the most efficient.

If I had to share the project with multiple users, I would definitely go for methods 3 & 4. Depending on the users, I would use the 4 if they had access to these credentials too (e.g. sharing the code with other developers), and I would pick the method 3 if I needed to share the project with other less-technical trusted users (e.g. our Sales team).
## Scalability

The execution time will linearly increase with higher volumes of data.

It takes approximately 1-1.5 seconds to get 100 results from the API, which is the maximum page size that we can retrieve at the same time. The below screenshot shows the execution time of one of these petitions:

![petition_time](petition_time.png)

It took me 4 minutes and a half to get the first 10,000 companies that had the word "smart" in their name.
I needed 4 minutes to retrieve the results, 0.1 second to store them in a csv file, and 30 seconds to upload the csv into the database.

Taking into consideration the above, it would take us about 45 minutes to retrieve 100,000 company records, 1 second to store them in a csv file, and 5 minutes to upload the csv into the database.

The time complexity is linear, `O(n)`, but we could speed it up if we sent requests in parallel and made the database insertions in batches so we reduce the number of connections that we have to open/close to the database.

## Database election
I picked up SQLLite as this project is really basic and we don't need many features to succeed, we just want it to be easy to set up and use. 

If we needed the database to be more secure (to implement authentication), more scalable or more performant I would have definitely picked up MySQL.  


