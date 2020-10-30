# Tweet Influencers October Surprises
This project is a part of the [Galvanize Alumni Relations](http://glavanize.com) at [Galvanize Datathon 2020 Blog](https://blog.galvanize.com/alumni-datathon-digging-into-the-election/). This project can be found at the [main GitHub repo](https://github.com/yuchild/galvanize_datathon2020).

#### -- Project Status: [Active]

## Project Description
The purpose of this project is use Twitter data from 3 days 30th September, 1st of October, and 2nd of October 2020 to provide three tiers of analysis.

  >**First** is a general exploration of data based on Twitter feeds, user characteristics, time series analysis, and natural language processing.

  >**Second** is a sentiment analysis of Twitter feeds funneled into an overall influencer score based on retweets, following, favorited, and other metrics. This analysis will then be rolled into regression model targeting user characteristics with the influencer score.

  >**Third** is a live web dashboard centered around a map data of states with metrics

### Partners
* Mathias Darr, Data Scientist and Data Engineer, web app ninja
* Julia Sokolova, Data Scientist and Project Manager Queen Bee, sentiment analyst and modeler extraordinaire
* David Yu, Data Scientist EDA Guru and bookworm for data

### Methods Used
* Inferential Statistics
* Machine Learning
* Data Visualization
* Predictive Modeling
* etc.

### Technologies
* Python
* Pandas, jupyter
* S3
* EC2
* PostGres, MySql
* HTML
* JavaScript
* etc.

## Needs of this project

- frontend developers
- data exploration/descriptive statistics
- data processing/cleaning
- statistical modeling
- writeup/reporting
- etc. (be as specific as possible)

## Getting Started

1. Clone this repo (for help see this [Readme](https://github.com/yuchild/galvanize_datathon2020/blob/main/README.md)).
2. Raw Data is being kept offline due to size considerations. Do get started do the following:

    Data Source: [GitHub Repo link provided @12PM Friday 10/29/2020]
    Clone [GitHub Repo link provided @12PM Friday 10/29/2020]
    Follow the instructions in the repository to install twarc and tqdm.
    Apply for a twitter developer account.
    Save api key, save api secret key, save bearer token.
    Enter your twitter api information into twarc.
    Use a mv command to move the contents of the desired days into a new single directory.
    Look inside the cloned repository for the appropriate .txt files containing tweet ids. (ex. cat * >>
    file name.txt)
    Concatenate those files into one file.
    In the terminal, use awk 'NR % 100 == 0' <file.txt> > <result.txt> to systematically sample every
    100th tweet id. These are the tweets you will hydrate.
    Modify the hydrate.py script in the cloned repository and run the script to rehydrate tweets from your file of tweet ids.
    Analyze tweets.

3. Data processing/transformation scripts are being kept [here](https://github.com/yuchild/galvanize_datathon2020/commit/14bf75445630b26fb33ac53e685442f1e6c846e4)
4. etc...
5. Follow setup [instructions](Link to file)

## Featured Notebooks/Analysis/Deliverables
* [EDA Notebook](https://github.com/yuchild/galvanize_datathon2020/blob/main/eda.ipynb)
* [Modeling Notebook](https://github.com/yuchild/galvanize_datathon2020/blob/main/Datathon%20-%20Sentiment%20Analysis%20%26%20Data%20Cleanup.ipynb)
* [Live Web Dashboard](link)


## Contributing Members

**Team Leads (Contacts) : [Julia Sokolova](https://github.com/JuliaSokolova)**

#### Other Members:

| **Name** | **Slack Member ID** |
|---------|-----------------|
|[Mathias Darr](https://github.com/MathiasDarr)| U01DGT9BYJE |
|[David Yu](https://github.com/yuchild) | U01DFNWBMNX |

## Contact
* If you haven't joined the Galvanize, [you can do that here](https://www.galvanize.com/).  
* Our slack channel is private because of Datathon rules
* Feel free to contact team leads with any questions or if you are interested in contributing!
