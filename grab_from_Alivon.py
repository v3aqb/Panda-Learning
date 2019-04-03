import urllib.request

path_url = {
    './pandalearning.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pandalearning.py',
    './pdlearn/__init__.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/__init__.py',
    './pdlearn/dingding.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/dingding.py',
    './pdlearn/get_links.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/get_links.py',
    './pdlearn/mydriver.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/mydriver.py',
    './pdlearn/score.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/score.py',
    './pdlearn/threads.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/threads.py',
    './pdlearn/user.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/user.py',
    './pdlearn/version.py': 'https://github.com/Alivon/Panda-Learning/raw/master/Source%20Packages/pdlearn/version.py',
}

for path, url in path_url.items():
    print('downloading %s' % path)
    data = urllib.request.urlopen(url).read()
    with open(path, 'wb') as f:
        f.write(data)
