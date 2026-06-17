import requests


for method in ("get", "post","put", "delete", "head", "options", "patch"):
    og=getattr(requests, method)    
    def insec_req(*args, _original =og, **kwargs):
        kwargs["verify"] = False
        return _original(*args, **kwargs)
    setattr(requests, method, insec_req)