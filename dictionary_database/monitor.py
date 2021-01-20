import subprocess

# restart program on death

while True:
    try:
        subprocess.check_call(["py", "fetch_dict_from_youdao.py"])
        break;
    except subprocess.CalledProcessError as err:
        print(err);