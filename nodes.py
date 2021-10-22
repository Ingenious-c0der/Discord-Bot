
import os
from PIL import Image, ImageDraw, ImageFont
import random
import sys
import string
import PIL
import asyncio
class Graph():
 
    def __init__(self, vertices,graph):
        self.V = vertices
        self.graph = graph
 



    async def minDistance(self, dist, sptSet):
 
        min = sys.maxsize
 
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
    async def dijkstra(self, src , end):
 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
            u = await self.minDistance(dist, sptSet)
            sptSet[u] = True
            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
 
        
        
        for node in range(self.V):
            if node==end:
                return dist[node]
 
class DrawNodes:

    async def drawer()->tuple[Image.Image,tuple[str,str],int]:
        """Returns the node structure image with the two selected nodes and shortest path between them
        Args : None
        Returns : tuple (pil image,(node1,node2),shortest_distance)
        """
        base_image = Image.open(os.path.join(os.getcwd(),"node_structure.png"))
        font = ImageFont.truetype("OpenSans-Regular.ttf", 35)
        draw_object = ImageDraw.Draw(base_image)
        letter_list=random.sample(string.ascii_uppercase,7)
    
        #node names
        pre_nodes = [0,1,2]
        post_nodes = [4,5,6]
        nodes = [random.choice(pre_nodes) ,random.choice(post_nodes)]
        node_color = (255,0,0)       
        value_color = (0,255,0)    
        draw_object.multiline_text((60,50), letter_list[0], font=font, fill=node_color)     #alpha
        draw_object.multiline_text((165,155), letter_list[1], font=font, fill=node_color)   #beta
        draw_object.multiline_text((150,370), letter_list[2], font=font, fill=node_color)   #gamma
        draw_object.multiline_text((350,140), letter_list[3], font=font, fill=node_color)   #delta
        draw_object.multiline_text((360,370),letter_list[4], font=font, fill=node_color)    #zeta
        draw_object.multiline_text((540,220), letter_list[5], font=font, fill=node_color)   #mu
        draw_object.multiline_text((725,155), letter_list[6], font=font, fill=node_color)   #epsilon


        #node values
        generated_values = x = [str(random.choice([197,145,189,123,144,146,"X"])) for i in range(12)]
        v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12 = generated_values
        draw_object.multiline_text((80,180), v1, font=font, fill=value_color)
        draw_object.multiline_text((100,100), v2, font=font, fill=value_color)
        draw_object.multiline_text((205,95), v3, font=font, fill=value_color)
        draw_object.multiline_text((257.5,147.5), v4, font=font, fill=value_color)
        draw_object.multiline_text((157.5,262.5), v5, font=font, fill=value_color)
        draw_object.multiline_text((250,255), v6, font=font, fill=value_color)
        draw_object.multiline_text((255,370), v7, font=font, fill=value_color)
        draw_object.multiline_text((355,255), v8, font=font, fill=value_color)
        draw_object.multiline_text((445,180), v9, font=font, fill=value_color)
        draw_object.multiline_text((537.5,147.5), v10, font=font, fill=value_color)
        draw_object.multiline_text((632.5,187.5), v11, font=font, fill=value_color)
        draw_object.multiline_text((450,295), v12, font=font, fill=value_color)

        safe_list = []
        for i in generated_values:
            if i=="X":
                safe_list.append(0)
            else:
                safe_list.append(int(i))


        v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12 = safe_list
        g = Graph(7,[[0,v2,v1,v3,0,0,0],
            [v2,0,v5,v4,0,0,0],
            [v1,v5,0,v6,v7,0,0],
            [v3,v4,v6,0,v8,v9,v10],
            [0,0,v7,v8,0,v12,0],
            [0,0,0,v9,v12,0,v11],
            [0,0,0,v10,0,v11,0]])
        shortest_dist =  await g.dijkstra(nodes[0],nodes[1])
        return (base_image,(letter_list[nodes[0]],letter_list[nodes[1]]),shortest_dist)


