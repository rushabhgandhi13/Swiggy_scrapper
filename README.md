# Swiggy_Scarpper
Scraping Swiggy website for Restuarant and Menu details

This project deals with 2 aspects

  1) Scraping Swiggy website for restuarant details and finding the cheapest items in a particular area(here Mumbai) and storing it into csv file(A1_output.csv)
  
  2) Calculating the spends on swiggy and finding the values like average order value, Total spendings, Most ordered dish.. etc and storing it to a text file(A2_output.txt). The order data is also stored in sqlite database named swiggy.db
  
<hr>

The script expects you to give your swiggy session as input.

- Login to swiggy.com or zomato.com on a browser (chrome or firefox)
- Install the [Cookie Editor chrome extension](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en) or the [Cookie Editor firefox extension](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to the Swiggy tab or Zomato tab and click on the Extension's icon, and select "Export". This will copy your cookies to clipboard
- Create a new file called `cookies.json` in the same directory as the `swiggy.py` script or `zomato.py` script and paste the copied 
