from __future__ import with_statement
from matrix import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import files

import thread
import time
import urllib
import logging

class Job(db.Model):
    
    name = db.StringProperty()
    progress = db.IntegerProperty(default = 0)
    time_started = db.DateTimeProperty(auto_now_add = True)
    completed = db.BooleanProperty(default = False)
    data_file = blobstore.BlobReferenceProperty(required = True)
    output_file = blobstore.BlobReferenceProperty()

def run_thread(identity):
    job = Job.get_by_id(identity)
    # Create the file
    file_name = files.blobstore.create(mime_type='text/plain')
    
    # Open the file and write to it
    with files.open(file_name, 'a') as f:
        #read from data_file
        blob_reader = blobstore.BlobReader(job.data_file)
        value = blob_reader.read()
        
        #multiply
        matrix = str_to_matrix(value)
        while job.progress < 10000:
            #time.sleep(1)
            try:
                matrix = matrix_mult(matrix,matrix)
            except Exception as e:
                logging.info("error: "+str(e))
            job.progress += 1
            job.put()
        
        #write 
        f.write(matrix_to_str(matrix))
    
    # Finalize the file. Do this before attempting to read it.
    files.finalize(file_name)
    
    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(file_name)
    
    job.output_file = blob_key
    job.completed = True
    job.put()
        
def run_it(identity):
        
    thread.start_new_thread(run_thread, (identity,))
    
class UploadPage(webapp.RequestHandler):
    
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #jobs =  {'jobs': db.GqlQuery("SELECT * FROM Job")}
        upload_url = {'upload_url': blobstore.create_upload_url('/upload')}
        self.response.out.write(template.render('upload_page.html', upload_url))
        
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    
    def post(self):
        
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]
        job = Job(data_file = blob_info.key())
        if self.request.get('name') is not None:
            job.name = self.request.get('name')
        else:
            job.name = "Untitled"
        job.put()
        run_it(job.key().id())
        self.redirect('/')
        #self.redirect('/serve/%s' % blob_info.key())
        
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class ProgressPage(webapp.RequestHandler):
    
    def get(self):
        
        self.response.out.write(template.render('progress_page.html', {}))
                 
class Results(webapp.RequestHandler):
    
    def get(self):
        
        jobs =  {'jobs': db.GqlQuery("SELECT * FROM Job ORDER BY time_started")}
        self.response.out.write(template.render('results.html', jobs))
        
class DownloadPage(webapp.RequestHandler):
    
    def get(self):
        
        jobs = {'jobs': db.GqlQuery("SELECT * FROM Job WHERE completed = TRUE ORDER BY time_started")}
        self.response.out.write(template.render('download.html', jobs))
        
application = webapp.WSGIApplication([('/', UploadPage),('/results', Results),('/progress',ProgressPage),
                                      ('/download',DownloadPage), ('/upload', UploadHandler),
                               ('/serve/([^/]+)?', ServeHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
