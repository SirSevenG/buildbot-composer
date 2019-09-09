import os
import string
import random


def str_rewrite(find, replace, infile):
    # expected str_replace(list_of_strings_to_find, list_of_string_to_replace, filename_string)
    tmp = (infile + '.tmp')
    for i in range(len(find)):
        os.system('cp' + ' ' + infile + ' ' + tmp)
        with open(tmp, 'r') as source:
            with open(infile, 'w') as out:
                for line in source.readlines():
                    # f.write(line.replace(find[i], replace[i]))
                    if find[i] in line:
                        line = (replace[i] + '\n')
                    out.write(line)
    os.remove(tmp)


def append_env(param_list):
    # expected param_list = [string1=buildbot, string2=9989, string3=name_worker, string4=password]
    low2 = param_list[2].lower()
    up2 = param_list[2].upper()
    name = low2 + "_worker"
    params = ('\n# Buildbot_' + name + 'params\n')
    params += (up2 + '_BUILDMASTER=' + param_list[0] + '\n')
    params += (up2 + '_BUILDMASTER_PORT=' + param_list[1] + '\n')
    params += (up2 + '_WORKERNAME=' + name + '\n')
    params += (up2 + '_WORKERPASS=' + param_list[3] + '\n')
    with open('.env', 'a') as env:
        env.write(params)


def append_yml(param_set, is_wine):
    # expected write_yml(string, any)
    up_set = param_set.upper()
    low_set = param_set.lower()
    params = ('\n' + 2 * ' ' + 'worker_' + low_set + ':\n')
    if is_wine:
        params += (4 * ' ' + 'build: ./worker_wine\n')
    else:
        params += (4 * ' ' + 'build: ./worker\n')
    params += (4 * ' ' + 'environment:\n')
    params += (6 * ' ' + 'BUILDMASTER: ${' + up_set + '_BUILDMASTER}\n')
    params += (6 * ' ' + 'BUILDMASTER_PORT: ${' + up_set + '_BUILDMASTER_PORT}\n')
    params += (6 * ' ' + 'WORKERNAME: ${' + up_set + '_WORKERNAME}\n')
    params += (6 * ' ' + 'WORKERPASS: ${' + up_set + '_WORKERPASS}\n')
    params += (6 * ' ' + 'WORKER_ENVIRONMENT_BLACKLIST: ${BASE_WORKER_ENVIRONMENT_BLACKLIST}\n')
    params += (4 * ' ' + 'links:\n')
    params += (8 * ' ' + '- buildbot\n')
    params += (4 * ' ' + 'depends_on:\n')
    params += (8 * ' ' + '- buildbot\n')
    with open('docker-compose.yml', 'a') as yml:
        yml.write(params)


def append_master(param_set, is_win):
    # expected append_master(string, any)
    if is_win:
        base = 'win_workernames'
    else:
        base = 'ux_workernames'
    low_set = param_set.lower()
    up_set = param_set.upper()
    master = '\n'
    master += (low_set + "_workername = os.environ.get('" + up_set + "_WORKERNAME')\n")
    master += (low_set + "_workerpass = os.environ.get('" + up_set + "_WORKERPASS')\n")
    master += ("c['workers'].append(worker.Worker(" + low_set + "_workername, " + low_set + "_workerpass))\n")
    master += (base + ".append(" + low_set + "_workername)\n")
    with open('master/docker/master.cfg', 'a') as cfg:
        cfg.write(master)


def write_env_settings(param_list):
    # expected param_list length is 4 strings
    param_list[3] = ('https://' + param_list[3] + '/')
    to_find = ["BM_BUILDBOT_REPO_URL=", "BM_BUILDBOT_REPO_BRANCH=", "BM_BUILDBOT_REPO=", "BM_BUILDBOT_WEB_URL="]
    to_write = []
    for i in range(len(to_find)):
        to_write.append(to_find[i] + param_list[i])
    str_rewrite(to_find, to_write, '.env')


def randgen(lens):  # expected int(lens)
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for num in range(lens))
    return password


def write_env_postgrespw():
    new_password = randgen(16)
    print('New Postgres password:\n' + new_password + '\n')
    to_find = ["POSTGRES_PASSWORD="]
    to_write = [("POSTGRES_PASSWORD=" + new_password)]
    str_rewrite(to_find, to_write, '.env')


def check_pgsql_exists():
    pass


def write_secret(value, file):
    secret = ("master/docker/secrets/" + file)
    with open(secret, 'w') as f:
        f.write(value)


def main():
    os.system('cp example.env .env')
    os.system('cp example-compose.yml docker-compose.yml')
    print("Welcome to buildbot-composer setup")
    print("Preparing databse password")
    write_env_postgrespw()
    print("Done")

    repo_url = input("Type url to github repository to test: ")
    print(repo_url)
    repo_branch = input("Repository branch to follow: ")
    print(repo_branch)
    repo = input("Repository url(without .git postfix): ")
    print(repo)
    domain = input("Domain or ip to point buildbot to: ")
    print(domain)
    print("Saving repo settings")
    write_env_settings([repo_url, repo_branch, repo, domain])
    print("Done")

    wif = input("Input WIF to test with: ")
    write_secret(wif, 'wif')
    coin = input("Coin to test: ")
    write_secret(coin, 'coin')
    addr = input("Test coin public address: ")
    write_secret(addr, 'addr')
    print("Libwin download params: ")
    url = input("url: ")
    user = input("user: ")
    pwd = input("pwd: ")
    write_secret(url, 'url')
    write_secret(user, 'user')
    write_secret(pwd, 'pwd')

    while True:
        change_admin = input("Do you want to change default webui login? (y/N): ")
        if change_admin == 'yes' or change_admin == 'y' or change_admin == 'Y':
            admin_name = input("Administrator login: ")
            admin_pass = input("Administrator password: ")
            print(admin_name, admin_pass)
            write_secret(admin_name, 'admin_name')
            write_secret(admin_pass, 'admin_pwd')
            print("Done")
            break
        elif change_admin == 'N' or change_admin == 'n' or change_admin == 'No':
            print("Defaults to admin/damin")
            write_secret('admin\n', 'admin_name')
            write_secret('admin\n', 'admin_pass')
            print("Done")
            break
        else:
            print("Unexpected input: ", change_admin)

    while True:
        add_workers = input("Set up additional workers? (y/N): ")
        if add_workers == 'yes' or add_workers == 'y' or add_workers == 'Y':
            worker_name = input("Name your new worker: ")
            print("New worker name: ", worker_name)
            pwd = randgen(8)
            defaults = ['buildbot', '9989', worker_name, pwd]
            append_env(defaults)
            while True:
                is_wine = input("Setup win or linux worker? (win/ux): ")
                if is_wine == 'win':
                    print("Windows worker set up")
                    append_yml(worker_name, 1)
                    append_master(worker_name, 1)
                    print("Done")
                    break
                elif is_wine == 'ux':
                    print("Linux worker set up:")
                    append_yml(worker_name, 0)
                    append_master(worker_name, 0)
                    print("Done")
                    break
                else:
                    print("Unexpected input: ", is_wine)
        elif add_workers == 'no' or add_workers == 'n' or add_workers == 'N':
            print("Setup finished, use 'docker-compose up' command to initiate build")
            break
        else:
            print("Unexpected input: ", add_workers)
    # prompt for secrets
    # prompt for settings
    # write settings to .env
    # prompt for extentions
    # prompt for extentions settings
    # append extentions to .env, compose.yml and master.cfg


if __name__ == '__main__':
    main()
