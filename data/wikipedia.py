import requests
import time
from urllib.parse import urljoin
import re

BASE_URL = "https://en.wikipedia.org/w/api.php"

def get_category_articles(main_category, subcategories=None, limit=500, max_pages=5):
    """
    Get articles from a main category and its subcategories
    :param main_category: Main category to search (e.g., "Computer science")
    :param subcategories: List of relevant subcategories to include
    :param limit: Number of articles per API request (max 500)
    :param max_pages: Maximum pages to retrieve per category
    :return: Set of article URLs
    """
    articles = set()
    categories = [main_category]
    
    if subcategories:
        categories.extend(subcategories)
    
    for category in categories:
        print(f"Processing category: {category}")
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmtype": "page",
            "cmlimit": limit,
            "continue": ""
        }
        
        page_count = 0
        while True:
            if max_pages and page_count >= max_pages:
                break
                
            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                for page in data["query"]["categorymembers"]:
                    title = page["title"]
                    if not re.match(r'.*:', title):  # Exclude subpages
                        url = urljoin("https://en.wikipedia.org/wiki/", title.replace(" ", "_"))
                        articles.add(url)
                
                page_count += 1
                print(f"Found {len(articles)} articles so far...")
                
                if "continue" in data:
                    params.update(data["continue"])
                    time.sleep(1)  # Respect API rate limits
                else:
                    break
                    
            except Exception as e:
                print(f"Error processing {category}: {e}")
                break
    
    return articles

def filter_articles_by_keywords(articles, keywords):
    """
    Filter articles based on relevance keywords
    :param articles: Set of article URLs
    :param keywords: List of keywords to check for
    :return: Filtered set of URLs
    """
    relevant_articles = set()
    keyword_pattern = re.compile('|'.join(keywords), re.IGNORECASE)
    
    for url in articles:
        if keyword_pattern.search(url):
            relevant_articles.add(url)
    
    return relevant_articles

def save_articles_to_file(articles, filename):
    """Save articles to a text file"""
    with open(filename, "w", encoding="utf-8") as f:
        for url in sorted(articles):
            f.write(url + "\n")

if __name__ == "__main__":
    # Define our target categories
    cs_categories = [
        "Computer science",
        "Algorithms",
        "Data structures",
        "Artificial intelligence",
        "Machine learning",
        "Computer programming",
        "Software engineering"
    ]
    
    ds_categories = [
        "Data science",
        "Data analysis",
        "Big data",
        "Data mining",
        "Database systems",
        "Statistical analysis",
        "Machine learning"
    ]
    
    # Additional keywords to filter for relevance
    cs_keywords = [
        'algorithm', 'programming', 'software', 'computer', 'computing',
        'ai', 'artificial intelligence', 'machine learning', 'data structure',
        'complexity', 'database', 'system', 'network', 'compiler', 'operating system'
    ]
    
    ds_keywords = [
        'data science', 'data analysis', 'big data', 'data mining',
        'database', 'statistic', 'machine learning', 'deep learning',
        'visualization', 'analytics', 'processing', 'warehouse', 'mining'
    ]
    
    print("Retrieving Computer Science articles...")
    cs_articles = get_category_articles(
        "Computer science",
        subcategories=cs_categories[1:],  # Skip main category (already included)
        limit=500,
        max_pages=3
    )
    
    print("\nRetrieving Data Science articles...")
    ds_articles = get_category_articles(
        "Data science",
        subcategories=ds_categories[1:],
        limit=500,
        max_pages=3
    )
    
    # Combine and filter results
    all_articles = cs_articles.union(ds_articles)
    relevant_articles = filter_articles_by_keywords(all_articles, cs_keywords + ds_keywords)
    
    # Save results
    save_articles_to_file(relevant_articles, "cs_ds_articles.txt")
    
    print(f"\nFound {len(all_articles)} total articles")
    print(f"Saved {len(relevant_articles)} relevant articles to cs_ds_articles.txt")