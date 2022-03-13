# Jenkins-Automation-Python

| Deployment | Type| Author |
| -------- | -------- |--------|
| Jenkins python Automation |Cloud  | BALAMURUGAN BASKARAN|

# Purpose
The purpose of this project is listed below:
  1) Create Jenkins file at any Github repo from jinja2 template
  2) Create pipeline in jenkins with newly created jenkins file
  3) Data Visualization of CI/CD.

In this project , I automated above 3 steps in single flow using Jenkins

# Jenkins Job with Build Parameters
Create Jenkins pipeline Job and Pass parameters to the job which is supplied as arguments to python script.

![Jenkins Pipeline Job](https://user-images.githubusercontent.com/47313756/155072524-86b0fcdb-10ce-4dda-979f-38cec4959e44.png)

```
pipeline{
    agent any
    environment {
        PAT = credentials('pat')
        jenkins_password = credentials('jenkins_password')
        jenkins_user = credentials('jenkins_username')
    }
    stages{
        stage('Checkout'){
            steps{
                checkout([$class: 'GitSCM',
                branches: [[name: '**']],
                extensions: [],
                userRemoteConfigs: [[
                    credentialsId: 'c94b22eb-6c7d-440b-b468-06679d537899',
                    url: 'https://github.com/bala280597/Jenkins-Automation-Python.git']]])
            }
        }
        stage(" Jenkins file creation "){
          steps {
              script {
                properties([parameters([
            	string(defaultValue: 'bala280597/Nodejs', description: 'Repository Name in Github', name: 'REPO'), 
            	string(defaultValue: 'heads/sample', description: 'Github Branch', name: 'BRANCH'), 
            	choice(choices: ['Docker', 'Maven'], description: 'Type of Build', name: 'BUILD_TYPE'), 
            	choice(choices: ['Kubernetes'], description: 'Type of Deployment', name: 'DEPLOY_TYPE'), 
            	string(defaultValue: 'Sample-test', description: 'Name of Jenkins Job', name: 'JENKINS_PIPELINE_JOB_NAME')
            	])])
              }
                    sh """ 
                           python job.py $PAT ${params.REPO} ${params.BRANCH} ${params.BUILD_TYPE} ${params.DEPLOY_TYPE} ${params.JENKINS_PIPELINE_JOB_NAME} $jenkins_user     $jenkins_password
                  """  
          }
        }
    }
}

```
# Sonar Integration
Sonarqube is integrated to analyze source code.
![image](![image](https://user-images.githubusercontent.com/47313756/158076865-ffa574fe-5330-424e-a6c1-e12e3fee8e7f.png))


# Data Visualization
Hosted SQL Server in Kubernetes cluster as Stateful set and expose it as Load Balancer Service. Data from Jenkins job inserted into MYSQL Database.
Data in Database is visualized in Grafana.

![Grafana](https://user-images.githubusercontent.com/47313756/155077273-a9c50f98-6013-4e30-9203-4cfd64d62e73.png)

