# Hadoop One-Click Cluster

## Pros:
- Easy to set up environments.
- Cluster infrastructure can be implemented.
- Since everything is taken care of by pre-made architecture, we can focus on logic.
## Cons:
- Since everything is pre-configured, it is difficult to get an
understanding of inner architecture.
- Cost money.
- GCP will not allow continuous connection with MasterNode, so inorder to run the application we need to submit spark jobs, which prevents customization of Cluster.

## Deployment

- In Gcp navigate to "DataProc" service and enable the API if not.

- Create Cluster by clicking “Create Cluster” button and select “Cluster on Computer Engine.”
- Select below configuration:
  - Cluster Name and Location: User Defined
  - Cluster type: Standard (1 master, N workers)
  - Choose Image Version: 1.5 (Ubuntu 18.04 LTS, Hadoop 2.10, Spark 2.4)
  - Components: Check Enable component gateway.
  - Optional components:
    - Anaconda
    - Jupyter Notebook
    - HBase