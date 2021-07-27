# swapcard_demo
Technical Demo for Swapcard Application Process

# Setup
First:  
**```Make sure you have Python 3 and pip installed in your machine```**

## Browsers and drivers
- Have [Google Chrome](https://www.google.com/chrome/) installed in your machine and an appropriate [chromedriver](https://chromedriver.chromium.org/downloads) for its version.
- Have [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/) installed in your machine and an appropriate [geckodriver](https://github.com/mozilla/geckodriver/releases/tag/v0.29.1) for its version.

Make sure both **chromedriver** and **geckodriver** are in the **PATH** environment variable of the system

## Installing packages and dependencies
```pip install -r requirements.txt```

# Running the project
To run the test, just call `pytest`

## Defining user and password
Edit the file `data/users.json` with the appropriate user and password to log into the system.

## Choosing browser for text execution
By default, the test will run in Chrome, but it can also run in Firefox if wanted. Use the `--browser="[option]"` with `pytest`.
- `pytest --browser="Chrome"`
- `pytest --browser="Firefox"`

### Run in both browsers
`pytest --browser="Chrome" --browser="Firefox"`  
The tests will run in both browsers following the `--browser` order.
