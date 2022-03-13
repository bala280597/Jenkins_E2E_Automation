def sql_insert_data(password,repo,job,build_no,time,table_name):
  cnx = mysql.connector.connect(user='root', password=password,
                                host='34.70.1.185',database='metrics')
  cursor = cnx.cursor()
  add_app = (f"INSERT INTO {table_name} "
             "(APP_NAME,JENKINS_JOB_NAME,BUILD_NUMBER,BUILD_TIME)"
             "VALUES (%(repo)s, %(job)s, %(build_no)s, %(time)s )")
  data_app = {
      'repo': repo,
      'build': job,
      'deploy': build_no,
      'jobname': time
  }
  cursor.execute(add_app, data_app)
  cnx.commit()
  cnx.close()
  self.sonar_automation()

if __name__ == '__main__':
    password = sys.argv[1]
    repo = sys.argv[2]
    job = sys.argv[3]
    build_no = sys.argv[4]
    time = sys.argv[5]
    table_name = sys.argv[6]
    sql_insert_data(password,repo,job,build_no,time,table_name)
   

