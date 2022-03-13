from jinja2 import Template
import base64
import requests
from github import Github
from github import InputGitTreeElement
import sys
import jenkins
import mysql.connector
from sonarqube import SonarQubeClient

class Jenkins:

    def __init__(self, jobname,token,repo,branch,build,deploy,jenkins_username,jenkins_password,stack):
        self.jobname = jobname
        self.token = token
        self.repo = repo
        self.branch = branch
        self.build = build
        self.deploy = deploy
        self.jenkins_username = jenkins_username
        self.jenkins_password = jenkins_password
        self.stack =  stack
    
    def sonar_automation(self):
        sonar = SonarQubeClient(sonarqube_url="http://104.198.141.127:9000", username=self.jenkins_username, password=self.jenkins_password)
        repository=self.repo
        repo = repository.split('/')
        repo_name = repo[1]
        try:
          sonar.projects.create_project(project="Bala", name="Bala", visibility="private")
          sonar.webhooks.create_webhook(name= repo_name,
                                           project= repo_name,
                                           url="http://34.102.134.5:8080/sonarqube-webhook/",
                                           secret=self.jenkins_password)
        except:
          print("Repo or WebHook already exist")
               

    def sql_insert_data(self):
        cnx = mysql.connector.connect(user='root', password=self.jenkins_password,
                                      host='34.70.1.185',database='metrics')
        cursor = cnx.cursor()
        add_app = ("INSERT INTO main "
                   "(APP_NAME, BUILD_TYPE, DEPLOY_TYPE, JENKINS_JOB_NAME )"
                   "VALUES (%(repo)s, %(build)s, %(deploy)s, %(jobname)s )")
        data_app = {
            'repo': self.repo,
            'build': self.build,
            'deploy': self.deploy,
            'jobname': self.jobname
        }
        cursor.execute(add_app, data_app)
        cnx.commit()
        cnx.close()
        self.sonar_automation()

    def jenkins_pipeline(self):
        Config_xml = open("config.xml", "r")
        data = Config_xml.read()
        Config_xml.close()
        server = jenkins.Jenkins('http://34.102.134.5:8080/',username=self.jenkins_username,password=self.jenkins_password)
        server.create_job(self.jobname, data)
        print('Jenkins Pipeline created sucessfully with url:' + " " + "http://34.102.134.5:8080/job/" + self.jobname + "/")
        self.sql_insert_data()

    def github(self):
        user = "bala280597"
        password = self.token
        g = Github(user, password)
        repo = g.get_repo(self.repo)
        file_list = [
            'Jenkinsfile'
        ]
        file_names = [
            'Jenkinsfile'
        ]
        commit_message = 'Jenkins file added '
        master_ref = repo.get_git_ref(self.branch)
        master_sha = master_ref.object.sha
        print(master_sha)
        base_tree = repo.get_git_tree(master_sha)
        element_list = list()
        for i, entry in enumerate(file_list):
            with open(entry) as input_file:
                data = input_file.read()
            element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
            element_list.append(element)
        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
        self.jenkins_pipeline()

    def template(self):
        with open('Jenkinsfile.jinja2') as file_:
            template = Template(file_.read())
        repository=self.repo
        repo = repository.split('/')
        repo_owner = repo[0]
        repo_name = repo[1]
        render_file = template.render(BUILD_TYPE=self.build, DEPLOY_TYPE=self.deploy, REPO=repo_name, STACK=self.stack)
        f = open("Jenkinsfile", "w")
        f.write(render_file)
        f.close()
        with open('config.xml.jinja2') as configfile_:
            config_template = Template(configfile_.read())
        config_render_file = config_template.render(REPO_NAME=repo_name, REPO_OWNER=repo_owner)
        f = open("config.xml", "w")
        f.write(config_render_file)
        f.close()
        self.github()

if __name__ == '__main__':
    token = sys.argv[1]
    repo = sys.argv[2]
    branch = sys.argv[3]
    build = sys.argv[4]
    deploy = sys.argv[5]
    jobname = sys.argv[6]
    jenkins_username = sys.argv[7]
    jenkins_password = sys.argv[8]
    stack = sys.argv[9]
    
    job_automation = Jenkins(jobname,token,repo,branch,build,deploy,jenkins_username,jenkins_password,stack)
    job_automation.template()
