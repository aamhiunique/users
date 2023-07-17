# users

# Step 1 -Install Serverless framework globally

-> npm install -g serverless

# Step 2 - Check the version and verify installation

-> sls -v

# Step 3 create a serverless project

-> clone you replo from github
-> sls create --template aws-python

# Step 4 configure by below command

serverless config credentials \
 --provider aws \
 --key KEY \
 --secret SECRET

# Step 5 deploy the code

sls deploy

Automate and chill
