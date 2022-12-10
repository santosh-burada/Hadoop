"""
  spark-submit --packages com.databricks:spark-xml_2.11:0.4.1,com.databricks:spark-csv_2.11:1.5.0 prepare_data_posts_all_csv.py

"""
import pyspark
import pyspark.sql
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import xml.etree.ElementTree as ET
import re
import sys
import time
import datetime
import csv


# extract the values in each xml row
def processXmlFields(string):
    elements = ET.fromstring(string.encode('utf-8')).attrib

    postId = elements.get("Id")
    postType = elements.get("PostTypeId")
    acceptedanswerid = elements.get("AcceptedAnswerId")
    creationdate = elements.get("CreationDate")
    score = elements.get("Score")
    viewCount = elements.get("ViewCount")
    owneruserid = elements.get("OwnerUserId")
    lasteditoruserid = elements.get("LastEditorUserId")
    lasteditdate = elements.get("LastEditDate")
    title = elements.get("Title")
    lastactivitydate = elements.get("LastActivityDate")
    tags = re.findall(r'[\w.-]+', elements.get("Tags", ""))
    answercount = elements.get("AnswerCount")
    commentcount = elements.get("CommentCount")
    favoritecount = elements.get("FavoriteCount")

    if lasteditdate == None:
        lasteditdate = creationdate

    return (
        postId, postType, acceptedanswerid, creationdate, score, viewCount, owneruserid, lasteditoruserid, lasteditdate,
        title, lastactivitydate, tags, answercount, commentcount, favoritecount)


def main():
    spark = SparkSession.builder.appName("PreparePostsCSV").getOrCreate()
    spark.conf.set('spark.sql.files.maxPartitionBytes', '1073741824')
    xml_posts = spark.sparkContext.newAPIHadoopFile(
        "gs://dataproc-staging-us-central1-291378718946-mvsxebny/notebooks/jupyter/test.xml",
        'com.databricks.spark.xml.XmlInputFormat',
        'org.apache.hadoop.io.Text', 'org.apache.hadoop.io.Text',
        conf={'xmlinput.start': '<row', 'xmlinput.end': '/>'})
    each_post = xml_posts.map(lambda x: x[1])
    post_fields = each_post.map(processXmlFields)

    questionsSchema = \
        StructType([
            StructField("Id", StringType()),
            StructField("PostTypeId", StringType()),
            StructField("AcceptedAnswerId", StringType()),
            StructField("CreationDate", StringType()),
            StructField("Score", StringType()),
            StructField("ViewCount", StringType()),
            StructField("OwnerUserId", StringType()),
            StructField("LastEditorUserId", StringType()),
            StructField("LastEditDate", StringType()),
            StructField("Title", StringType()),
            StructField("LastActivityDate", StringType()),
            StructField("Tags", StringType()),
            StructField("AnswerCount", StringType()),
            StructField("CommentCount", StringType()),
            StructField("FavoriteCount", StringType())])

    postDF = spark.createDataFrame(post_fields, questionsSchema)

    postDF.write.format('parquet').options(header='false').save(
        "gs://dataproc-staging-us-central1-291378718946-mvsxebny/notebooks/jupyter/data-large/posts")


if __name__ == "__main__":
    main()
