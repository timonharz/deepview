from bs4 import BeautifulSoup
import requests

class YahooFinanceProvider:
    def __init__(self):
        self.base_url = "https://finance.yahoo.com/quote/{symbol}"
        self.url = "https://finance.yahoo.com/news"
        self.latest_news_url = "https://finance.yahoo.com/topic/latest-news/"

    def get_news_from_symbol(self, symbol):
        url = self.base_url.format(symbol=symbol)
        response = requests.get(url)
        
    def fetch_recent_news(self):    
        
        
        
        # Make a request to fetch the page content
        response = requests.get(self.latest_news_url)
        
        print("Response status code: ", response.status_code)
        
        soup = BeautifulSoup(response.text, 'html.parser')


        if response.status_code == 200:
            # Find the news section using the ID provided in your example
            news_section = soup.find('div', id='mrt-node-Fin-Stream')

            # Check if news_section is found
            if news_section:
                # Find the unordered list that contains the news items
                news_list = news_section.find('ul')

                # Check if the news list is found
                if news_list:
                    # Iterate over each list item (li) in the news list
                    all_items = news_list.find_all('li', class_='js-stream-content')
                   
                    for item in all_items:
                        # Find the headline link and image (if available)
                        headline_link = item.find('a')
                        image = item.find('img')

                        # Extract headline text
                        if headline_link:
                            headline_text = headline_link.get_text(strip=True)
                            article_url = headline_link['href']
                            article_text = self.get_article_text(article_url)
                            if article_url.startswith('/'):
                                article_url = url + article_url  # Add base URL if needed

                            # Extract image source (if available)
                            image_src = image['src'] if image else "No image available"

                            # Print the results
                            print(f"Headline: {headline_text}\nLink: {article_url}\nArticle text: {article_text}")
                    print("Total items: ", len(all_items))
                else:
                    print("News list not found.")
            else:
                print("News section not found.")
           
        else:
            print(f"Failed to retrieve news: {response.status_code}")
                    
    # Function to get the article text from a given URL
    def get_article_text(self, article_url):
        # Send a request to fetch the article content
        article_response = requests.get(article_url)
        
        # Check if the request was successful
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            # Find the article body
           # Find the specific <div> by class
            target_div = article_soup.find('div', class_='body-wrap yf-i23rhs')

            if target_div:
                # Extract text content from the found <div>
                div_text = target_div.get_text(separator='\n', strip=True)
                return div_text
            else:
                return "No target <div> found."
        else:
            return f"Failed to retrieve article: {article_response.status_code}" 
            
provider = YahooFinanceProvider()
provider.fetch_recent_news()
