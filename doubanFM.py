#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, requests, os.path, os
MUSIC_DIR = os.path.dirname(os.path.realpath(__file__))
class DoubanFM():
    def __init__(self):
        self.logined = False
        self.history = []
        self.song_list = []
        self.channel = 1
        self.cur_song = ''
        self.proxy = None
    def login(self,email,passwd):
        payload={'email':email,'password':passwd,'app_name':'radio_desktop_win','version':100}
        url = 'http://www.douban.com/j/app/login'
        r = requests.post(url, data=payload,proxies=self.proxy)
        print r.text
        data = r.json
        if data['err']!='ok':
            return False
        self.user_id = data['user_id']
        self.expire = data['expire']
        self.token = data['token']
        self.logined = True
        return True
    def changeChannel(self,channel):
        self.channel = channel
    def playSong(self):
        if len(self.song_list) < 2:
            self.song_list.extend(self.getSongList(self.channel))
        song = self.song_list.pop(0)
        self.history.append(song)
        self.cur_song = song
        print(song['title'])
        return song
    def getParams(self,channel):
        type = 'n'
        h = ''
        sid = ''
        if len(self.history)>0:
            type = 'p'
            h = '|'+':s|'.join([x['sid'] for x in self.history])+':s'
            sid = self.cur_song['sid']
            self.history = []
        if self.logined:
            params = {'app_name':'radio_desktop_win','version':100,'user_id':self.user_id,
                'expire':self.expire,'token':self.token,'type':type,'sid':sid,'h':h,'channel':channel}
        else:
            params = {'app_name':'radio_desktop_win','version':100,'type':type,'sid':sid,'h':h,'channel':channel}
        return params
    def getSongList(self,channel):
        url = 'http://www.douban.com/j/app/radio/people'
        payload = self.getParams(channel)
        r = requests.get(url,params=payload,proxies=self.proxy)
        return r.json['song']
    def getChannels(self):
        url = 'http://www.douban.com/j/app/radio/channels'
        r = requests.get(url,proxies=self.proxy)
        return r.json['channels']
    def printChannels(self):
        self.channels = ''
        if not self.channels:
            self.channels = self.getChannels()
        for channel in self.channels:
            print('%d\t%s\t%s'%(channel['channel_id'],channel['name'],channel['name_en']))
class MusicPlayer():
    def running(self):
        doubanFM = DoubanFM()
        channels = doubanFM.printChannels()
        c = raw_input('channel:')
        doubanFM.changeChannel(int(c))
        if c=='0':
            email = raw_input("email:") 
            import getpass
            password = getpass.getpass("password:") 
            doubanFM.login(email,password)
        while True:
            song = doubanFM.playSong()
            self.playing(url=song['url'])
    def playing(self,url='',file_path='',download=False):
        if download and url and file_path:
            downFile(url,file_path)
        if url:
            os.system('ffplay '+url+' -nodisp -autoexit 1>null 2>null')
        elif file_path:
            os.system('ffplay -i '+file_path+' -nodisp -autoexit 1>null 2>null')
    def onMessage(self):
        pass
    def pause(self):
        pass
    def skip(self):
        pass
    def downFile(self,url,file_path):#Asynchronous
        pass
def main():
    player = MusicPlayer()
    player.running()
if __name__=='__main__':
    main()