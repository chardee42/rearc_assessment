
# README

I started with reading (and re-reading) the requirements to fully grasp how the sections fit together. 

During this time, I also started to build my tech stack in my head trying to decide the best tools to use. 

***

## Part 1: AWS S3 & Sourcing Datasets

I set up an S3 bucket called **rearc-chardee-project**.

Here is the link to both files we used in the bucket:

API data:
https://rearc-chardee-project.s3.us-east-1.amazonaws.com/api_out.json

BLS data:
https://rearc-chardee-project.s3.us-east-1.amazonaws.com/bls-data/pr.data.0.Current

### Created Lambda function bls_data
This function downloaded the files into the S3 bucket.

Source: https://github.com/chardee42/rearc_assessment/blob/main/lambda_function_copy_bls.py

As part of this process, I created a deployment package that included Beautiful Soup and requests.

- Created zip file for deployment to Lambda

   - pip install requests beautifulsoup4 -t .
   -    This downloaded the required files to my local machine.

   - Used this command in PowerShell since Windows 11 Personal does not have zip

      - Compress-Archive -Path .\\\* -DestinationPath .\\lambda\_[package.zip] -CompressionLevel Optimal

      -    This command should be ran from the package directory

- Uploaded zip file to Lambda

Used the IAM the following role, giving it permissions to my S3 test environment: lambda-bls-s3-role


*Note: My AWS account is for learning purposes and only contains publicly available data. For this reason, I haven’t tried to lock it down in IAM.*


***


## Part 2: APIs
### Created lambda function event_api_call

Source: https://github.com/chardee42/rearc_assessment/blob/main/lambda_function_get_api.py

I had a template for API calls in my code snippets collection, so I used that as a base and modified it.



Built new zip file for distribution to lambda using:

- pip install requests -t .

- zipped up contents and uploaded them to AWS.



***


## Part 3: Data Analytics

Source: https://github.com/chardee42/rearc_assessment/blob/main/analysis.ipynb

I chose SageMaker because I wanted to use PySpark but also wanted to have full access to visualizations.

I got SageMaker working on my instance. This required that I give it special permission to the role to allow it to run with AWS Glue. 

Selected PySpark Glue Notebook.

Please see .ipynb file for details and results


***

## Part 4: AWS CDK

Source: https://github.com/chardee42/rearc_assessment/blob/main/rearc-cdk.py

*This code was generated with ChatGPT.*

I asked ChatGPT to create a base template so I could modify to create the Amazon CDK.

It also suggested that I add a third lambda function for reporting.

Source: https://github.com/chardee42/rearc_assessment/blob/main/lambda_function_reports.py




***


## Areas of Improvement

### Project

- Improve the presentation of analysis

   - Add more visualizations

- Test and optimize the AWS CDK



### Personal Knowledge

- I need to spend more time with AWS CDK, creating and optimizing scripts.


