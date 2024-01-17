from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from data_matching import jaccard_similarity

# Create a Spark session
spark = SparkSession.builder.appName("DataClustering").getOrCreate()

# ss
# Load CSV files into DataFrames
file1_path = "./data/ACM_1995_2004.csv.csv"
file2_path = "./data/DBLP_1995_2004.csv.csv"

df1 = spark.read.csv(file1_path, header=True, inferSchema=True)
df2 = spark.read.csv(file2_path, header=True, inferSchema=True)

# Blocking based on a common attribute like 'year'
blocked_data = df1.join(df2, df1['year'] == df2['year'], 'inner')

jaccard_similarity_udf = spark.udf.register("jaccard_similarity", jaccard_similarity)
matched_pairs = blocked_data.filter(jaccard_similarity_udf(blocked_data['authors'], blocked_data['authors']) >= 0.9)

# Clustering using KMeans (example)
feature_cols = ['year']
vector_assembler = VectorAssembler(inputCols=feature_cols, outputCol='features')
vectorized_data = vector_assembler.transform(matched_pairs)

kmeans = KMeans(featuresCol='features', predictionCol='cluster', k=3)
model = kmeans.fit(vectorized_data)
clustered_data = model.transform(vectorized_data)

# Show the resulting clusters
clustered_data.select('id', 'title', 'year', 'cluster').show()
