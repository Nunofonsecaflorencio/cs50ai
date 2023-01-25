import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize with random chosen from all pages in the corpus
    probabilities = {
        page: (1 - damping_factor) / len(corpus) 
        for page in corpus 
    }
    
    # if the current page has no outgoing links, treat it as having links to all pages
    links = corpus.get(page, corpus.keys())
    
    # Distribute linked pages
    for link in links:
        probabilities[link] += damping_factor / len(links)
    
    # Normalize
    normalize(probabilities)
    return probabilities            
        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_rank = {
        page: 0 for page in corpus 
    }
    # Initial random page
    page = random.choice(list(corpus.keys()))
    page_rank[page] += 1 / n
    
    for _ in range(n - 1): # n-1 because the first random page its one sample
        # Choose next page based on their weights
        probabilities = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probabilities), weights=list(probabilities.values()), k=1)[0]
        page_rank[page] += 1 / n
        
    # Normalize
    normalize(page_rank)
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    ERROR = 0.001
    # Initialize all with PR(p) = 1 / N
    page_rank = {
        page: 1 / N for page in corpus 
    }
    
    while True:
        new_page_rank = dict()
        
        for page in corpus:
            sum_PRi = 0
            for pageI in corpus:    
                if page not in corpus[pageI]:
                    continue
                # If pageI links to page 
                NumLinks = len(corpus[pageI])
                sum_PRi += page_rank[pageI] / NumLinks
            
            # Calculate PR(page)    
            new_page_rank[page] = (1 - damping_factor) / N + damping_factor * sum_PRi
        
        # Check convergence
        if all([abs(new_page_rank[page] - page_rank[page]) < ERROR for page in corpus]):
            break    
        # Go to next iteration
        page_rank = new_page_rank
    
        
    normalize(page_rank)
    return page_rank
    

def normalize(distribution):
    SUM = sum(distribution.values())
    for key in distribution:
        distribution[key] /= SUM
        
        
if __name__ == "__main__":
    main()
