# Fragrantica Web Scraping and Data Analysis (Work in Progress)

## Introduction

This project aims to web scrape all the fragrances on [fragrantica.com](https://www.fragrantica.com/noses/) for the purpose of conducting data analysis.

I thought this would be a good way to practice what I've learned with Python and web scraping.

I haven't figured out the scope of the data analysis yet, but so far, I have decided to include breakdowns on the following:
- Most popular notes
    - Possibly further breakdown based on top/middle/base notes
- Breakdowns on accords
- Breakdowns on the average user's voted longevity/sillage

## Timeline So Far
- 10/8/2023: Web scraped all perfumers and created a list of all their respective pages
- 10/12/2023: Trying to scrape all 85k+ fragrances by perfumers but having trouble without Selenium getting stuck 

### Project Tasks

The plan so far:

1. Navigate to [fragrantica.com](https://www.fragrantica.com/noses/).
    - Web scrape all of the perfumer's names.
    - Use the perfumer's name to search for fragrances created by them (can't search for all because the maximum result shown is 1,000).
2. Perform data analysis.

## Required Libraries

To run this script, you'll need to install the following Python libraries using `pip`:

```bash
pip install selenium
pip install tqdm
```

## Challenges

During development, the following challenges were encountered:

1. **Getting all the fragrances** 
    - **First attempt -** I tried to go to the search page [here](https://www.fragrantica.com/search/) and use Selenium to keep clicking the "show more results" button, but I ran into two issues:
        - There was an issue where the button existed but couldn't be clicked because an iframe/Google Ads element was blocking the button. I had to search for a solution to bypass the `ElementClickInterceptedException` error. I ended up adding a JavaScript command to scroll the element to the center of the page so it would not be blocked by any Google ads.
        - Once I got past the button-clicking issue, I noticed that the site only allows results up to 1,000, so I had to find another way to get all of the fragrances.
    - **Second attempt -** I web scraped all the perfumer's names [here](https://www.fragrantica.com/noses/) and then went back to the search page and input the perfumer's name to get all the fragrances by them. I ran into a few issues:
        - When I click another link, the routing is intercepted by Cloudflare. I had so much trouble passing the bot detection. I noticed that Cloudflare only pops up when I go to another link with Selenium, and not the initial `driver.get(url)`. I decided to separate the two web scraping instances into two separate Python files. 
        - My plan now is:
            1. `fetch_perfumers.py` - Web scrape the perfumer's names and save the result to a JSON.
            2. `fetch_fragrances.py` - Load the result from step 1 and loop through each of the perfumer's names to get their fragrance links.
            3. Loop through all of the results from step 2 to web scrape each link.

2. **Designing the roadmap** - I have a good idea of what I want to do, but I keep running into unexpected roadblocks like the Cloudflare bot detection. I have been trying to work around all of these problems. Some examples:
    - Bypassing the max 1,000 result threshold by finding all of the perfumers' names first, then searching for the fragrance by them.
    - Bypassing Cloudflare by using two different Python scripts to instantiate a new driver so I don't have to avoid routing to a different link and triggering Cloudflare.
    - Now trying to troubleshoot Selenium getting stuck during the loop through all of the perfumers.

3. **Adding more feedback** - While revisiting my old project, I noticed that I don't often write `print` statements to provide feedback on my Python code. Especially now that this project has over 85k fragrances to go through, the web scraping part of the code takes a long time. I want to add some feedback on what is happening in my code.   
    - I installed the `tqdm` package to display a process meter for my loop.
    - Adding more print statements to give feedback on which step the script is on.


## Mistakes and Things I Learned
- `Selenium`: The `By.CLASS_NAME` method is designed to find elements by their CSS class attribute, and it expects you to provide only a single class name.When you use multiple class names or a class name that includes spaces, it won't work as expected, so you must use `By.CSS_SELECTOR`
- `Selenium`: You can also get an element by their attribute like placeholder/value/name etc.
- I spent too much time tunnel visioning on making a certain method work like:
    - trying to bypass the cloudflare bot detection, I ended up finding a solution that avoided cloudflare directly.