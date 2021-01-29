# IMDB_Web_Scraper
Multi-Threaded IMDB Web Scraper with VaderSentiment Analysis

Uses Selenium, BeautifulSoup4, and Vader Sentiment (links at the bottom) to web scrape IMDB for movie reviews and then performs Sentiment Analysis

Warning: Currently only works with Firefox and uses the direct path to geckodriver

Steps to use:
  1. Run program and input the name of the show or movie
  
  2. Select the show/movie if you can see it
  
  3a. If the original score is greater then 0.05 (>0.05) it has mostly positive reviews
  
  3b. If it is lower than is 0.05 (<0.05) it has mostly negative reviews
  
  Selenium:https://github.com/baijum/selenium-python
  
  BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup
  
  VaderSentiment: https://github.com/cjhutto/vaderSentiment
