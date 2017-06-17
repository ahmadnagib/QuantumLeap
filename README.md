# QuantumLeap

QuantumLeap is a multi-user blog that allows users to create accounts and share their own posts. The application is built using Google App Engine and Jinja templates are used to unify the blog. 

This project is part of Udacity's Full Stack Web Developer Nanodegree Program. A Pyhton class is used from udacity lessons to handle rendering the right Jinja2 template and the passed parameters.

# Documentation

The information related to supported functionalities and how to get started is included in this documentation.

- [Supported Functionalities](#supported-functionalities)
- [Quick Start](#quick-start)
- [What is included](#what-is-included)
- [License](#license)


## Supported Functionalities

QuantumLeap supports creating new account for using the blog. Usernames are unique and a user have to sign-in to enjoy the full functionalities of the blog. All the saved passwords are hashed and user cookies are secured.

A logged-in user can:

- Add a new blog post
- Edit her/his own existing blog posts
- Delete her/his own existing blog posts
- View her/his own existing blog posts
- Like posts of other users
- Comment on any post
- Edit her/his own existing comments
- Delete her/his own existing comments

Kindly report any malfunctions by sending an email to [me](mailto:ahmadnagib@fci-cu.edu.eg).

## Quick start

### Local Deployment Software Prerequisites 

1. [Python 2.x](https://www.python.org/downloads/) should be installed.
2. [Jinja2 Python Package](https://pypi.python.org/pypi/Jinja2) should be installed to be used as a template engine.
3. Google App Engine SDK for Python should be [downloaded and installed](http://cloud.google.com/appengine/docs/flexible/python/download).

### Deploy QuantumLeap Locally

1. Download the [project's files](https://github.com/ahmadnagib/QuantumLeap) and put them together in one folder.
2. Make sure that all of the prequesites mentioned above are satisfied.
3. Run `dev_appserver.py "PATH TO THE DOWNLOADED PROJECT FOLDER"` from the command line.
4. This will make the blog available at [local host](localhost:8080)

### Deploy QuantumLeap on Google Cloud Platform

1. You should have a [Google Cloud Platform](https://cloud.google.com) account.
2. [Create a new project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) on Google Cloud Platform or overwrite an existing project.
3. Make sure that the [default configurations](https://cloud.google.com/sdk/gcloud/reference/config/set) including the default project are properly set.
4. Open the command line and navigate to the path of the downloaded project folder.
5. You may use the command `gcloud app deploy index.yaml` from the command line to build the Data Store indexes before deploying to your default project. For more info about indexes kindly check [this link](https://cloud.google.com/datastore/docs/concepts/indexes).
6. Deploy your application to the default project on Google Cloud Platform using the command `gcloud app deploy`.
7. Make sure that the [status of all of your project indexes](https://console.cloud.google.com/datastore/indexes) is "serving" so that the blog would perform properly.
8. Use `gcloud app browse` command to open the base url in your default web browser. Alternatively, you can manually open the url on which your application has been deployed using any web browser.
9. An implementation of the blog is available at [QuantumLeap](quantum-leap-blog.appspot.com/).

## What is included

Within the downloaded folder you will find the following files:

```
quantumleap-master/
├── stylesheets/
    ├── main.css
├── templates/
    ├── add-comment.html
    ├── article.html
    ├── base.html
    ├── blog.html
    ├── editcomment.html
    ├── editpost.html
    ├── join.html
    ├── newpost.html
    ├── registration.html
    ├── welcome.html
├── app.yaml
├── blog.py
├── blog_tables.py
├── index.yaml
├── LICENSE
├── README.md
```

## License

QuantumLeap is Copyright © 2017 Ahmad Nagib. It is free software, and may be redistributed under the terms specified in the [LICENSE](/LICENSE) file.
