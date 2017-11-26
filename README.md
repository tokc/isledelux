# Isle de Lux

Isle de Lux is a Python 3 program that generates and renders images of islands and posts them to Twitter.

## Dependencies

This program depends on Blender, the 3D modeling software, as well as the Python module Tweepy in order to talk to Twitter.

You can get Blender from [www.blender.org](https://www.blender.org).

You can use something like pip to install Tweepy:

```
pip install tweepy
```

## Run the Twitter Bot

Fill in your API keys and path to Blender in config.py, then run isledelux.py, and it will tweet out images.

```
python isledelux.py
```

## Blender Scripts

If you would like to play around with the Blender Python script in your own Blender scene, load up the isledelux_GUI.py file and hit "Run Script". Be aware that the script empties out the scene before adding stuff, so **don't run it in a scene full of important stuff!**

### Twitter

You can find Isle de Lux [@isledelux on Twitter](https://twitter.com/isledelux).