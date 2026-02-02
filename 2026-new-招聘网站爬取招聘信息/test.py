from DrissionPage import ChromiumOptions
#打开edge浏览器
path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
ChromiumOptions().set_browser_path(path).save()
#打开chrome浏览器
path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ChromiumOptions().set_browser_path(path).save()