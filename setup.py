from setuptools import setup

setup(
  name = 'tweet2story',         
  packages = ['tweet2story'],   
  version = '1.0.1a', 
  setup_requires=['wheel'],
  entry_points='''
        [console_scripts]
        tweet2story=tweet2story.__main__:main
    ''',
  license='MIT',        
  description = 'Create instagram stories from tweets',   
  author = 'Dilpreet Singh',                   
  author_email = 'imdilpreetsio@gmail.com',      
  url = 'https://github.com/dilpreetsio/tweet2story',   
  # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    
  keywords = ['twitter', 'instagram', 'image', 'image processing', 'story', 'computer graphics', 'graphics'],   
  install_requires=[            
          'click',
          'pillow',
          'twint',
          'tweepy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'License :: OSI Approved :: MIT License',   # Again, pick a license
  ],
  python_requires='>=3.5',
)