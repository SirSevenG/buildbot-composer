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


def apppend_yml(param_set, is_wine):
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


def append_env(param_list):
    # expected param_list = [string1, string2, string3, string4, string5]
    low4 = param_list[4].lower()
    up4 = param_list[4].upper()
    params = ('\n# Buildbot_' + low4 + '_worker params\n')
    params += (up4 + '_BUILDMASTER=' + param_list[0] + '\n')
    params += (up4 + '_BUILDMASTER_PORT=' + param_list[1] + '\n')
    params += (up4 + '_WORKERNAME=' + param_list[2] + '\n')
    params += (up4 + '_WORKERPASS=' + param_list[3] + '\n')
    with open('.env', 'a') as env:
        env.write(params)


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
    master += ("c['workers'].append(worker.Worker(" + low_set + "_workername, " + low_set + "_workerpass)\n")
    master += (base + ".append(" + low_set + "_workername)\n")
    with open('master/docker/master.cfg', 'a') as cfg:
        cfg.write(master)


def write_env_settings(param_list):
    # expected param_list length is 4 strings
    to_find = ["BM_BUILDBOT_REPO_URL=", "BM_BUILDBOT_REPO_BRANCH=", "BM_BUILDBOT_REPO=", "BM_BUILDBOT_WEB_URL="]
    to_write = []
    for i in range(len(to_find)):
        to_write.append(to_find[i] + param_list[i])
    str_rewrite(to_find, to_write, '.env')


def write_env_postgrespw():
    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(random.choice(alphabet) for num in range(16))
    print('New Postgres password:\n' + new_password + '\n')
    to_find = ["POSTGRES_PASSWORD="]
    to_write = [("POSTGRES_PASSWORD=" + new_password)]
    str_rewrite(to_find, to_write, '.env')


def check_pgsql_exists():
    pass


def main():
    # prompt for secrets
    # prompt for settings
    # write settings to .env
    # prompt for extentions
    # prompt for extentions settings
    # append extentions to .env, compose.yml and master.cfg
    pass


if __name__ == '__main__':
    main()
