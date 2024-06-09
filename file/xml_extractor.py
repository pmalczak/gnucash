#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler


class MyHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.stack = []
        self.accounts = {}
        self.transactions = []
        self.txt = ""
        self.bufAcc = Container()
        self.bufTrans = Container()
        self.bufTrans.splits = []
        self.bufSplit = Container()
        self.unused = set()

    def characters(self, content):
        self.txt += content

    def startElement(self, name, attr):
        self.stack += [name]

    def endElement(self, name):
        top = self.stack.pop()
        if top != name:
            raise Exception(name + " for self.stack: " + str(self.stack))

        if name == "gnc:account":
            self.bufAcc.strip()
            self.accounts[self.bufAcc.id] = self.bufAcc
            self.bufAcc = Container()
        elif name == "gnc:transaction":
            self.bufTrans.strip()
            self.transactions += [self.bufTrans]
            self.bufTrans = Container()
            self.bufTrans.splits = []

        elif name == "trn:split" and self.stack[-1] == "trn:splits":
            self.bufSplit.strip()
            self.bufTrans.splits += [self.bufSplit]
            self.bufSplit = Container()

        elif name == "act:name" and self.stack[-1] == "gnc:account":
            self.bufAcc.name = self.txt
            self.txt = ""
        elif name == "act:id" and self.stack[-1] == "gnc:account":
            self.bufAcc.id = self.txt
            self.txt = ""
        elif name == "act:type" and self.stack[-1] == "gnc:account":
            self.bufAcc.type = self.txt
            self.txt = ""
        elif name == "act:commodity" and self.stack[-1] == "gnc:account":
            self.txt = ""
        elif name == "act:parent" and self.stack[-1] == "gnc:account":
            self.bufAcc.parent = self.txt
            self.txt = ""

        elif name == 'cmdty:space' and self.stack[-1] == 'act:commodity':
            self.txt = ""

        elif name == 'cmdty:id' and self.stack[-1] == 'act:commodity':
            self.bufAcc.account_currency = self.txt[-3:]
            self.txt = ""

        elif name == "cmdty:id" and self.stack[-1] == "trn:currency":
            self.bufTrans.currency = self.txt
            self.txt = ""
        elif name == "ts:date" and self.stack[-1] == "trn:date-posted":
            self.bufTrans.date = self.txt
            self.txt = ""

        elif name == "trn:description" and self.stack[-1] == "gnc:transaction":
            self.bufTrans.desc = self.txt
            self.txt = ""
        elif name == "trn:num" and self.stack[-1] == "gnc:transaction":
            self.bufTrans.num = self.txt
            self.txt = ""

        elif name == "split:reconciled-state": # and self.stack[-1] == "trn:split":
            self.bufSplit.reconciled_state = self.txt
            self.txt = ""

        elif name == "split:value" and self.stack[-1] == "trn:split":
            self.bufSplit.val = self.txt
            self.txt = ""
        elif name == "split:account" and self.stack[-1] == "trn:split":
            self.bufSplit.acc = self.txt
            self.txt = ""
        elif name == "split:action" and self.stack[-1] == "trn:split":
            self.bufSplit.action = self.txt
            self.txt = ""
        elif name == "split:memo" and self.stack[-1] == "trn:split":
            self.bufSplit.memo = self.txt
            self.txt = ""

        elif name == 'trn:id':
            assert len(self.txt) == 37
            self.bufTrans.trn_id = self.txt[5:]
            self.txt = ''

        else:
            self.txt = ''
            self.unused.add(name)


class Container:
    def strip(self):
        for x in dir(self):
            if "__" not in x:
                a = getattr(self, x)
                if isinstance(a, str):
                    a = a.strip()
                    setattr(self, x, a)
