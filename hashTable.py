import hashlib 
import Crypto.Random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
class Hash:
    def __init__(self ):
        self.table = {}

    def KeyHash(self,key):
        self.data = key.encode('utf-8')
        hash_obj = hashlib.new('sha256')
        hash_obj.update(self.data)
        self.hash1 = hash_obj.hexdigest()
        # np.random.seed(45)
        num = np.random.randint(2,10)
        return self.hash1[(len(self.hash1)//2)-3:(len(self.hash1)//2)+3]
        # return self.hash1[num-2:num+2]
    
    def InsertElement(self,userName,email,password):
        index = self.KeyHash(email)
        self.table[index] = [index ,userName , email,password]

    def Display(self):
        aa = []
        for i in self.table:
            aa.append(self.table[i])
        self.AllData = pd.DataFrame(aa , columns=['Index','UserName','Email','Password'])
        self.AllData = self.AllData.set_index(self.AllData['Index'])
        self.AllData = self.AllData.drop('Index',axis=1)
        print(self.AllData)
    def PlotGraph(self):
        fig = plt.figure(1)
        ax = fig.add_subplot(1,1,1)
        # Re-index to include the custom index title
        self.AllData.index.name = 'Index'
        table1 = ax.table(cellText=self.AllData.values,
                 colLabels=self.AllData.columns,
                 rowLabels=self.AllData.index,
                 cellLoc='center',
                 loc='center',
                 colColours=['#BBB09B']*self.AllData.shape[1],
                  cellColours=[['#f5f5f5' if i % 2 == 0 else '#e0e0e0' for j in range(self.AllData.shape[1])] for i in range(self.AllData.shape[0])]
        ) 
        # for (i, j), cell in table1._cells.items():
        #     if i == 0:  # Skip header row
        #         continue
        #     # Stripe row colors
        #     cell.set_facecolor(['#697565', '#3C3D37'][i % 2])

        # Remove borders for all cells
        for (i , j ) , cell in table1._cells.items():
            cell.set_edgecolor('none')  # Set edgecolor to 'none' to remove the border
        table1.auto_set_font_size(False) 
        table1.set_fontsize(10) 
        table1.auto_set_column_width(range(self.AllData.shape[1]))
        plt.show()
        




# hasher = hashlib.new('ripemd160')
# print(Crypto.Random.get_random_bytes(45).hex())
aa = Hash()
aa.InsertElement("vandy","5vandy@gamil.com","123321")
aa.InsertElement("dy","1vandy@gamil.com","123321")
aa.InsertElement("df","2vandy@gamil.com","123321")
aa.InsertElement("dg","4vandy@gamil.com","123321")
aa.InsertElement("jonh","helldy@gamil.com","123321")
aa.InsertElement("hasha","4vjonh@gamil.com","123321")
aa.InsertElement("haha","4v@gamil.com","123321")
aa.InsertElement("hello world","4afy@gamil.com","123321")
aa.InsertElement("wo","dfa@gamil.com","123321")
aa.InsertElement("d","kk@gamil.com","123321")
aa.InsertElement("df","hh@gamil.com","123321")
aa.Display()
print(np.random.randint(10))
print(aa.KeyHash('1'))
print(hashlib.algorithms_guaranteed)
aa.PlotGraph()

