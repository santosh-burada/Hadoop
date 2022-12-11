
# StackOveflow Data Analysis Using Hadoop and Spark

StackOverflow (https://stackoverflow.com/) is the most popular
question and answer website, popular among coders and generate
very huge amounts of data on daily basis. It is an excellent example of
big data. The site’s Data Dump is available online
(https://archive.org/details/stackexchange) and we are using it for
analytics purpose. For this project, we are using a three different
infrastructure that is Stand alone, Custom Cluster with Cloudera and
One-click Cluster.
## Functionalities

- EXTRACT DATASETS
     ##### Gathering the datasets for analyzing and meeting our project goals,we follow the following path:
  - The data dump is composed of a set of XML files compacted with the .7z extension.
  - Even after compacting the biggest file has 18GB of data.
  - If we extract this file, it would be around 92GB,which is not easy  to handle with a local machine.
  - We are using python to extract the subset of around 6GB and prepare data for our analysis. Code for the same can be found on
      GitHub link: https://github.com/santoshburada/Hadoop/tree/main/Data-Extraction
  - Schema of the dataset can be viewed on belowlink:  https://data.stackexchange.com/stackoverflow/query/472607/
- PREPARING DATASETS:
  - We are converting the data from XML to Dataframe and from dataframe to parquetfile format. Code for the same can be found in file prepare_data.py under the belowlink: https://github.com/santosh-burada/Hadoop/blob/main/prepare_data.py
- ANALYSIS:
  - Reading the Paraquetformat and running spark script to perform analysis, such as:
    - Number of questions in the dataset
    - Number of answers in dataset
    - Distinct number of users
    - Questionswhich are answered
    - Most viewed questions
    - Computing the response time to getthe answer for questions.
    - Computing hourly data (per hour how many questions got answered)
    - Time evaluation of number of questions and answers.
    - Computing number oftags
    - Getting the most popular tags based on their frequency.


## Deployments

 - [Standalone](https://github.com/santosh-burada/Hadoop/blob/main/Cluster-Configurations/STANDALONE.md)
 - [Core Cluster](https://github.com/santosh-burada/Hadoop/blob/main/Cluster-Configurations/CORE-CLUSTER.md)
 - [One-Click Cluster](https://github.com/santosh-burada/Hadoop/blob/main/Cluster-Configurations/ONE-CLICK-CLUSTER.md)

