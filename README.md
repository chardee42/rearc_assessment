
# README

I started with reading the instructions a few times to fully grasp the requirements and how they fit together. 

Then I did some preliminary web research on things like copying files with Lambda, AWS CDK using Python, and more. 
I was mainly trying to wrap my brain around the project and fill in any gaps. I like to understand most if not all of the project and get an overview of what I need to do.

During this time, I’m also starting to build my tech stack in my head trying to decide the best tools to use to get this done. For example, do I want to run the code from my machine or should I store it all in AWS.


## Part 1: AWS S3 & Sourcing Datasets

Set up an S3 bucket called rearc-chardee-project.

s3://rearc-chardee-project/bls-data/

Source: https://github.com/chardee42/rearc_assessment/blob/main/lambda_function_copy_bls.py

On my laptop, I wrote a script that downloads the files to my local computer.

I then researched and coverted it to a Lambda script making the following changes:

- Changed it from writing to local files to writing to S3



Created a deployment package that included Beautiful Soup

- Created zip file

   - pip install requests beautifulsoup4 -t .

   - Used this command in PowerShell since Windows 11 Personal does not have zip

      - Compress-Archive -Path .\\\* -DestinationPath .\\lambda\_[package.zip] -CompressionLevel Optimal

      - This should be ran from the package directory

- Uploaded zip file to Lambda



With some tweaking (found a few typos), I was able to get the lambda function to run.

Used the IAM role giving it permissions to my S3 test environment: lambda-bls-s3-role



*Note: My AWS account is for learning purposes and only contains publicly available data, so I haven’t tried to lock it down in IAM.*





## Part 2: APIs
Event name: event_api_call

I had a template for API calls in my code snippets collection, so used that as a base template and modified it.



Built new zip file using:

pip install requests -t .

zipped up contents and uploaded them to AWS.






## Part 3: Data Analytics

I chose SageMaker because I wanted to use PySpark but also wanted to have full access to visualizations.

Got SageMaker working on my instance. This required I give special permission to the role to allow it to run with AWS Glue. 

Select PySpark Glue Notebook.

Please see .ipynb file for details and results



## Part 4: AWS CDK

*This code was generated with ChatGPT*

I don’t have much experience with AWS CDK, so I asked ChatGPT to create a base template I could modify to create the Amazon CDK.

Full disclosure: ChatGPT wrote most of this code. It also suggested I add code for third lambda script so I used it.





## Project Areas of Improvement

Improve the presentation of analysis

- Add more visualizations

Update the file location for Lambda functions that pull data from BLS and the API.

Test and optimize the AWS CDK



## My Areas of Improvement

I need to spend more time with AWS CDK creating and optimizing scripts.


