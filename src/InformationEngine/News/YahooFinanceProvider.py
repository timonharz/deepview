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
            
            news_section_text = news_section.get_text(separator='\n', strip=True)
            
            print("News section text: ", news_section_text)

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
                            article_text = self.extract_article_text(article_url)
                            if article_url.startswith('/'):
                                article_url = url + article_url  # Add base URL if needed

                            # Extract image source (if available)
                            image_src = image['src'] if image else "No image available"

                            # Print the results
                            print(f"Headline: {headline_text}\nLink: {article_url}\nArticle text: {article_text[:50]}")
                            
                            
                    print("Total items: ", len(all_items))
                else:
                    print("News list not found.")
            else:
                print("News section not found.")
           
        else:
            print(f"Failed to retrieve news: {response.status_code}")
                    
    # Function to get the article text from a given URL
    def get_article_text(self, article_url):
        print("Running get_article_text")
        # Send a request to fetch the article content
        article_response = requests.get(article_url)
        
        # Check if the request was successful
        if article_response.status_code == 200:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            # Find the main article content
            article_content = article_soup.find('div', {'data-component': 'article-body'})
            print("\nArticle content: ", article_content)

            if article_content:
                # Extract all paragraph texts
                paragraphs = article_content.find_all('p')
                article_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
                return article_text
            else:
                return "No article content found."
        else:
            return f"Failed to retrieve article: {article_response.status_code}"
        
        
        
    def extract_article_text(self, url):
        """
        Fetches and extracts the text content from the provided article URL.
        
        :param url: The URL of the article to extract text from.
        :return: The extracted text content of the article.
        """
        try:
            # Fetch the webpage content
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse the webpage content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from <p> tags (usually article text is inside <p> tags)
            paragraphs = soup.find_all('p')

            # Combine all text into one string, stripping any extra whitespaces
            article_text = '\n'.join([para.get_text(strip=True) for para in paragraphs])

            return article_text

        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching the article: {e}"
            
provider = YahooFinanceProvider()
provider.fetch_recent_news()
print("Yahoo Data Provider: Done fetching news.")
