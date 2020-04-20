




def save_page(html,filename):
    f = open(filename, 'wb')
    f.write(html)
    f.close()
    return 1


def logging(path, url, status):
    from os.path import exists, join

    if not exists(path):
        f = open(join(path, 'crawlerlog.txt'), 'w')
    else:
        f = open(join(path, 'crawlerlog.txt'), 'a')
        
    log = str(status) + "->" + url + '\n'
    print(log)
    f.write(log)
    f.close()
        
    