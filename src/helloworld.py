from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext import blobstore
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
        
class MainPage(webapp.RequestHandler):
    
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        jobs =  {'jobs': db.GqlQuery("SELECT * FROM Job")}
        self.response.out.write(template.render('main2.html', jobs))
    
    def post(self):
        
        job = Job()
        job.put()
        try:
            thread.start_new_thread(run_thread, (job.key().id(),))
        except:
            logging.info("Unable to create Thread")
        #self.redirect('/')

class Results(webapp.RequestHandler):
    
    def get(self):
        
        jobs =  {'jobs': db.GqlQuery("SELECT * FROM Job")}
        self.response.out.write(template.render('results.html', jobs))
        
application = webapp.WSGIApplication([('/', MainPage),('/results', Results)], debug=True)
upload_url = blobstore.create_upload_url('/upload')

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
