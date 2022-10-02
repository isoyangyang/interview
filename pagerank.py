import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    for key, value in corpus.items():
        print(key, type(value), value)
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
    # Return dictionary
    output_dictionary = copy.deepcopy(corpus)
    for key in output_dictionary.keys():
        output_dictionary[key] = 0

    # Retrieve dictionary keys aka links from page
    links = set()
    for key, value in corpus.items():
        if key == page:
            print(key, page, value)
            links = value

    # Number of links available on the current page
    num_page_links = len(links)
    num_corpus_pages = len(output_dictionary)
    random_all_pages = (1 / num_corpus_pages) * (1 - damping_factor)

    # if set is empty choose among all corpus pages equally
    if num_page_links == 0:
        for key in output_dictionary.keys():
            output_dictionary[key] = random_all_pages
        return output_dictionary
    else:
        random_links = (1 / num_page_links) * damping_factor
        for key in output_dictionary.keys():
            if key in links:
                output_dictionary[key] = (random_all_pages + random_links)
            else:
                output_dictionary[key] = random_all_pages
        return output_dictionary

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a deepcopy of dictionary
    pagerank_dictionary = copy.deepcopy(corpus)
    dict_counter = copy.deepcopy(pagerank_dictionary)
    for key in dict_counter:
        dict_counter[key] = 0

    # get the keys and get a random page entry for first sample
    page_list = list(pagerank_dictionary.keys())
    random_entry = random.choice(page_list)

    # based on the previous derive transitional model results and next page
    sample = transition_model(pagerank_dictionary, random_entry, damping_factor)
    iteration_weights = list(sample.values())
    next_page = random.choices(page_list, iteration_weights)

    # Count hits per page
    dict_counter[next_page[0]] += (1 / n)

    for i in range(n - 1):
        sample = transition_model(pagerank_dictionary, next_page[0], damping_factor)
        n_iteration_weights = list(sample.values())
        next_page = random.choices(page_list, n_iteration_weights)
        dict_counter[next_page[0]] += (1 / n)

    return dict_counter


def num_links(corpus, source_page):
    """
    Number of links to a given page
    """
    links = set()
    for key, value in corpus.items():
        if key == source_page:
            links = value
    number = len(links)
    return number


def num_pages_link(corpus, page):
    """
    Number of incoming pages
    """
    incoming = []
    for key, value in corpus.items():
        for x in value:
            if x == page:
                incoming.append(key)
    return incoming


def iterative_test(iterative_dictionary, corpus, random_surfer, damping_factor):
    """
    Returns the next iteration of the dictionary
    """
    return_dict = copy.deepcopy(iterative_dictionary)
    for key in iterative_dictionary.keys():
        incoming_pages = num_pages_link(corpus, key)
        end_of_equation = 0
        for i in range(len(incoming_pages)):
            end_of_equation += (iterative_dictionary[incoming_pages[i]] / num_links(corpus, incoming_pages[i]))
        placeholder = random_surfer + (damping_factor * end_of_equation)
        return_dict[key] = placeholder
    return return_dict


def threshold_check(list1, threshold):
    for i in list1:
        if i > threshold:
            return True
    return False


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    iterative_dictionary = copy.deepcopy(corpus)
    corpus_len = len(corpus)

    for key in iterative_dictionary.keys():
        iterative_dictionary[key] = (1 / corpus_len)

    random_surfer = (1 - damping_factor) / corpus_len

    threshold = 0.001

    while True:
        delta = []
        temp = copy.deepcopy(iterative_dictionary)
        iterative_dictionary = iterative_test(iterative_dictionary, corpus, random_surfer, damping_factor)
        for key in temp.keys():
            delta.append((temp[key] - iterative_dictionary[key]))
        if not threshold_check(delta, threshold):
            break
    return iterative_dictionary


if __name__ == "__main__":
    main()
