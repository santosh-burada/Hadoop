"""
  spark-submit --packages com.databricks:spark-xml_2.11:0.4.1 prepare_data.py

"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *
import xml.etree.ElementTree as ET
import re


# extract the values in each xml row
def processXmlFields(string):
    # function to extract filed and data. will be used with map function

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

    if lasteditdate is None:
        lasteditdate = creationdate

    return (
        postId, postType, acceptedanswerid, creationdate, score, viewCount, owneruserid, lasteditoruserid, lasteditdate,
        title, lastactivitydate, tags, answercount, commentcount, favoritecount)


def main():
    # creating Spark Context
    spark = SparkSession.builder.appName("PreparePostsFor Analysis").getOrCreate()
    # setting max portion size
    spark.conf.set('spark.sql.files.maxPartitionBytes', '1073741824')
    # reading the xml file. To do this we need extra spark package called com.databricks.spark.xml.XmlInputFormat.
    """
    Below is the function definition of newAPIHadoopFile
    newAPIHadoopFile(self,
                     path: str,
                     inputFormatClass: str,
                     keyClass: str,
                     valueClass: str,
                     keyConverter: Optional[str] = None,
                     valueConverter: Optional[str] = None,
                     conf: Optional[Dict[str, str]] = None,
                     batchSize: int = 0) -> RDD[Tuple[T, U]]
    """
    xml_posts = spark.sparkContext.newAPIHadoopFile(
        # "gs://dataproc-staging-us-central1-291378718946-mvsxebny/notebooks/jupyter/test.xml",(reading from gcp cloud storage)
        r'C:\Users\Santosh_Burada\PycharmProjects\hadoop\data\posts_10000000.xml',
        'com.databricks.spark.xml.XmlInputFormat',
        'org.apache.hadoop.io.Text', 'org.apache.hadoop.io.Text',
        conf={'xmlinput.start': '<row', 'xmlinput.end': '/>'})

    # applying map on xml posts
    each_post = xml_posts.map(lambda x: x[1])

    # from each post we are extracting the fields with data
    post_fields = each_post.map(processXmlFields)

    # Creating schema for our final Data Frame
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

    # creating data frame.
    postDF = spark.createDataFrame(post_fields, questionsSchema)

    # saving the dataframe in PARQUET formate
    postDF.write.format('parquet').options(header='false').save(
        r"C:\Users\Santosh_Burada\PycharmProjects\hadoop\data\posts_10000000")


if __name__ == "__main__":
    main()
