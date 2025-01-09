# A Comparative Analysis of Retrievability and PageRank Measures

<p>
    <a href="https://doi.org/10.1145/3632754.3632760">
        <img alt="DOI" src="https://img.shields.io/badge/DOI-10.1145%2F3632754.3632760-blue.svg">
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="https://arxiv.org/abs/2311.10348">
        <img alt="arxiv" src="https://img.shields.io/badge/arXiv-2311.10348-b31b1b.svg">
    </a>
</p>

Official implementation for our paper [A Comparative Analysis of Retrievability and PageRank Measures](https://arxiv.org/abs/2311.10348) with code and result data. In this paper, we compute rank correlation coefficents (Kendall's $\tau$, Spearman's $\rho$, Ranked Biased Overlap (RBO)) between Retrievability and PageRank scores of the documents for 2 collections (Wikipedia and WT10g).

### Paper Abstract

The accessibility of documents within a collection holds a pivotal role in Information Retrieval, signifying the ease of locating specific content in a collection of documents. This accessibility can be achieved via two distinct avenues. The first is through some retrieval model using a keyword or other feature-based search, and the other is where a document can be navigated using links associated with them, if available. Metrics such as PageRank, Hub, and Authority illuminate the pathways through which documents can be discovered within the network of content while the concept of Retrievability is used to quantify the ease with which a document can be found by a retrieval model. In this paper, we compare these two perspectives, PageRank and retrievability, as they quantify the importance and discoverability of content in a corpus. Through empirical experimentation on benchmark datasets, we demonstrate a subtle similarity between retrievability and PageRank particularly distinguishable for larger datasets.

### Retrievability measure

The **retrievability** measure quantifies how easily a document can be retrieved in a specific configuration of an Information Retrieval (IR) system. The retrievability score, denoted as $r(d)$, is computed for a document $d$ within a collection $D$ based on a set of queries and their associated weights. The formal representation of the retrievability formula is as follows:

$$
r(d) = \sum_{q \in Q} o_q \cdot f(k_{dq}, c)
$$

Where:

- $r(d)$: The retrievability score of document $d$.
- $d \in D$: The document $ d $ is a member of the collection $D$.
- $Q$: The set of all possible queries that could be answered by the collection $D$. This set encompasses the entire range of queries that the IR system might encounter.
- $o_q$: The opportunity weight associated with query $q$, which quantifies the likelihood or frequency of selecting query $q$ from the set $Q$.
- $f(k_{dq}, c)$: A function that measures the effectiveness of retrieving document $d$ in response to query $q$, where $k_{dq}$ denotes the retrieval rank of document $d$ to query $q$, and $c$ represents rank cutoff after which user ceases to examine the ranked list.

### PageRank measure

The PageRank formula is as follows:

$$
PR(A) = (1 - d) + d \cdot \sum_{i=1}^{n} \frac{PR(T_i)}{C(T_i)}
$$

Where:

- $PR(A)$: The PageRank score of page $A$.
- $d$: The damping factor, typically set to 0.85. It balances the influence of following links on the current page and the randomness of jumping to any page on the web.
- $n$: The total number of pages that link to page $A$.
- $PR(T_i)$: The PageRank score of page $T_i$, a page that links to $A$.
- $C(T_i)$: The number of outgoing links from page $T_i$.
- $\frac{PR(T_i)}{C(T_i)}$: The share of the PageRank score that page $A$ receives from page $T_i$, where the score is divided by the number of outgoing links from $T_i$.

### Rank Correlation between Retrievability and PageRank

| Dataset       | Kendall's $\tau$     | Spearman's $\rho$     | RBO   |
|---------------|----------------------|-----------------------|-------|
| **WT10g**     | 0.0487               | 0.0730                | 0.5173|
| **Wikipedia** | 0.1532               | 0.2247                | 0.5633|

We observe, while lower Kendall’s $\tau$ and Spearman’s $\rho$ indicate weak correlations overall, the higher value of RBO reveals a substantial overlap in the top-ranked documents when considering both retrievability and PageRank. This implies that, although the two metrics may not be highly correlated overall, they tend to agree on at least in terms of the top elements of their respective ranked lists (sorted based on the retrievability and PageRank values).

## Citation

```
@inproceedings{10.1145/3632754.3632760,
author = {Sinha, Aman and Mall, Priyanshu Raj and Roy, Dwaipayan and Ghosh, Kripabandhu},
title = {A Comparative Analysis of Retrievability and PageRank Measures},
year = {2024},
isbn = {9798400716324},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3632754.3632760},
doi = {10.1145/3632754.3632760},
booktitle = {Proceedings of the 15th Annual Meeting of the Forum for Information Retrieval Evaluation},
pages = {67–72},
numpages = {6},
location = {Panjim, India},
series = {FIRE '23}
}
```
