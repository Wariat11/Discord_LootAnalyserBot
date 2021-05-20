# https://pastebin.com/0yuxc4Ek
# https://pastebin.com/eE6JGf7S
from json import load,dump
import requests
from bs4 import BeautifulSoup
import re

pastebin_pattern = re.compile(r"(https|http)://pastebin.com/(raw/)?([A-Za-z0-9]{8})")


class LootAnalyser:
    def parse_loot(self,pastebin):
        self.monsters = {}
        try:
            pastebin_pattern.match(pastebin)
            response = requests.get(pastebin)
            soup = BeautifulSoup(response.text, 'html.parser')
            pastebin_list = soup.find_all('li',{'class':'li1'})
        except:
            print("Error, incorrect pastebin")
            
        for i in pastebin_list:
            delete_time = i.text[8:]
            if delete_time[:3] == 'You' or delete_time[:3] == '':
                continue
            colon = delete_time.find(':')
            monster = delete_time[0:colon]
            drop = ' '.join([i for i in delete_time[colon + 1:].split() if not i.isdigit()]).split(', ')
            if monster not in self.monsters:
                self.monsters[monster] = {
                'monster_name' : monster,
                'killed' : 1,
                'drop' : {
                }
                }
            else:
                self.monsters[monster]['killed'] += 1
                for item in drop:
                    if item == '':
                        continue
                    if item not in self.monsters[monster]['drop']:
                        self.monsters[monster]['drop'][item] = 1
                    else:
                        self.monsters[monster]['drop'][item] += 1
        return self.monsters
    
    def add_to_json(self):
        with open('loot.json') as file:
            data = load(file)
        with open('loot.json','w') as file:
            for monster, monster_value in self.monsters.items():
                if monster not in data:
                    data[monster] = {
                        "monster_name" : monster,
                        "killed" : monster_value['killed'],
                        "drop" : monster_value['drop']
                    }
                else:
                    data[monster]['killed'] += monster_value['killed']
                    for item in self.monsters[monster]['drop']:
                        if item not in data[monster]['drop']:
                            data[monster]['drop'][item] = self.monsters[monster]['drop'][item]
                        else:
                            data[monster]['drop'][item] += self.monsters[monster]['drop'][item]
            dump(data,file,indent=4)
        self.monsters.clear()
        
    def load_info_json(self,choice):
        with open('loot.json') as file:
            data = load(file)
        monster_capitalize = [i for i in choice.split()]
        choice = " ".join(monster_capitalize)
        for monster in data:
            try:
                if choice in monster:
                    print (choice)
                    print(choice)
                    print(f"Zabitych: {data[choice]['killed']}")
                    print(f"Loot:")
                    for item,quantity in data[choice]['drop'].items():
                        print( f"{item.ljust(22)} {round(quantity / data[choice]['killed'] * 100,1)} %")
                    break
                if choice in data[monster]['drop']:
                    if choice in data[monster]['drop']:
                        print( f"{data[monster]['monster_name'].ljust(22)} {round(data[monster]['drop'][choice] / data[monster]['killed'] * 100,1)} %")
            except:
                print("Not exists in database")
    