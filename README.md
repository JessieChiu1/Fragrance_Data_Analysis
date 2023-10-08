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
- 10/8/2023: Web scraped all perfumers and created a list of all of their respective pages

### Project Tasks

The plan so far:

1. Navigate to [fragrantica.com](https://www.fragrantica.com/noses/).
    - create a list of all of the perfumers' link
    - web scrape all of the fragrances' link from the perfumer's page
2. Go to each link and web scrape the data for each respective fragrance.
    - Store the information as JSON.

## Required Libraries

To run this script, you'll need to install the following Python libraries using `pip`:

```bash
pip install selenium
pip install tqdm
```

## Challenges

During development, the following challenges were encountered:

1. **Getting all the fragrances"** 
- At first, I tried to go to the search page [here](https://www.fragrantica.com/search/) and use selenium to keep clicking the "show more results" button but I ran into 2 issue:
    - There was an issue where the button existed but couldn't be clicked because an iframe/Google Ads element was blocking the button. I had to search for the correct exception to bypass this error. `ElementClickInterceptedException`
    - Once I get pass the button clicking issue, I noticed that the site only allows result up to 1,000 so I had to find another way to get all of the fragrances.

2. **Designing the roadmap** - I have a good idea of what I want to do, but I need to figure out how to design the script better so that I might not have to web scrape the page from scratch each time. I am currently storing the HTML/links to fragrances for reference so that while testing, I am not waiting for Selenium to web scrape 85k fragrances.

3. **Adding more feedback** - While revisiting my old project, I noticed that I don't often write `print` statements to provide feedback on my Python code. Especially now that this project has over 85k fragrances to go through, the web scraping part of the code takes a long time. I want to add some feedback on what is happening in my code. I install the tqdm package to display process meter for my loop

