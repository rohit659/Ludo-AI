from Strategy import *
from Attacking import *
from Defensive import *
from Escape import *
from Random import *
import tensorflow as tf
import numpy as np
from PIL import Image
import copy

class RLearning(Strategy):
    def __init__(self,name):
        Strategy.__init__(self,name)
        self.attack = Attacking("Attacking")
        self.defense = Defensive("Defensive")
        self.escape = Escape("Escape")
        self.randomm = Random("Random")

    def findState(self, colors,idx,noofplayers):
        
        lst=[]

        for i in range(4):
            for j in range(4):
                lst.append( (colors[i][j].pathindex+1)/57)
        
        lst.append(idx/(noofplayers-1))
        NPArr = lst
        return NPArr 

    def findnewState(self,colors,idx,x,face,noofplayers):

        pn=0

        if(colors[idx][x].pathindex!=-1):
            pn=colors[idx][x].pathindex+face+1 
        else:
            pn=1

        lst=[]

        for i in range(4):
            for j in range(4):
                if(i==idx and j==x):
                    lst.append(pn/57)
                else :     
                    lst.append( (colors[i][j].pathindex+1)/57)   

        if(face==6):
            newturn=idx
        else:
            newturn=(idx+1)%noofplayers             

        lst.append(newturn/(noofplayers-1))

        return lst
    
    # def getWorstAction(self,colors,idx,face,NPArr):
    #     j = 0
    #     qMin = 2
    #     for i in range(4):
    #         if colors[idx][i].ismovePossible(face):
    #             na = copy.deepcopy(NPArr)
    #             na.append(i)
    #             na.append(face)
    #             NArr = np.array(na)
    #             qMin = sess.run(tf.max(output_layer,1), feed_dict={X: NArr})
        



    def getCoinToMove(self,idx,colors,face,noofplayers):
        n_input = 19  # input layer 
        n_hidden = 8 # Hidden layer
        n_output = 1   # output layer, the Q - Value
        eps = 1.1
        alpha = 0.2
        gamma = 0.8

        tf.reset_default_graph()

        learning_rate = 1e-4
        dropout = 0.1

        X = tf.placeholder("float", [None, n_input])
        Y = tf.placeholder("float", [None, n_output])
        keep_prob = tf.placeholder(tf.float32)

        weights = {
            'w1': tf.Variable(tf.truncated_normal([n_input, n_hidden], stddev=0.1)),
            'out': tf.Variable(tf.truncated_normal([n_hidden, n_output], stddev=0.1))
        }

        biases = {
            'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden])),
            'out': tf.Variable(tf.constant(0.1, shape=[n_output]))
        }

        layer_1 = tf.add(tf.matmul(X, weights['w1']), biases['b1'])
        layer_drop = tf.nn.dropout(layer_1, keep_prob)
        output_layer = tf.matmul(layer_1, weights['out']) + biases['out']

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output_layer))
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

        correct_pred = tf.equal(tf.argmax(output_layer, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        saver = tf.train.Saver()

        init = tf.global_variables_initializer()
        sess = tf.Session()
        # sess.run(init)
        saver.restore(sess, "./tmp/model.ckpt")

        # Epsilon-greedy for Explore-Exploit Dilemma
        p = np.random.random()
        x = 0
        if p < eps:

            lst = []
            for i in range(4):
                if colors[idx][i].ismovePossible(face):
                    lst.append(i)
            x = choice(lst)
        else:
            qMax = -2.0
            j = 0
            NPArr = self.findState(colors,idx,noofplayers)
            for i in range(4):
                if colors[idx][i].ismovePossible(face):
                    na = copy.deepcopy(NPArr)
                    na.append(i)
                    na.append(face)
                    NArr = np.array(na)
                    if qMax < sess.run(output_layer, feed_dict={X: [NArr]}):
                        qMax = sess.run(output_layer, feed_dict={X: [NArr]})
                        j = i
            x = j
            
        NPArr = self.findnewState(colors,idx,x,face,noofplayers)
        j = 0
        qMin = 2
        for i in range(4):
            if colors[idx][i].ismovePossible(face):
                na = copy.deepcopy(NPArr)
                na.append(i)
                na.append(face)
                NArr = np.array(na)
                qMin = min(qMin,sess.run(output_layer, feed_dict={X: [NArr]}))
        print("Q-Value")

        # Update rule
        NPArr = self.findState(colors,idx,noofplayers)
        na = copy.deepcopy(NPArr)
        na.append(x)
        na.append(face)
        NArr = np.array(na)
        qprev = sess.run(output_layer, feed_dict={X: [NArr]})
        r = self.reward(idx,x,colors,face)
        qnew = qprev + alpha*(r+gamma*(qMin) - qprev)
        sess.run(train_step, feed_dict={X: [NArr], Y: qnew, keep_prob:dropout})
        print(np.squeeze(qprev))
        print(np.squeeze(qnew))
        # sess.run(tf.argmax(output_layer, 1), feed_dict={X: NPArr})
        save_path = saver.save(sess, "./tmp/model.ckpt")
        return x


    def getDangerLevel(self,idx,colors,face):
        dangerlist=[3,3,3,3]

        for coin in range(4):
            curx=colors[idx][coin].cur_x
            cury=colors[idx][coin].cur_y
            minn=1000
            if colors[idx][coin].ismovePossible(face)==0:
                dangerlist[coin]=-1
                continue
            cnt=0
            for i in range(4):
                if i== idx:
                    continue 
                for j in range(4):
                    pind=colors[i][j].pathindex
                    if pind == -1:
                        continue
                    maxpind=len(colors[i][j].path_list)
                    cnt=0
                    for k in range(pind,maxpind,1):
                        nx=colors[i][j].path_list[k][0]
                        ny=colors[i][j].path_list[k][1]
                        cnt+=1
                        if nx==curx and ny==cury:
                            minn=min(minn,cnt)
                            break

            if minn<=5 and (colors[idx][coin].pathindex==-1 or colors[idx][coin].path_list[colors[idx][coin].pathindex][2]==0) :
                dangerlist[coin]=0
            elif  minn <=11:
                dangerlist[coin]=1
            elif minn<=17:
                dangerlist[coin]=2
            else:
                dangerlist[coin]=3
                         
        return dangerlist
            
    def reward(self,idx,n,colors,face):
        pathini = colors[idx][n].pathindex
        dangerlist = self.getDangerLevel(idx, colors,face)
        prevdanger = dangerlist[n]
        pathind = colors[idx][n].pathindex + face


        cnt = 0
        # if won
        if(pathind == len(colors[idx][n].path_list)-1):
                return 1


        # realising a piece from jail
        if pathini == -1 and face == 6:
            return 0.25
        
        npos = colors[idx][n].pathindex + face
        if colors[idx][n].path_list[npos][2] == 1:
            return 0.35
        else:
            nx = colors[idx][n].path_list[npos][0]
            ny = colors[idx][n].path_list[npos][1]
            #  knocking an opponent’s piece
            for coin in range(0, 4):
                if coin != idx:
                    for i in range(0, 4):
                        if colors[coin][i].cur_x == nx and colors[coin][i].cur_y == ny:
                            cnt = cnt+1
            if cnt == 1:
                return 0.4

        colors[idx][n].pathindex  = colors[idx][n].pathindex + face
        colors[idx][n].cur_x = colors[idx][n].path_list[colors[idx][n].pathindex][0]
        colors[idx][n].cur_y = colors[idx][n].path_list[colors[idx][n].pathindex][1]

        dangerlist = self.getDangerLevel(idx, colors,face)
        currdanger = dangerlist[n]
        colors[idx][n].pathindex = colors[idx][n].pathindex - face
        colors[idx][n].cur_x = colors[idx][n].path_list[colors[idx][n].pathindex][0]
        colors[idx][n].cur_y = colors[idx][n].path_list[colors[idx][n].pathindex][1]
        # defending a vulnerable piece
        if prevdanger < currdanger :
            return ((currdanger-prevdanger)/3)*0.75
        # for getting a piece knocked in the next turn    
        elif prevdanger > currdanger:
            return -((prevdanger-currdanger)/3)*0.75  

        # forming a blockade
        cnt = 0
        for i in range(0, 4):
            if i != n:
                if colors[idx][i].pathindex == pathind:
                    cnt = cnt+1
        if cnt > 1:
            return 0.05

        #  moving the piece that is closest to home.
        return pathind/56  
    
     

        
        






