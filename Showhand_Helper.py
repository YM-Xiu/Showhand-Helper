'''
File    :   Showhand_Helper.py
Note    :   A little tool that helps us to figure out the possibility of win.
Time    :   2022/07/05 21:23
Author  :   Kevin Xiu
Version :   1.0
Contact :   xiuyanming@gmail.com
'''

import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

program_vision = 1.0

'''
全局变量
'''
root = tk.Tk()


class Card(object):
    '''One card.'''

    def __init__(self, suit, number):
        self._suit = suit  # 花色
        self._number = number  # 数值
        self._content = ''  # not used

    @property
    def number(self):
        return self._number

    @property
    def suit(self):
        return self._suit

    @property
    def content(self):
        return self._content

    def get_card(self):  # 用于获取某张牌的字符串形式
        '''Use this function to get the card in str format.'''
        if self._number == 14:
            num_str = 'A'
        elif self.number == 11:
            num_str = 'J'
        elif self.number == 12:
            num_str = 'Q'
        elif self.number == 13:
            num_str = 'K'
        else:
            num_str = str(self._number)

        return '%s%s' % (self._suit, num_str)


class Poker(object):
    '''One deck of cards for Show Hand only.'''

    def __init__(self):
        self.cards = [Card(suit, number)
                      for suit in '♠♥♣♦' for number in range(8, 15, 1)]
        # self.cards_left = [Card(suit, number)
        #                    for suit in '♠♥♣♦' for number in range(8, 15, 1)]
        self.cards_shown = []

    def find_card(self, card):  # 查找某张牌card是否在未知牌堆中
        for c in self.cards:
            if c.get_card() == card:
                return True
        return False

    def find_card_shown(self, card):  # 查找某张牌card是否在已知牌堆中
        for c in self.cards_shown:
            if c.get_card() == card:
                return True
        return False


class Player(object):
    def __init__(self, name):
        self.name = name
        self.cards_have = []
        self.hidden = False
        self.win_poss = 0.0

    def show_your_cards(self, remove=False):
        '''
        显示玩家的牌
        '''
        i = int(self.name[-1])
        cards_text = ''
        if self.hidden == True:
            cards_text += '底牌 '
        # print(self.cards_have)
        for t in self.cards_have:

            # print(f't:{t}')
            cards_text += t.get_card()
            cards_text += ' '

        player_num_label = tk.Label(root, text=cards_text, font=('宋体', 15))
        player_num_label.place(anchor='nw', x=250, y=200+50*i)
        if remove:
            player_num_label = tk.Label(
                root, text='                   ', font=('宋体', 15))
            player_num_label.place(anchor='nw', x=250, y=200+50*i)
        pass


