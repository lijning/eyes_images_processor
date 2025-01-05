# Roadmap

- To publish the webapp as an Android appication:
  - Use p4a: https://python-for-android.readthedocs.io/en/latest/quickstart.html

```
p4a apk --private $HOME/your_app_directory --package=org.example.yourpackage --name "Your App Name" --version 0.1 --bootstrap=webview --requirements=flask --port=5000
```

- Problem shooting:

识别面部位置，框选上半部分。