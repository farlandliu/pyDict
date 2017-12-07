#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import os, sys
import click
import urllib2, urllib
from bs4 import BeautifulSoup
from colorama import init   #, AnsiToWin32
from colorama import Fore, Back, Style

"""
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
"""
init(autoreset=True)

def wd(word):
    wd_dict ={'word':word}
    wd_dict['auth_exp']= ""
    wd_dict['en_exp'] = ""
    url = 'https://www.bing.com/dict/search?' + urllib.urlencode({'q':word})
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
    res = urllib2.urlopen(request,timeout=10)    
    content = res.read().decode('utf-8')
    
    root = BeautifulSoup(content,  "html.parser")

    print Fore.RED + root.title.text
    hd_pr = root.find("div", class_="hd_pr")
    if hd_pr:
        wd_dict['pro'] = hd_pr.text + ' | ' + root.find("div", class_="hd_prUS").text
        print wd_dict['pro']
    thesaurus = root.find("div", id="thesaurusesid")
    if thesaurus:
        wd_dict['thesaurus'] = thesaurus.text
        print wd_dict['thesaurus']
    # authrity explanation
    auth_list = root.find("div",id="authid").find("div", class_="li_sen").find_all("div", class_="se_lis")
    for auth in auth_list:
        wd_dict['auth_exp'] += auth.text + '\n'
    print Fore.BLUE + "--------Auth Explanation------------"
    print wd_dict['auth_exp']  

    #english explanation
    # import pdb;pdb.set_trace()
    homos = root.find("div",id="homoid").find_all("tr", class_="def_row df_div1")
    ex_homo = ""
    for homo in homos:
        ex_homo += homo.find("div",class_="pos pos1").text + '\n'
        df_list = homo.find("div", class_="def_fl").find_all(class_="de_li1 de_li3")
        for df in df_list:
            ex_homo += df.text + "\n "
    wd_dict['en_exp'] = ex_homo 
    print Fore.BLUE + "--------Eng to Eng Explanation------------"
    print wd_dict['en_exp']


@click.command()
@click.argument('word')
def cli(word):
    """Example script."""
    print Style.DIM + "Bing Dictionary ..."
    wd(word)

if __name__ == '__main__':
    cli()
    
