# Hadoop
## TABLE OF CONTENTS
<!-- TOC -->


* [Functionalities](###FUNCTIONALITIES-)

<!-- TOC -->


### FUNCTIONALITIES:
- #### EXTRACT DATASETS:
    ##### Gathering the datasets for analyzing and meeting our project goals,we follow the following path:
  - The data dump is composed of a set of XML files compacted with
  the .7z extension.
  - Even after compacting the biggest file has 18GB of data.
  - If we extract this file, it would be around 92GB,which is not easy
  to handle with a local machine.
  - We are using python to extractthe subset of around 6GBand
  prepare data for our analysis. Code for the same can be found on
  GitHub link:
  https://github.com/santoshburada/Hadoop/tree/main/Data-Extraction
  - Schema of the dataset can be viewed on belowlink:
  https://data.stackexchange.com/stackoverflow/query/472607/
  information-schema-for-a-table?table=posts#resultSets
- #### PREPARING DATASETS:
  - We are converting the data from XML to Dataframe and from
  dataframe to parquetfile format. Code for the same can be found
  in file prepare_data.py under the belowlink:
  https://github.com/santosh-burada/Hadoop
3. ANALYSIS:
Reading the Paraquetformat and running spark scriptto
perform analysis, such as:
• Number of questions in the dataset
• Number of answers in dataset
• Distinct number of users
• Questionswhich are answered
• Most viewed questions
• Computing the response time to getthe answer for
questions.
• Computing hourly data (per hour how many questions got
answered)
• Time evaluation of number of questions and answers.
• Computing number oftags
• Getting the most popular tags based on their frequency.
ARCHITECTURE AND DESIGN:
TECHNOLOGIES:
Ø Spark 2.4 – An open-source unified analytics engine for analyzing enormous
amounts of data is Apache Spark. An interface called Spark allows clusters
to be programmed with implicit data parallelism and fault tolerance.
Ø Cloudera Manager – A complete application for managing CDH clusters is
Cloudera Manager. Every component of the CDH cluster can be seen and
controlled precisely with the help of Cloudera Manager, enabling
administrators to lower expenses while increasing compliance and
performance.
Ø Spark SQL – A Spark module for processing structured data is Spark SQL. It
offers the Data Frame programming abstraction and functions as a
distributed SQL query engine. It makes Hadoop Hive queries that aren't
updated execute up to 100 times quicker on current deployments and data.
Ø HDFS - The main data storage system utilized by Hadoop applications is the
Hadoop Distributed File System (HDFS). To construct a distributed file
system that offers high-performance access to data across extremely
scalable Hadoop clusters, HDFS uses a NameNode and DataNode
architecture.
Ø YARN – Big data applications use the large-scale, distributed operating
system YARN. One of the core components of Hadoop 2, the open-source
distributed processing framework developed by the Apache Software
Foundation, the technology is intended for cluster administration.
Ø HUE - Hue is an open-source SQL Assistant for collaborating and querying
databases and data warehouses. Its objective is to increase the use of selfservice data querying within businesses. On their website, the Hue team
posts releases.
Ø XML (Extensible Markup Language) - A tool for storing and transferring data
that is independent of hardware and software is XML. XML stands for
eXtensible Markup Language. Like HTML, XML is a markup language. XML
was created to store and move data. XML was intended to be selfexplanatory.
Ø Cloud (GCP) – GCP is abbreviated as Google Cloud Platform. A provider of
computer resources for creating, installing, and running Web applications is
Google Cloud (sometimes referred to as Google Cloud Platform or GCP).
Ø PARQUET - One of the quickest file formats to read from is the open-source
Parquet format. The data is saved per column as opposed to just per row
because it is a column-oriented file format. The parquet files are structured
and contain the column schema, making them suitable for direct import into
a database or data warehouse.
GITHUB LOCATION OF CODE:
https://github.com/santosh-burada/Hadoop
DEPLOYMENT INSTRUCTIONS:
Deployment Instruction for Stand Alone:
Ø Download Spark executable from below link and install it:
https://spark.apache.org/downloads.html
Ø Set User Environment Variable: SPARK_HOME: C:\Spark\spark-3.1.3-binhadoop2.7
Ø Create an entry under path variable as: %SPARK_HOME%\bin.
Ø Set User Environment Variable: JAVA_HOME:
C:\Softwares\Java\jdk1.8.0_333
Ø Create an entry under path variable as: %JAVA_HOME%\bin.
Ø Install pyspark using command: pip install pyspark.
Deployment Instruction for Core Cluster using Cloudera Manager:
Ø Create a GCP account.
Ø Enable VM instance API: API & Services -> Enable API & Services -> First time
it will ask to enable VM Instances
Ø An VM instance will be created under Compute Engine -> VM Instances
Ø Go to Create Instance (this will be our master node) -> Here specify the
configuration for Image:
• Name: User Defined
• Region and Zone: Location near to User as per requirement
• Machine configuration: N1
• Machine Type: n1-standard-4 (we can choose this as per project
requirement, in our case we are handling huge amount of data, so we
chose 4 virtual CPUs)
• Change Boot disk configuration: (User centric)
• Operating System: CentOS
• Boot Disk Type: Standard Persistent disk
• Allow Firewall: Allow HTTP traffic and Allow HTTPS traffic, in order to
access Cloudera Manager UI.
• Advanced options: Not required in our case.
• Create instance by clicking on "create.”
Ø Connect to the newly created instance through SSH.
Ø Follow below link to configure cluster which is suitable to run Cloudera
Manager
Ø Create new machine image (click on three dots highlighted in image)
• you can find created image under Compute Engine -> Machine Image
• we will use this image to create our data nodes by following below steps:
Ø clicking on 'Create Instances' on top of "VM instances" page.
Ø Choose option "New VM Instance from Machine image.”
Ø Choose a newly created machine image. Repeat this process to create as
much as data nodes needs to be created (we created three)
Ø Connect to the created nodes using SSH and follow the below steps in sudo
mode to make an entry for all your servers in /etc/hosts:
# vi /etc/hosts
10.168.0.8 cloudera-manager.us-west2-a.c.light-processor-366800.internal clouderamanager
10.138.0.8 datanode-1.us-west1-b.c.light-processor-366800.internal datanode-1
10.182.0.16 datanode-2.us-west4-b.c.light-processor-366800.internal datanode-2
10.180.0.2 datanode-3.us-west3-a.c.light-processor-366800.internal datanode-3
Ø Connect to Master Node using SSH and login as a root user (sudo) and
execute the commands below.
Ø Now copy the id_rsa.pub from master vm to all other data node vm
Ø Follow the below commands in master vm to do above process.
Ø Download the latest Cloudera Manager using below link:
Ø After downloading, we will get a bin file (cloudera-manager-installer.bin).
User must give execute permission for this file, run the below command to
do so:
Ø Next step is to run below command to install Cloudera Manager in Master
Node:
Ø After installing Cloudera Manager Successfully access the Cloudera Manager
UI using below format
copy external Ip address of master node (refer screenshot) and use the port
7180 to access Cloudera Manager: <External Ip address>:7180.
ssh-keygen -t rsa
ssh-copy-id -i ~/.ssh/id_rsa.pub root@datanode-1.us-central1-c.c.light-processor-366800.internal
ssh-copy-id -i ~/.ssh/id_rsa.pub root@datanode-2.us-central1-c.c.light-processor-366800.internal
ssh-copy-id -i ~/.ssh/id_rsa.pub root@datanode-3.us-central1-c.c.light-processor-366800.internal
wget https://archive.cloudera.com/cm7/7.4.4/cloudera-manager-in
chmod u+x cloudera-manager-installer.bin
sudo ./cloudera-manager-installer.bin
Ø Below is a screenshot to configure the cluster.
Deployment Instruction for One Click Cluster:
Ø From the hamburger icon choose Datarproc
Ø Create Cluster by clicking “Create Cluster” button and select “Cluster on
Computer Engine.”
Ø Select below configuration:
• Cluster Name and Location: User Defined
• Cluster type: Standard (1 master, N workers)
• Choose Image Version: 1.5 (Ubuntu 18.04 LTS, Hadoop 2.10, Spark 2.4)
• Components: Check Enable component gateway.
• Optional components:
ü Anaconda
ü Jupyter Notebook
ü HBase
STEPS TO RUN THE APPLICATION:
Ø Download PrepareData.py from GitHub and upload to master node (refer
GitHub for detailed explanation)
Ø Run below command to run:
spark-submit --packages com.databricks:spark-xml_2.11:0.4.1
PrepareData.py
Ø This will create a paraquet file in Hadoop file system.
Ø After preparing the data, start analyzing by running analysis.py. Follow the
below steps to do so:
Ø Download analysis.py from GitHub and upload to master node (refer GitHub
for detailed explanation). Run below command to run:
spark-submit analysis.py.
Ø You can see the output in the console.
Ø Ways to access files with different storage:
• from local: r'file:///<Absolute path to the file>'
(r'file:///C:/Users/Saloni.modi/Documents/SparkProject/input/Posts.
xml')
• from GCP bucket: gs://<bucketName>/<filename>
(gs://sparkbucketsod/Posts.xml)
• from Hadoop file system: /<path till file in Hadoop><name of file>
(/HBase/wordcount.txt)
Ø We can use the above URLs to access the file required to run our script. We
uploaded data in Hadoop file System using Cloudera Manager HBase.
TEST RESULTS:
Test results can be found on below GitHub link:
https://github.com/santosh-burada/Hadoop/blob/main/output.txt