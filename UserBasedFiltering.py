# -*- coding: utf-8 -*-
"""
Mining Assignment 1
"""

import math

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # metric:
    # metric is in the form of a string. it can be any of the following:
    # "minkowski", "cosine", "pearson"
    #     recall that manhattan = minkowski with r=1, and euclidean = minkowski with r=2
    # defaults to "pearson"
    #
    # r:
    # minkowski parameter
    # set to r for minkowski, and ignored for cosine and pearson
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    def __init__(self, usersItemRatings, metric='pearson', r=1, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings

        # set self.metric and self.similarityFn
        if metric.lower() == 'minkowski':
            self.metric = metric
            self.similarityFn = self.minkowskiFn
        elif metric.lower() == 'cosine':
            self.metric = metric
            self.similarityFn = self.cosineFn
        elif metric.lower() == 'pearson':
            self.metric = metric
            self.similarityFn = self.pearsonFn
        else:
            print ("    (DEBUG - metric not in (minkowski, cosine, pearson) - defaulting to pearson)")
            self.metric = 'pearson'
            self.similarityFn = self.pearsonFn
        
        # set self.r
        if (self.metric == 'minkowski'and r > 0):
            self.r = r
        elif (self.metric == 'minkowski'and r <= 0):
            print ("    (DEBUG - invalid value of r for minkowski (must be > 0) - defaulting to 1)")
            self.r = 1
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (DEBUG - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            
    
    #################################################
    # minkowski distance (dis)similarity - most general distance-based (dis)simialrity measure
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def minkowskiFn(self, userXItemRatings, userYItemRatings):
        
        distance = 0
        commonRatings = False 
        
        for item in userXItemRatings:
            # inlcude item rating in distance only if it exists for both users
            if item in userYItemRatings:
                distance += pow(abs(userXItemRatings[item] - userYItemRatings[item]), self.r)
                commonRatings = True
                
        if commonRatings:
            return round(pow(distance,1/self.r), 2)
        else:
            # no ratings in common
            return -2

    #################################################
    # cosince similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def cosineFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
        if denominator == 0:
            return -2
        else:
            return round(sum_xy / denominator, 3)

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                n += 1
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
       
        if n == 0:
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
        
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
         
        user_dist = {}      # stores the distance between the userX and other users
        song_data = self.usersItemRatings    # brings the dataset into song_data
        
        # passing the user disctionaries into the distance functions       
        for user_name in sorted(song_data.keys()):
             if userX != user_name:
                 dist = self.similarityFn(song_data[userX], song_data[user_name])
                 user_dist[user_name] = dist    
                 
        # stores the calculated distace in a sorted order of higher to lower   
        sorted_user_dist = sorted(user_dist.items(), key=lambda x: x[1], reverse=True)
        
        # stores the items and the corresponding ratings for Veronica in a list
        userX_list = [(k,v) for k,v in song_data[userX].items()]    
        
        
        # Recommendation function for Minkowski, Cosine, and Pearson (k=1)
        def calc(user_match):
            user_list = [(k,v) for k,v in song_data[user_match[0]].items()]    # stores the items and the corresponding ratings for the user that matched
            counter = 0
            temp_list=[]    # temporary list to store the final recommendations
            for i in range(len(user_list)):
                for j in range(len(userX_list)):
                    if user_list[i][0] == userX_list[j][0]:
                        counter += 1
                if (counter==0):
                    temp_list.append(user_list[i])
                counter = 0
            # this return statement sends the value back to the metric from where it was called     
            return(sorted(temp_list))
        
        # Minkowski Recommendation
        if self.metric == 'minkowski':
            user_match = sorted_user_dist[len(sorted_user_dist)- 1]
            return calc(user_match)     # calls the function calc and returns the received value to CollaborativeFilteringUBF (main)
            
        
        # Cosine Recommendation
        if self.metric == 'cosine':
            user_match = sorted_user_dist[0]
            return calc(user_match)          # returns the value to CollaborativeFilteringUBF (main)
        
        
        if self.metric == 'pearson':
            # Pearson Recommendation
            if self.k ==1:
                user_match = sorted_user_dist[0]
                return calc(user_match)      # returns the value to CollaborativeFilteringUBF (main)
            
            # KNN Recommendation
            if self.k >1:               
                user_weight_dict = {}     # used to store the weights of each user's ratings
                influence_deno = 0
                reco_item = []              # used to store the items that can be recommended to Veronica 
                user_match_dict = dict(sorted_user_dist [:self.k])           # used to store the details of the k nearest neighbour    
                
                # from line 229 to line 234, the user rating weights are being calculated                
                for i in sorted(user_match_dict.keys()):
                    user_match_dict[i] = (user_match_dict[i] + 1) / 2
                    influence_deno += user_match_dict[i]
                for i in sorted(user_match_dict.keys()):
                    user_weight_dict[i] = (user_match_dict[i] / influence_deno)
                
                # from line 237 to 240, the items that have to be submitted are being stored a separate list
                for user_match in user_match_dict.keys():
                    for item_match in song_data[i].keys():
                        if item_match not in song_data[userX]:
                            reco_item.append(item_match)
                            
                reco_item_set = set(reco_item)      # To remove duplicates the list is converted to a set
                
                # This is where the weights are being used to calculate the combined rating for an item
                sorted_user_weight_dict = sorted(user_weight_dict.items(), key=lambda x: x[1], reverse=True)
                final_dict = {}
                for i in reco_item_set:
                    counter = 0              
                    for j in range(len(sorted_user_weight_dict)):
                        for k in song_data.keys():                     
                            if sorted_user_weight_dict[j][0] ==k:                           
                               for v in song_data[k].keys():                              
                                   if v == i:                                                                     
                                       counter += sorted_user_weight_dict[j][1] * song_data[k][i]
                    final_dict[i] = round(counter,2)          # This dictionary had the recommendations along with the KNN score   
                    
                # returns the value to the CollaborativeFilteringUBF after the dictionary is sorted and stored in a list.
                return(sorted(final_dict.items(), key=lambda x: x[1], reverse=True))            
                                
                  
                                
                    
                    
                    
                       
                    
                                
                    
                                
            
        
        
          
        
                
                
            
            
        
        
            
    
        
        
        
        
        
            
            
                
#        
         
         
     
                

                
                        
                        
                        
                
        
        
        
        
        
             
            
            
       
    
        



        
