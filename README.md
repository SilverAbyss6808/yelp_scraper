yelp scraper v1.0
by lila baxter 10/03/2024

to run: python scraper.py [zipcode]
- if no zipcode is provided, it will default to 45810
- if it doesn't work, try the relative filepath (absolute path only if that doesn't work)

known bugs:
- doesn't validate if it's a real zipcode, will just crash
- rate limit can be exceeded if used too many times in succession, let it cool down for 10-15 minutes and try again