class Helper(object):

    def __init__(self, root):
        self.player_num = 0
        self.poker = Poker()
        self.player_list = []
        self.root = root
        self.gaming = False

    def get_win_chance(self):
        top = tk.Toplevel()
        top.geometry('450x300')
        top.title('正在建设中...')
        top.mainloop()
        pass

    def check_player_num(self, button, entry):
        '''
        异常处理
        '''
        try:
            player_num = int(entry.get())
        except:
            messagebox.askretrycancel(
                "警告", "进程没有响应。如果您选择重试，进程也不会有任何响应。但是在这个等待的过程中，您可能会产生进程可能会响应的错觉。\n您想要现在重试吗？")
            # messagebox.showwarning(title='您好', message="操你妈的")
            entry.delete(0, tk.END)
            return 0

        if player_num <= 5 and player_num >= 2:
            messagebox.showinfo(title='游戏即将开始！', message=f"玩家人数为：{player_num}")
            self.player_num = player_num
            self.game_starts()
            button.config(state=tk.DISABLED)
            return player_num

        # elif self.gaming == True:
        #     messagebox.showwarning(
        #         title='您好', message="游戏已经开始！要重新开始游戏，请点击屏幕下方按钮。")
        #     entry.delete(0, tk.END)
        else:
            messagebox.showwarning(title='您好', message="你输入的能称为一个🧠吗？")
            entry.delete(0, tk.END)
            return 0

    def game_starts(self):
        num = self.player_num

        for i in range(num):
            p_name = 'Player' + str(i)  # Player0 为玩家，Player1/2/3/4为对手。
            self.player_list.append(Player(p_name))

        player_num_label_0 = tk.Button(
            root, text='Player0(点击添加牌)', command=lambda: self.add_card('Player0'))
        player_num_label_0.place(x=100, y=200)
        player_clear_label_0 = tk.Button(
            root, text='Player0(点击清空牌)', command=lambda: self.clear_card('Player0'))
        player_clear_label_0.place(x=600, y=200)

        player_num_label_1 = tk.Button(
            root, text='Player1(点击添加牌)', command=lambda: self.add_card('Player1'))
        player_num_label_1.place(x=100, y=250)
        player_clear_label_1 = tk.Button(
            root, text='Player1(点击清空牌)', command=lambda: self.clear_card('Player1'))
        player_clear_label_1.place(x=600, y=250)

        if num >= 3:
            player_num_label_2 = tk.Button(
                root, text='Player2(点击添加牌)', command=lambda: self.add_card('Player2'))
            player_num_label_2.place(x=100, y=300)
            player_clear_label_2 = tk.Button(
                root, text='Player2(点击清空牌)', command=lambda: self.clear_card('Player2'))
            player_clear_label_2.place(x=600, y=300)

        if num >= 4:
            player_num_label_3 = tk.Button(
                root, text='Player3(点击添加牌)', command=lambda: self.add_card('Player3'))
            player_num_label_3.place(x=100, y=350)
            player_clear_label_3 = tk.Button(
                root, text='Player3(点击清空牌)', command=lambda: self.clear_card('Player3'))
            player_clear_label_3.place(x=600, y=350)

        if num >= 5:
            player_num_label_4 = tk.Button(
                root, text='Player4(点击添加牌)', command=lambda: self.add_card('Player4'))
            player_num_label_4.place(x=100, y=400)
            player_clear_label_4 = tk.Button(
                root, text='Player4(点击清空牌)', command=lambda: self.clear_card('Player4'))
            player_clear_label_4.place(x=600, y=400)

    def clear_card(self, name=None):
        '''
        清空某玩家已选的手牌，从而重新选择。
        '''
        player = self.player_list[int(name[-1])]
        player.hidden = False  # 重置底牌标志
        for e in player.cards_have:
            self.poker.cards.append(e)  # 把玩家手中的每一张牌都还回未知牌堆
            self.poker.cards_shown.remove(e)  # 从已知牌堆中清除玩家手牌
        player.cards_have = []  # 清空玩家手牌
        player.show_your_cards(remove=True)  # 刷新显示
        print('已知的牌：', )  # 在终端刷新已知的牌，并显示之
        for ca in self.poker.cards_shown:
            print(ca.get_card(), end='')
        print('\n')

    def add_card(self, name=None):
        '''
        给某个玩家添加手牌，并选择牌的花色
        '''
        # print(name)
        player = self.player_list[int(name[-1])]
        top = tk.Toplevel()
        top.geometry('450x300')
        top.title(f'为玩家{player.name}添加牌')
        quit_button = tk.Button(top, text='结束选牌', command=top.destroy)
        quit_button.place(x=350, y=250)
        label_choose_suit = tk.Label(top, text='请选择要添加的牌的花色')
        label_choose_suit.place(anchor='nw', x=50, y=20)
        suit_blade = tk.Button(
            top, text='♠', command=lambda: self.add_suit_to_player(top, player, '♠'))
        suit_blade.place(x=50, y=50)

        suit_blade = tk.Button(
            top, text='♥', fg='red', command=lambda: self.add_suit_to_player(top, player, '♥'))
        suit_blade.place(x=100, y=50)

        suit_blade = tk.Button(
            top, text='♣', command=lambda: self.add_suit_to_player(top, player, '♣'))
        suit_blade.place(x=150, y=50)

        suit_blade = tk.Button(
            top, text='♦', fg='red', command=lambda: self.add_suit_to_player(top, player, '♦'))
        suit_blade.place(x=200, y=50)

        suit_hidden = tk.Button(
            top, text='底牌', command=lambda: self.add_suit_to_player(top, player, '底牌'))
        suit_hidden.place(x=250, y=50)
        if player.hidden == True:
            suit_hidden.config(state=tk.DISABLED)
        # print(self.poker.cards)
        top.mainloop()
        pass

    def add_suit_to_player(self, window=None, player=None, suit=None):
        '''
        在花色确定的前提下，进一步确定牌的面值。底牌无面值。
        '''
        if suit == '底牌':
            self.add_card_to_player(player, suit, '')
            return 0

        label_choose_suit = tk.Label(window, text='请选择要添加的牌的数值')
        label_choose_suit.place(anchor='nw', x=50, y=120)
        number_8 = tk.Button(
            window, text='8', command=lambda: self.add_card_to_player(player, suit, '8'))
        number_8.place(x=50, y=150)
        if self.poker.find_card(suit+'8') == False:
            number_8.config(state=tk.DISABLED)

        number_9 = tk.Button(
            window, text='9', command=lambda: self.add_card_to_player(player, suit, '9'))
        number_9.place(x=100, y=150)
        if self.poker.find_card(suit+'9') == False:
            number_9.config(state=tk.DISABLED)

        number_10 = tk.Button(
            window, text='10', command=lambda: self.add_card_to_player(player, suit, '10'))
        number_10.place(x=150, y=150)
        if self.poker.find_card(suit+'10') == False:
            number_10.config(state=tk.DISABLED)

        number_J = tk.Button(
            window, text='J', command=lambda: self.add_card_to_player(player, suit, 'J'))
        number_J.place(x=200, y=150)
        if self.poker.find_card(suit+'J') == False:
            number_J.config(state=tk.DISABLED)

        number_Q = tk.Button(
            window, text='Q', command=lambda: self.add_card_to_player(player, suit, 'Q'))
        number_Q.place(x=250, y=150)
        if self.poker.find_card(suit+'Q') == False:
            number_Q.config(state=tk.DISABLED)

        number_K = tk.Button(
            window, text='K', command=lambda: self.add_card_to_player(player, suit, 'K'))
        number_K.place(x=300, y=150)
        if self.poker.find_card(suit+'K') == False:
            number_K.config(state=tk.DISABLED)

        number_A = tk.Button(
            window, text='A', command=lambda: self.add_card_to_player(player, suit, 'A'))
        number_A.place(x=350, y=150)
        if self.poker.find_card(suit+'A') == False:
            number_A.config(state=tk.DISABLED)

    def add_card_to_player(self, player=None, suit=None, number=None):
        '''
        将选择好的牌发到玩家手中，并在GUI上显示。
        '''
        card_final = suit + number
        # print(f'finalcard:{card_final}')
        if card_final == '底牌':  # 底牌并不会作为一张实体牌被放入已知牌堆/玩家手牌堆。
            player.hidden = True

        if len(player.cards_have) == 5:
            messagebox.showwarning(title='您好', message="这是港式五张，所以不能摸六张牌。")
            return 0

        for c in self.poker.cards:
            # print(c.get_card())
            if card_final == c.get_card():
                player.cards_have.append(c)
                self.poker.cards_shown.append(c)
                self.poker.cards.remove(c)
                break

        player.show_your_cards()
        print('已知的牌：', )
        for ca in self.poker.cards_shown:
            print(ca.get_card(), end='')
        print('\n')

    def helper_main(self):
        root.geometry('900x600')  # 窗口大小
        root.iconbitmap('icon.ico')  # 设置图标
        root.title(f'Showhand Helper{program_vision}')  # 窗口名称

        # 添加文本内,设置字体的前景色和背景色，和字体类型、大小
        text = tk.Label(root, text="欢迎使用梭哈助手", bg="white",
                        fg="black", font=('隶书', 30))
        # 将文本内容放置在主窗口内
        text.place(anchor='n', x=450, y=0)

        player_num = 0
        player_num_label = tk.Label(root, text='请输入玩家人数')
        player_num_label.place(anchor='nw', x=100, y=50)
        player_num_entry = tk.Entry(root)
        player_num_entry.place(anchor='nw', x=100, y=100)
        start_button = tk.Button(root, text='开始游戏',
                                 command=lambda: self.check_player_num(start_button, player_num_entry))  # the lambda is of great significance!!!!!
        start_button.place(anchor='nw', x=100, y=150)
        # player_num = int(player_num_entry.get())

        quit_button = tk.Button(root, text="退出程序",
                                command=root.destroy)  # 退出程序按钮
        quit_button.place(anchor='center', width=100,
                          height=50, relx=0.7, rely=0.9)
        cal_button = tk.Button(root, text="计算胜率",
                               command=self.get_win_chance)  # 退出程序按钮
        cal_button.place(anchor='center', width=100,
                         height=50, relx=0.3, rely=0.9)
        restart_button = tk.Button(root, text="重新开始",
                                   command=lambda: self.restart(start_button))  # 退出程序按钮
        restart_button.place(anchor='center', width=100,
                             height=50, relx=0.5, rely=0.9)
        root.mainloop()

        return 0

    def restart(self, button):
        self.poker = Poker()  # 重置牌堆（已知的和未知的）
        root.quit()  # 刷新界面
        cover = tk.Frame(root, height=300, width=800)  # 强行把组件盖住
        cover.place(x=0, y=200)
        for player in self.player_list:
            print(player.name)
            player.hidden = False  # 重置底牌标志
            player.cards_have = []  # 收回手牌
            # player.show_your_cards(remove=True)
        self.player_list = []  # 清空玩家
        button['state'] = 'normal'  # “开始游戏”按钮设置为可点击状态
        return 0


def main():
    while(1):
        myHelper = Helper(root)
        myHelper.helper_main()
        print('new loop!')


if __name__ == '__main__':
    main()
