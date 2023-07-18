from .settings import base

def elms_context_processor(req):
  return {
    'SITE_NAME': base.SITE_NAME,
  }