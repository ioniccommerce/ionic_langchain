TOOL_PROMPT = str("""
Ionic is an e-commerce shopping tool. Assistant uses the Ionic Commerce Shopping Tool to find, discover, and compare products from thousands of online retailers. Assistant should use the tool when the user is looking for a product recommendation or trying to find a specific product. 

The user may specify the number of results, minimum price, and maximum price for which they want to see results.
Ionic Tool input is a comma-separated string of values:
  - query (required)
  - number of results (default to 5)
  - minimum price in cents
  - maximum price in cents
For example, `coffee beans, 5, 500, 1000` or `coffee beans, 5` or `coffee beans, 5, 500` or `coffee beans, 5, 1000`.
Query values cannot include commas; replace with `-`
Convert the price to cents before passing to the tool. For example, if the user asks for a product between $5 and $10, you would pass `500` and `1000` to the tool.  
Use the full detail PDP URL and always include query parameters.
""")
