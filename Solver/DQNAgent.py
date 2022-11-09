import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # supress tensorflow warnings

from Game import config
from Game.Tetris import Tetris
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from collections import deque
import numpy as np
import random
from random import choice

REPLAY_MEMORY_SIZE= 512
BATCH_SIZE= 512
UPDATE_TARGET_EVERY=50
DISCOUNT=0.9
EPSILON_START_VALUE = 0.8

class DQNAgent:
    def __init__(self,game:Tetris):
        self.game=game

        # observation is the game field
        self.observation_space = (config.width,config.height, 1)

        # actions are the 4 keys
        self.action_space = 3

        #main  get trained evert batch
        # self.model=self.createModel()
        self.model = load_model("Solver/models/target_model.h5")

        #target predicts every step
        self.targetModel= self.createModel()
        self.targetModel.set_weights(self.model.get_weights())

        # for each step we need to keep track of (observation, action, reward, newObservation, done) we call this a transiton
        self.replayMemory = deque(maxlen=REPLAY_MEMORY_SIZE)
        
        self.targetUpdateCounter=0
        self.current_highest_level = 0
        self.train_every = config.height
        self.train_counter = 0

        self.epsilon = EPSILON_START_VALUE



    #creates model for training and predicting
    def createModel(self):
        model = Sequential()
    
        model.add(Conv2D(32,(3,3), input_shape=self.observation_space))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(0.3))
        
        model.add(Conv2D(16,(3,3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(0.3))
        
        model.add(Flatten())
        model.add(Dense(32,activation='relu'))   
        model.add(Dense(self.action_space, activation="linear"))
        model.compile(loss="mse", optimizer='rmsprop', metrics=['accuracy'])
        return model


    #getting actions
    def getAction(self, observation):
        #observation is a (W,H) matrix. We add an extra dimension at the end and predict
        if(np.random.random()>self.epsilon):
            preds = self.targetModel.predict(np.expand_dims(observation, 0))[0]
            return np.argmax(preds)
        else:
            rand = choice(list(np.arange(self.action_space)))
            return rand
    
     #adds transitions to replay memory for training later
    def updateReplyMemory(self, trainsition):
        self.replayMemory.append(trainsition)
    

    #main train function
    def train(self):
        if(len(self.replayMemory) < BATCH_SIZE):
            return
        
        minibatch= random.sample(self.replayMemory, BATCH_SIZE)
        
        observations = np.array([transition[0] for transition in minibatch])

        currentQsList= self.targetModel.predict(observations)
        
        newObservations= np.array([transition[3] for transition in minibatch])

        futureQsList = self.targetModel.predict(newObservations)

        x=[]
        y=[]
        for index,(observation, action, reward, _, done) in enumerate(minibatch):
            if not done:
                maxFututeQ= np.max(futureQsList[index])
                newQ= reward+ DISCOUNT * maxFututeQ
            else:
                newQ= reward
            
            currentQs= currentQsList[index]
            currentQs[action]= newQ
            
            x.append(observation)
            y.append(currentQs)
        
        self.model.fit(np.array(x), np.array(y),batch_size=BATCH_SIZE,verbose=0,shuffle=False)
        

        self.targetUpdateCounter+=1
            
            
        if self.targetUpdateCounter>UPDATE_TARGET_EVERY:
            print('target updated!')
            self.targetModel.set_weights(self.model.get_weights())
            self.targetUpdateCounter=0
            self.targetModel.save('Solver/models/target_model.h5')
        

    def step(self,action):
        ((full_lines, highest_level, impact_point_level, count_holes), done) = self.game.step(action)
        reward = 0
        if(done):
            reward = -100 # maximum negative reward if game lost
        elif(full_lines!=0):
            reward = 2 * full_lines * config.width # if lines removed 1 point per pixel removed
            self.current_highest_level = highest_level # reset highest level
        else:
            if(highest_level>self.current_highest_level):
                self.current_highest_level = highest_level # negative reward for every high level
                reward = 0 # -highest_level  # <------------------------------------------------------------------------ CHANGE from 0
            else:
                if(impact_point_level!=-1):
                    reward =  highest_level - impact_point_level
        new_observation=self.game.get_observation()
        self.train_every = highest_level
        self.train_counter +=1
        return new_observation,reward,done
    

    def reset(self):
        self.game.start_new_game()
        self.current_highest_level = 0
        self.train_every = config.height
        return self.game.get_observation()

    def solve(self,total_games=150_000):
        start_decay=0
        end_decay=total_games//4
        
        epsilon_decay_value=self.epsilon/(end_decay-start_decay)
        
        for episode in range(total_games):
            episode_reward = 0
            observation = self.reset()
            print(f"game number {episode}")
            done = False
            while not done:
                action = self.getAction(observation)
                
                new_observation, reward, done = self.step(action)
                episode_reward += reward
                self.updateReplyMemory(
                    (observation, action, reward, new_observation, done)
                )

                observation = new_observation
                if(self.train_counter>self.train_every):
                    self.train()    
                    self.train_counter = 0
            if(end_decay>=episode >=start_decay):
                self.epsilon *=epsilon_decay_value
        
            print('score for this episode is ',self.game.score,'reward for this episode', episode_reward)
            print()
        
        self.model.save('Solver/models/DQN.h5')
        self.final_sol()
    
    def final_sol(self):
        self.epsilon = 0
        observation = self.reset()
        while self.game.running:
            action=self.getAction(observation)  
            observation, _, done=self.step(action)
            if(done):
                break