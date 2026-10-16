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
    probabilities = {}
    N = len(corpus)
    if len(corpus[page]) == 0:
        for p in corpus:
            probabilities[p] = 1/N
        return probabilities

    for p in corpus:
        probabilities[p] = 1 - damping_factor / N

    for linked_page in corpus[page]:
        probabilities[linked_page] += damping_factor / len(corpus[page])

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    for p in corpus:
        page_rank = {p: 0 for p in corpus}
        page = random.choice(list(corpus.keys()))
        page_rank[page] += 1
        for _ in range(n):
            probabilities = transition_model(corpus, page, damping_factor)
            pages = list(probabilities.keys())
            weights = list(probabilities.values())
            page = random.choices(pages, weights=weights, k=1)[0]
            page_rank[page] += 1
        
        for p in page_rank:
            page_rank[p] = page_rank[p]/n

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    for p in corpus:
        page_rank[p] = 1/len(corpus)

    while True:
        new_pagerank = {}
        for page in corpus:
            total = 0
            for other_page in corpus:
                links = corpus[other_page]
                if len(links) == 0:
                    total += page_rank[other_page]/len(corpus)
                elif page in links:
                    total += page_rank[other_page]/len(links)
            new_pagerank[page] = (1-damping_factor)/len(corpus) + damping_factor * total

        done = True
        for page in page_rank:
            if abs(new_pagerank[page] - page_rank[page]) > 0.001:
                done = False
        page_rank = new_pagerank
        if done:
            break
    return page_rank

if __name__ == "__main__":
    transition_model(corpus={"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"1.html"}}, page="1.html", damping_factor=0.85)
    main()

