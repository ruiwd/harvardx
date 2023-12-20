import os
import random
import re
import sys
from collections import Counter

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
    num_links = len(corpus[page])

    if not num_links:
        num_links = len(corpus)

    linked_page = damping_factor/num_links
    random_page = (1 - damping_factor)/len(corpus)
    page_probability = {}

    for i in corpus:
        if i in corpus[page]:
            page_probability[i] = round(linked_page + random_page, 4)
        else: page_probability[i] = round(random_page, 4)

    return page_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start_page = random.choice(list(corpus.keys()))

    samples = []
    samples.append(start_page)

    for i in range(n-1):
        page_probability = transition_model(corpus, start_page, damping_factor)
        el = list(page_probability.keys())
        pr = list(page_probability.values())
        selected = random.choices(population=el, weights=pr, k=1)[0]
        samples.append(selected)
        start_page = selected
    
    sample_results = dict(Counter(samples))
    
    for j in sample_results:
        sample_results[j] = round(sample_results[j] / n, 4)

    return sample_results


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    old_pr = {}
    new_pr = {}
    converged = False
    new_corpus = {}
    
    for page in corpus:
        if not len(corpus[page]):
            new_corpus[page] = set(corpus.keys())
        else: 
            new_corpus[page] = corpus[page]

    for i in corpus:
        old_pr[i] = 1/len(corpus)

    while converged == False:
        if new_pr:
            old_pr = new_pr
            new_pr = {}
            
        for j in old_pr:
            new_pr[j] = calc_pr(new_corpus, damping_factor, j, old_pr)

        test = True
        for k in new_pr:
            if abs(new_pr[k] - old_pr[k]) > 0.001:
                test = False
        
        converged = test
    
    return new_pr

def calc_pr(corpus, damping_factor, page, old_pr):
    parent_links = []
    parent_prs = []

    for i in corpus:
        if page in corpus[i]:
            parent_links.append(i)

    for j in parent_links:
        parent_prs.append(old_pr[j]/len(corpus[j]))

    new_value = (1-damping_factor)/len(corpus) + damping_factor*sum(parent_prs)

    return new_value


if __name__ == "__main__":
    main()
