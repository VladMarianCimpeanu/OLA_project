# OLA_project
Online Learning Application Project 

Course held @ Politecnico di Milano\
Acadamic year 2021 - 2022

## Table of contents
* [Motivation](https://github.com/VladMarianCimpeanu/OLA_project/edit/main/README.md#motivation)
* [Problem](https://github.com/VladMarianCimpeanu/OLA_project/edit/main/README.md#problem)
* [Repository structure](https://github.com/VladMarianCimpeanu/OLA_project/edit/main/README.md#repository-structure)
* [Set up](https://github.com/VladMarianCimpeanu/OLA_project/edit/main/README.md#set-up)

## Developed by
| Name | Surname | person code | github | 
|------|---------|--------|--------|
| Sofia | Martellozzo | 10623060 | [link](https://github.com/sofiamartellozzo)|
| Vlad Marian | Cimpeanu | 10606922 | [link](https://github.com/VladMarianCimpeanu)|
| Lorenzo | Rossi | 10698834 | [link](https://github.com/tpoppo)|

## Topic
*Social influence techniques and Pricing*

## Motivation
Nowadays one big problem of e-commerces is to allocate the best price to its products so that, the
seller can maximize its margin.\
The main issue is that increasing the price of a product leads to fewer people interested in that
product, thus increasing the price is not necessarily beneficial to the seller. In contrast, decreasing
the price will increase the number of people interested in the product, but the revenue will be of
course sub-optimal.\
In order to maximize the revenue, we can analyze the demand curve of a given product, which is
a graphical representation of the relationship between the price $p_i$ of a good or service $i$ and the
quantity demanded $q_i(p_i)$ for a given period of time, and find the price $\hat{p}$ such that:
\
\
&ensp; &ensp; &ensp; &ensp; $\hat{p} = argmax(pq(p))$
\
\
Unfortunately, in real-world problems, the demand curve is not available, furthermore, we need to
estimate this curve by interacting with the environment. One main problem of interacting with an
unknown environment is that exploration costs a lot of money, so we want to find the best prices
in the shortest amount of time to decrease the regret.
In order to do so, we can use reinforcement learning techniques such as Multi Armed Bandit (MAB)
algorithms.

## Problem
In our project we deal with a website supported by a recommender system: once a customer buys a specific product, it will suggest up to 2 new products (called secondary products), thus, a customer might buy multiple products during the same visit.\
Here an example of the recommender system graph:
![image](https://user-images.githubusercontent.com/62434812/194702338-57ebcfe3-a5ad-4f6d-b716-125e93d51032.png)
From this graph we can see for instance, if a customer decides to buy a shirt, the system will suggest to buy a hoodie and a t-shirt.\
This means our algorithm should consider the indirect reward a specific product may lead.\
For more details about the environment and its settings, read the [report](https://github.com/VladMarianCimpeanu/OLA_project/blob/main/Report/main.pdf).\
In order to solve this problem:
* each day we estimate the customers' conversion rate with MAB algoirhtms based on the collected observations.
* according to the estimated conversion rates, we solve a combinatorial problem to find the best prices using a dynamic programming approach. DP gives a correct estimate of the margin given by the prices (assuming the conversion rate estimates are correct) but is computationally expensive, thus, this approach is affordable in small optimization problems as this one. In case of more complex problems, one may consider using Montecarlo simulations to have a raw estimate of the reward in reasonable time.

We compare the performances achieved by UCB-1 and Thompson sampling algorithms.

## Repository structure
* [Code](https://github.com/VladMarianCimpeanu/OLA_project/tree/main/Code) folder contains all the classes used to solve the problem:
  * [environment package](https://github.com/VladMarianCimpeanu/OLA_project/tree/main/Code/environment) content is mainly used to simulate the environment, which our alogrithms interact with.
  * [data folder](https://github.com/VladMarianCimpeanu/OLA_project/tree/main/Code/data) contains json files having all the parameters used to model the customers (real conversion rates, click rates, ...) and the graph used by the recommender system.
* [Report](https://github.com/VladMarianCimpeanu/OLA_project/tree/main/Report) folder contains the latex code used for the [pdf report](https://github.com/VladMarianCimpeanu/OLA_project/blob/main/Report/main.pdf).

Here a simplified UML of the project:
![UML_ola](https://user-images.githubusercontent.com/62434812/194703935-3a35f387-5081-403e-a3da-d0852e8a1859.svg)

## Set up
Use the following command to compile the report.

```bash
pdflatex -shell-escape  main.tex
```
