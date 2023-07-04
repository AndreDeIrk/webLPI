from setuptools import setup

setup(
   name='app',
   version='1.0',
   description='A useful module',
   author='BA',
   author_email='foomail@foo.example',
   packages=['app'],
   install_requires=[
      'uvicorn',
      'fastapi',
      'sqlalchemy',
      'pydantic',
      'python-decouple',
      'pyjwt',
      'requests',
      'python-multipart',
      'Pillow',      
   ],
)