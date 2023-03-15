# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 08:17:07 2021

Card.py

@author: onodera
"""

from enum import Enum, auto
import pygame

class Type(Enum):
    """
     ランプカードの種類列挙子
     (なし、スペード、ハート、ダイア（モンド）、クラブ、ジョーカー)
    """
    NONE = auto()
    SPADE = auto()
    HEART = auto()
    DIAMOND = auto()
    CLUB = auto()
    JOCKER = auto()

class Card(Enum):
    """
    トランプカードの列挙子（５２枚）
    
    Attributes:
        id(int):        ID
        str(String):    名称文字列
        type(Type):     カードの種類
        num(int):       番号
        filename(str):  画像ファイル名称
    """
    NONE = (-1, "裏", Type.NONE, -1, "card_back")
    S01 = (0, "スペード１", Type.SPADE, 1, "card_spade_01")
    S02 = (1, "スペード２", Type.SPADE, 2, "card_spade_02")
    S03 = (2, "スペード３", Type.SPADE, 3, "card_spade_03")
    S04 = (3, "スペード４", Type.SPADE, 4, "card_spade_04")
    S05 = (4, "スペード５", Type.SPADE, 5, "card_spade_05")
    S06 = (5, "スペード６", Type.SPADE, 6, "card_spade_06")
    S07 = (6, "スペード７", Type.SPADE, 7, "card_spade_07")
    S08 = (7, "スペード８", Type.SPADE, 8, "card_spade_08")
    S09 = (8, "スペード９", Type.SPADE, 9, "card_spade_09")
    S10 = (9, "スペード１０", Type.SPADE, 10, "card_spade_10")
    S11 = (10, "スペードＪ", Type.SPADE, 11, "card_spade_11")
    S12 = (11, "スペードＱ", Type.SPADE, 12, "card_spade_12")
    S13 = (12, "スペードＫ", Type.SPADE, 13, "card_spade_13")
    H01 = (13, "ハート１", Type.HEART, 1, "card_heart_01")
    H02 = (14, "ハート２", Type.HEART, 2, "card_heart_02")
    H03 = (15, "ハート３", Type.HEART, 3, "card_heart_03")
    H04 = (16, "ハート４", Type.HEART, 4, "card_heart_04")
    H05 = (17, "ハート５", Type.HEART, 5, "card_heart_05")
    H06 = (18, "ハート６", Type.HEART, 6, "card_heart_06")
    H07 = (19, "ハート７", Type.HEART, 7, "card_heart_07")
    H08 = (20, "ハート８", Type.HEART, 8, "card_heart_08")
    H09 = (21, "ハート９", Type.HEART, 9, "card_heart_09")
    H10 = (22, "ハート１０", Type.HEART, 10, "card_heart_10")
    H11 = (23, "ハートＪ", Type.HEART, 11, "card_heart_11")
    H12 = (24, "ハートＱ", Type.HEART, 12, "card_heart_12")
    H13 = (25, "ハートＫ", Type.HEART, 13, "card_heart_13")
    D01 = (26, "ダイア１", Type.DIAMOND, 1, "card_diamond_01")
    D02 = (27, "ダイア２", Type.DIAMOND, 2, "card_diamond_02")
    D03 = (28, "ダイア３", Type.DIAMOND, 3, "card_diamond_03")
    D04 = (29, "ダイア４", Type.DIAMOND, 4, "card_diamond_04")
    D05 = (30, "ダイア５", Type.DIAMOND, 5, "card_diamond_05")
    D06 = (31, "ダイア６", Type.DIAMOND, 6, "card_diamond_06")
    D07 = (32, "ダイア７", Type.DIAMOND, 7, "card_diamond_07")
    D08 = (33, "ダイア８", Type.DIAMOND, 8, "card_diamond_08")
    D09 = (34, "ダイア９", Type.DIAMOND, 9, "card_diamond_09")
    D10 = (35, "ダイア１０", Type.DIAMOND, 10, "card_diamond_10")
    D11 = (36, "ダイアＪ", Type.DIAMOND, 11, "card_diamond_11")
    D12 = (37, "ダイアＱ", Type.DIAMOND, 12, "card_diamond_12")
    D13 = (38, "ダイアＫ", Type.DIAMOND, 13, "card_diamond_13")
    C01 = (39, "クラブ１", Type.CLUB, 1, "card_club_01")
    C02 = (40, "クラブ２", Type.CLUB, 2, "card_club_02")
    C03 = (41, "クラブ３", Type.CLUB, 3, "card_club_03")
    C04 = (42, "クラブ４", Type.CLUB, 4, "card_club_04")
    C05 = (43, "クラブ５", Type.CLUB, 5, "card_club_05")
    C06 = (44, "クラブ６", Type.CLUB, 6, "card_club_06")
    C07 = (45, "クラブ７", Type.CLUB, 7, "card_club_07")
    C08 = (46, "クラブ８", Type.CLUB, 8, "card_club_08")
    C09 = (47, "クラブ９", Type.CLUB, 9, "card_club_09")
    C10 = (48, "クラブ１０", Type.CLUB, 10, "card_club_10")
    C11 = (49, "クラブＪ", Type.CLUB, 11, "card_club_11")
    C12 = (50, "クラブＱ", Type.CLUB, 12, "card_club_12")
    C13 = (51, "クラブＫ", Type.CLUB, 13, "card_club_13")
    JOK = (52, "ジョーカー", Type.JOCKER, 0, "card_joker")
    
    def __init__(self, id, str, type, num, filename):
        """
        コンストラクタ（自動生成）

        Parameters
        ----------
        id : int
            カードID.
        str : string
            カード名称文字列.
        type : Type
            カード種類.
        num : int
            カード番号.
        filename : string
            カード画像ファイル名.

        Returns
        -------
        None.

        """
        self.id = id
        self.str = str
        self.type = type
        self.num = num
        self.filename = filename
        self.images = []
        
    def __hash__(self):
        """
        ハッシュ関数

        Returns
        -------
        int
            ハッシュ値（IDをハッシュ化した値）

        """
        return hash(self.id)
    
    def __eq__(self, other):
        """
        比較関数（等価）

        Parameters
        ----------
        other : Fuda
            比較対象.

        Returns
        -------
        bool
            等価であればTrueを返す.

        """
        if not isinstance(other, Card):
            return NotImplemented
        return self.id == other.id
    
    def __lt__(self, other):
        """
        比較関数（より小さい）

        Parameters
        ----------
        other : Fuda
            比較対象.

        Returns
        -------
        bool
            比較対象より小さければTrue.

        """
        if not isinstance(other, Card):
            return NotImplemented
        return self.id < other.id
    
    def __ne__(self, other):
        """
        比較関数（非等価）

        Parameters
        ----------
        other : Fuda
            比較対象.

        Returns
        -------
        bool
            比較対象と非等価であればTrue.

        """
        return not self.__eq__(other)
    
    def __le__(self, other):
        """
        比較関数（等価か、より小さい）

        Parameters
        ----------
        other : Fuda
            比較対象.

        Returns
        -------
        bool
            比較対象と等価か、より小さければTrue.

        """        
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other):
        """
        比較関数（より大きい）

        Parameters
        ----------
        other : Fuda
            比較対象.

        Returns
        -------
        bool
            比較対象より大きければTrue.

        """
        return not self.__le__(other)
    
    def __ge__(self, other):
        """
        比較関数（等価か、より大きい）

        Parameters
        ----------
        other : Fuda
            比較対象.

        Returns
        -------
        bool
            比較対象と等価か、より大きければTrue.

        """  
        return not self.__lt__(other)
    
    def getId(self):
        """
        カードのIDを返す

        Returns
        -------
        int
            カードID

        """
        return self.id
    
    def __str__(self):
        """
        カード名称を返す

        Returns
        -------
        string
            カード名称文字列.

        """
        return self.str
    
    def getType(self):
        """
        カードの種類を返す

        Returns
        -------
        Type
            カード種.

        """
        return self.type
    
    def getNumber(self):
        """
        カード番号を返す

        Returns
        -------
        int
            カード番号.

        """
        return self.num
    
    def getImage(self, i):
        """
        カードの画像を返す

        Returns
        -------
        Image
            カード画像.

        """
        return self.images[i]
    
    @classmethod
    def getByid(cls, id):
        """
        IDに対応する列挙型を返す（クラスメｓドッド）

        Parameters
        ----------
        cls : Card
            クラス（クラスメソッド引数）.
        id : int
            ID.

        Returns
        -------
        Card
            カード列挙子（該当しない場合はNone）

        """
        for c in cls.__members__.values():
            if id == c.id:
                return c
        return None
    
    @classmethod
    def initImage(cls):
        """
        画像データの初期化（クラスメソッド）

        Parameters
        ----------
        cls : Card
            クラス（クラスメソッド引数）.
        master : tkinter.Tk
            描画トップレベル.

        Returns
        -------
        None.

        """
        for c in cls.__members__.values():
            filename = "./png/" + c.filename + ".png"
            img = pygame.image.load(filename)
            img1 = pygame.transform.scale(img, (82, 120))
            c.images.append(img1)
            img2 = pygame.transform.scale(img, (61, 90))
            c.images.append(img2)
            
    @classmethod
    def Dimensions(cls, i):
        """
        画像のサイズ（幅、高さ）を返す

        Parameters
        ----------
        cls : Card
            クラス（クラスメソッド引数）.
        i : int
            画像番号.

        Returns
        -------
        int
            画像の幅.
        int
            画像の高さ.

        """
        return ((82, 120),(61, 90))[i]