from pyspark.sql.functions import (
    col, count, desc, explode, ceil, unix_timestamp, window, sum, when, array_contains, lit, split, to_utc_timestamp,

)
from pyspark.sql import SparkSession
import io
from contextlib import redirect_stdout

f = io.StringIO()
with redirect_stdout(f):
    spark = SparkSession.builder.appName("PreparePostsCSV").getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "America/Los_Angeles")
    posts_path = r'C:\Users\Santosh_Burada\PycharmProjects\hadoop\data\posts_all_10000'

    posts_all = spark.read.parquet(posts_path)

    print("===========Schema of Posts DataFrame============")
    posts_all.printSchema()

    posts = posts_all.select(
        'Id',
        'PostTypeId',
        'AcceptedAnswerId',
        'ViewCount',
        'Title',
        'OwnerUserId',
        'CreationDate',
        'Tags',
        'AnswerCount'
    ).cache()
    print("++++++++++++++++++++++++++++++Compute the counts+++++++++++++++++++++++++++++++++++++++++++++++++")

    questions = posts.filter(col('PostTypeId') == 1)
    answers = posts.filter(col('PostTypeId') == 2)

    print("Number of Question in Posts Dataset: ", questions.count())
    print("Number of Answers in Posts Dataset: ", answers.count())
    print("Distinct Number Of Users In Posts Dataset",
          posts.filter(col('OwnerUserId').isNotNull()).select('OwnerUserId').distinct().count())
    AnsweredQuestions = questions.filter(col('AcceptedAnswerId').isNotNull())
    print("Questions which are answered", AnsweredQuestions.count())

    Most_viewd = questions.filter(
        col('ViewCount') == (questions.agg({"ViewCount": "max"}).collect()[0])["max(ViewCount)"])
    Most_viewd.show(truncate=False)

    print("=============================Compute the response time====================================================")
    response_time = (
        AnsweredQuestions.alias('questions')
        .join(answers.alias('answers'), col('questions.AcceptedAnswerId') == col('answers.Id'))
        .select(
            col('questions.Id'),
            to_utc_timestamp(col('questions.CreationDate'), "America/Montreal").alias('question_time'),
            to_utc_timestamp(col('answers.CreationDate'), "America/Montreal").alias('answer_time')
        )
        .withColumn('response_time',
                    unix_timestamp(to_utc_timestamp('answer_time', "America/Los_Angeles")) - unix_timestamp(
                        to_utc_timestamp('question_time', "America/Los_Angeles")))
        .filter(col('response_time') > 0)
        .orderBy('response_time')
    )

    response_time.show(response_time.count(), False)
    print("==============================hourly_data========================================")
    hourly_data = (
        response_time
        .withColumn('hours', ceil(col('response_time') / 3600))
        .groupBy('hours')
        .agg(count('*').alias('cnt'))
        .orderBy('hours')
        .limit(24)
    )
    hourly_data.show(hourly_data.count(), False)

    print("==================The time evolution of the number of questions and answeres====================")
    posts_grouped = (
        posts
        .filter(col('OwnerUserId').isNotNull())
        .groupBy(
            window('CreationDate', '1 week')
        )
        .agg(
            sum(when(col('PostTypeId') == 1, lit(1)).otherwise(lit(0))).alias('questions'),
            sum(when(col('PostTypeId') == 2, lit(1)).otherwise(lit(0))).alias('answers')
        )
        .withColumn('date', col('window.start').cast('date'))
        .orderBy('date')
    )

    posts_grouped.show(posts_grouped.count(), False)

    print("=============Compute number of tags===============")
    #
    tags = (
        questions
        .select('Id',
                'PostTypeId',
                'AcceptedAnswerId',
                'ViewCount',
                'OwnerUserId',
                'CreationDate',
                'Tags',
                'AnswerCount')
        .withColumn('tags', split('tags', '><'))
        .selectExpr(
            '*',
            "TRANSFORM(tags, value -> regexp_replace(value, '(>|<)', '')) AS tags_arr"
        ).withColumn('tags_arr', col('tags_arr')[0])
    )
    tags.show(n=100, truncate=False)

    #
    print("==========See most popular tags============")
    #
    (
        questions
        .withColumn('tags', split('tags', '><'))
        .selectExpr(
            '*',
            "TRANSFORM(tags, value -> regexp_replace(value, '(>|<)', '')) AS tags_arr"
        )
        .withColumn('tag', explode('tags_arr'))
        .groupBy('tag')
        .agg(count('*').alias('tag_frequency'))
        .orderBy(desc('tag_frequency'))
    ).show(n=10)

    print("===========See the popularity of some tags============")

    spark_tag = (
        questions
        .withColumn('tags', split('tags', '><'))
        .selectExpr(
            '*',
            "TRANSFORM(tags, value -> regexp_replace(value, '(>|<)', '')) AS tags_arr"
        )
        .select('Id', 'CreationDate', 'tags_arr')
        .filter(array_contains(col('tags_arr'), 'apache-flex') | array_contains(col('tags_arr'),
                                                                                'apache-spark-sql') | array_contains(
            col('tags_arr'), 'apache'))
        .groupBy(
            window('CreationDate', "1 week")
        )
        .agg(
            count('*').alias('tag_frequency')
        )
        .withColumn('date', col('window.start').cast('date'))
        .orderBy('date')
    )
    spark_tag.show(n=100, truncate=False)

file = open("output.txt", "w")

# file = open('gs://dataproc-staging-us-central1-291378718946-mvsxebny/notebooks/jupyter/output.txt', 'w')
out = f.getvalue()

file.writelines(out)

