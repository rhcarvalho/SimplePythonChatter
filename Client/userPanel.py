class userPanel:

    def __init__(self, treestore):
        self.treestore = treestore
        self.IDs = []

    def add (self, User):
        if self.IDs.count(User.ID) == 0:
            if int(User.ID) >= 1000:
                self.IDs.append(User.ID)
                name = self.treestore.append(None, ["  " + User.name])
                self.treestore.append(name, [" ID: " + User.ID])
                self.treestore.append(name, [" Known Since: " + str(User.knownsince)])

    def remove(self, User):
        for ID in self.IDs:
            if ID == User.ID:
                self.IDs.remove(ID)
                a = self.treestore.get_iter_first()
                go = True
                while go == True:
                    if a == None:
                        go = False
                    if self.treestore.get_value(a, 0) == "  " + User.name:
                        self.treestore.remove(a)
                        break
                    if not self.treestore.iter_is_valid(self.treestore.iter_next(a)):
                        break
                    a = self.treestore.iter_next(a)

    def clear(self):
        for ID in self.IDs:
            self.IDs.remove(ID)
        self.treestore.clear()
