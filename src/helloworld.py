from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import background_thread
import thread
import time
import logging

'''class Constants():
    
    DELAY = 5
    JOB_COMPLETE_TIME = 10'''

class Job(db.Model):
    
    progress = db.IntegerProperty(default = 0)
    time_started = db.DateTimeProperty(auto_now_add = True)
    completed = db.BooleanProperty(default = False)

def run_thread(identity):
    job = Job.get_by_id(identity)
    while job.progress < 10:#Constants.JOB_COMPLETED_TIME:
        time.sleep(2)
        job.progress += 1
        job.put()
    job.completed = True
    job.put()
        
def run_it(identity):
        
    thread.start_new_thread(run_thread, (identity,))
    
class UploadPage(webapp.RequestHandler):
    
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #jobs =  {'jobs': db.GqlQuery("SELECT * FROM Job")}
        self.response.out.write(template.render('upload_page.html', {}))
    
    def post(self):
        
        job = Job()
        job.put()
        
        #t = background_thread.BackgroundThread(target= run_thread, args=[job.key().id(),])
        #t.start()
        run_it(job.key().id())
        self.redirect('/progress')

class ProgressPage(webapp.RequestHandler):
    
    def get(self):
        
        self.response.out.write(template.render('progress_page.html', {}))
                 
class Results(webapp.RequestHandler):
    
    def get(self):
        
        jobs =  {'jobs': db.GqlQuery("SELECT * FROM Job")}
        self.response.out.write(template.render('results.html', jobs))
        
class DownloadPage(webapp.RequestHandler):
    
    def get(self):
        
        jobs = {'jobs': db.GqlQuery("SELECT * FROM Job WHERE completed = TRUE")}
        self.response.out.write(template.render('download.html', jobs))
        
application = webapp.WSGIApplication([('/', UploadPage),('/results', Results),('/progress',ProgressPage),('/download',DownloadPage)], debug=True)
upload_url = blobstore.create_upload_url('/upload')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
