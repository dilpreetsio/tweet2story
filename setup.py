from setuptools import setup

setup(
  name = 'tweet2story',         # How you named your package folder (MyLib)
  packages = ['tweet2story'],   # Chose the same as "name"
  version = '0.1', 
  setup_requires=['wheel'],
  entry_points='''
        [console_scripts]
        tweet2story=tweet2story.__main__:main
    ''',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Create instagram stories from tweets',   # Give a short description about your library
  author = 'Dilpreet Singh',                   # Type in your name
  author_email = 'imdilpreetsio@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['twitter', 'instagram', 'image', 'image processing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
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