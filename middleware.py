class ForceHttps(object):
    """
    Work around a bug with Azure Container Apps ingress. Because they don't set
    proxy headers, we need to force Flask to generate https URLs in
    url_for(external=True) calls.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["wsgi.url_scheme"] = "https"
        return self.app(environ, start_response)
