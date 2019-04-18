import os
import requests
import urllib.request
import zipfile
import glob


def main():
    # check update_log
    update_log = requests.get(
        "https://raw.githubusercontent.com/Alivon/Panda-Learning/master/Update%20log").content.decode(
        "utf8").splitlines()

    version_info = update_log[1].split("=")[1]
    print('remote_version: %s' % version_info)

    # compare with local version
    try:
        current_version = open('pdl_current').read()
    except Exception:
        current_version = '0'
    print('current_version: %s' % current_version)

    if version_info == current_version:
        print('no update required')
        return

    # download form https://github.com/Alivon/Panda-Learning/archive/master.zip
    print('download pd.zip ...')
    urllib.request.urlretrieve('https://github.com/Alivon/Panda-Learning/archive/master.zip', 'pd.zip')

    # remove files
    flist = glob.glob('pdlearn/*.py')
    for f in flist:
        os.remove(f)

    print('extract pd.zip ...')
    with zipfile.ZipFile('pd.zip') as z:
        namelist = z.namelist()
        file_list = [name for name in namelist if name.startswith('Panda-Learning-master/Source Packages/') and '.py' in name]

        # extract files
        for file in file_list:
            data = z.open(file).read()
            new_file = file.replace('Panda-Learning-master/Source Packages/', '')
            with open(new_file, 'wb') as f:
                f.write(data)

    os.remove('pd.zip')
    with open('pdl_current', 'w') as f:
        f.write(version_info)


if __name__ == '__main__':
    main()
