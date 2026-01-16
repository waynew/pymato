from invoke import task


@task
def upload_docs(c):
    c.run('rsync -rv docs/ dev.waynewerner.com:/var/www/dev.waynewerner.com/pub/pymato/')
