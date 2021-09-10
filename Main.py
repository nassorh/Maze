#Maze Genertor
import pygame,random
import time
import sys

__author__ = "Hamad Nassor"
__maintainer__ = "Hamad Nassor"
__email__ = "nassorh.dev@gmail.com"

class Maze():
    """
    Maze class to repesent the maze as a graph using
    edges(walls) and vertices(cells)

    self.vertices -> Dictonary that contains all of the vertices in form of coor:Cell
    """
    def __init__(self):
        self.vertices = dict()

    def getVertex(self,x,y):
        """
            Fetches a vertex from self.vertices

            Parameters:
                X(int): X coor
                Y(int): Y coor

            Returns:
                Cell: if exist returns a Cell object
                None: if the vertex does not exists
        """
        return self.vertices.get((x,y))
    def add_cell(self,c):
        """
            Adds a cell to the graph

            Parameters:
            C (Cell): A cell object being added to the graph

            Returns:
            Boolean:True if the cell has been added
                    False if the cell was not added since it isn't an instance of Cell class or already exists in the graph

       """
        if isinstance(c,Cell) and c.coor not in self.vertices:
            self.vertices[c.coor] = c
            return True
        else:
            return False
    
    def add_edge(self,u,v):
        """
            Creates and edge between cells by adding them to self.neigbours array
            in the cell class

            Parameters:
            U (Cell): First Cell object 
            V (Cell): Second Cell object

            Returns:
            Boolean:True if the edge has been added
                    False if the edge was not added since the cell does not already exists in the graph

       """
        if u.coor in self.vertices and v.coor in self.vertices:
            self.vertices[u.coor].add_neighbour(v)
            self.vertices[v.coor].add_neighbour(u)
            return True
        return False

    def __str__(self):
        """
            Prints the graph in the form of an adjacency list

            Returns:
            String: a string with the format of:
                 ( 0 ,   0 ) 	 ( 1 ,   0 ) ( 0 ,   1 ) 
                 ( 0 ,   1 ) 	 ( 0 ,   0 ) ( 1 ,   1 ) ( 0 ,   2 ) 

       """
        string =""
        for x in self.vertices.values():
            string+="\n"+str(x.coor)+"\t"
            for v in x.neighbours.keys():
                string+=str(v.coor)
        return " ".join(string)

    def dfsMazeGen(self):
        """
            Using dfs this is used to create the maze.

            Starting pos is (0,0)
            Starting pos is then append to queue
            Starting pos is then marked as visited
            Colour of starting pos is changed
                while the stack is not empty
                    current = stack.pop
                    All neighbours are fetched 
                    A random neigbour is chosen and added to the stack, current is added back the stack since not all neighbour nodes have been visited
                    The wall between current and random neighbour is removed
                    Neigbour is marked as visited and added to the stack
                Graphics updated

        
            Returns:
            Boolean:True maze has been generated

       """
        stack = []
        visited = dict()
        
        #Starting node, marked visited and pushed to stack
        current = self.getVertex(0,0)
        stack.append(current)
        visited[current] = True
        
        while len(stack)>0:
            #Current cell
            current = stack.pop()
            #Fetch neigbours which have not been visited yet
            neighbours = [x for x in current.neighbours.keys() if visited.get(x) != True]
            
            if(len(neighbours)>0):
                stack.append(current)#Adds the current back to the stack
                

                #Fetches the random neigbour and wall
                index = random.randint(0,len(neighbours)-1)#Picks a random index
                unvisitedNeigbour = neighbours[index]
                unvisitedNeigbourWall = current.neighbours.get(unvisitedNeigbour)

                #Removes the wall and sets the next cell that will be visited to true, then adds it to the stack
                current.removeWall(unvisitedNeigbour,unvisitedNeigbourWall)
                visited[unvisitedNeigbour] = True
                stack.append(unvisitedNeigbour)
            pygame.display.flip()#Updates the graphic
        return True
            
    def bfsSolver(self):
        """
            Using bfs to find the shorest path

            Empty dict with all visted (Cell:Visted->Boolean) cells set to and all parents set to false (Cell:Parent->Cell)
            
            Starting pos is then append to queue
            Starting pos is then marked as visited
            Colour of starting pos is changed
            
                while the stack is not empty
                    current = queue.pop(0) -> queue.dequeue
                    Checks if the bottom right corner is found if so
                        Find the shoresPath
                        Then draw the shorestPath
                    All neighbours are fetched 
                        If the neigbour is not marked as visited and has no wall blocking(meaning we can enter the block)
                        marked as visited and add to queue
                        update colour of visted cell

        
            Returns:
            Boolean:  True if a path has been found
                      False if a path has not been found

       """
        queue = []
        visited = dict()
        parent = dict()
        #level = dict() Used to measure how far the node is 

        for vertex in self.vertices.values():
            visited[vertex]=False #Cell:False
            parent[vertex]=None #Cell:None
            #level[vertex]=-1 Cell:-1
        
        current = self.getVertex(0,0)
        queue.append(current)
        visited[current]=True
        #level[current]=0#Sets the start pos level 0
        ui.updateCol(current)

        while len(queue) > 0:
            current = queue.pop(0)
            ui.updateCol(current)
            
            #If Exit is found we no longer need to con the search
            if current == self.getVertex(x-1,y-1):
                        shorestPath = self.createShortestPath(parent,self.getVertex(x-1,y-1))#Creates the shorest path
                        time.sleep(0.01)
                        ui.removeAllColBlocks(visited)
                        ui.colourPath(shorestPath)#Draws the shorest path
                        return True
            for neighbour,wall in current.neighbours.items():
                if visited.get(neighbour) != True and wall==None:
                    visited[neighbour] = True
                    queue.append(neighbour)
                    parent[neighbour] = current#Neigbour parent is set to the current
                    #level[neighbour] = level[current]+1#Sinces its the child of currrent level = currentLevel+1
                    ui.updateCol(current)
                    time.sleep(ui.SPEED)
        return False       

    def createShortestPath(self,parent,cell):
        """
            Used to construct the shorest path

            Using the parent array which contains the cell and the parent in which the bfs traversal from, None values are used to represent no other parent cell.
            while cell is not None 
                append the cell coor to the shorest path array
                then fetch the current cell parten
            check if last first element is cell (0,0) 
                if true
                    path.reverse() since we have worked backwards meaning the array is backwards
                else
                    assume no path was found
            
            Parameters:
                parent (dict): Parent dictonary which containts the Cell:Parent
                node (Cell): End node(Starting node can always be assumed as (0,0)

            Returns:
                Array:Shorest path from 0,0 to node
                None: if no path was found

       """
        path = []
        while cell is not None:
            path.append(cell.coor)
            cell = parent.get(cell)
        if path[-1] == (0,0):
            path.reverse()
            return path
        else:
            None
        
            
class Cell():
    """
    Cell class which reprensents all cells as vertices

    self.coor(Tuple) -> Contains the abstacr coor of the cell
    self.neighbours(Dict) -> Contains all of the vertices in form of Cell:wall
    """
    def __init__(self,x,y):
        self.coor=(x,y)
        self.neighbours = dict() #neightbour:wall 

    def add_neighbour(self,v,wall=None):
        """
            Adds neighbour to the cell when creating an edge and the corresponding wall blocking the cell and the neighbour by defual no walls are blocking 
            
            Parameters:
                v (Cell): Cell object
                wall (array): Array contain tuple values of the starting and end postion coor for the wall

            Returns:
                Boolean:True if the neighbour has been added

       """
        if v not in self.neighbours:
            self.neighbours[v]=wall
            return True
            
    def removeWall(self,n,wall):
        """
            Sets the neigbour wall to none for both self and neighbour since its bidirectonal also envokes removeLine method in the UI to remove the line drawing
            
            Parameters:
                n (Cell): Cell object
                wall (array): Array contain tuple values of the starting and end postion coor for the wall

            Returns:
                Boolean:True if the wall has been removed

       """
        if n !=None and wall != None:
            self.neighbours[n] = None
            n.neighbours[self] = None
            if ui.removeLine(wall): return True
            
    
class UI():
    """
        UI class hanldes all the graphic

        self.WIDTH(int)         --> Width of window
        self.HEIGHT(int)        --> Height of window
        self.WHITE(Tuple)       --> Value of RGB white
        self.VISITEDCOL(Tuple)  --> Value of RGB white
        self.CURRENTCOL(Tuple)  --> Value of RGB white
        self.CELLWIDTH(int)     --> Cell width
        self.CELLHEIGHT(int)    --> Cell heihgt
        self.LINESIZE(int)      --> Line thickness
        self.SPEED(int)         --> Speed of loading
        self.Screen             --> Screen object
    """
    def __init__(self):
        #Variables
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.WHITE=(255,255,255)
        self.VISITEDCOL = (255, 0, 0)
        self.CURRENTCOL = (255,160,122)
        self.CELLWIDTH = self.WIDTH/x
        self.CELLHEIGHT = self.WIDTH/y
        self.LINESIZE = 1
        self.SPEED = 1
        #Screen
        self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT),0,32)
    
    def drawOuterWall(self):
        """
            Draws the outer wall of the maze which is constant
        
            Returns:
                Boolean:True if the wall has drawn

       """
        topleft = (0,0)
        topright = (self.WIDTH,0)
        bottomleft = (0,self.HEIGHT)
        bottomright = (self.WIDTH,self.HEIGHT)
        pygame.draw.line(self.screen,(0,0,255),topleft,topright,self.LINESIZE)
        pygame.draw.line(self.screen,(0,0,255),topleft,bottomleft,self.LINESIZE)
        pygame.draw.line(self.screen,(0,0,255),topright,bottomright,self.LINESIZE)
        pygame.draw.line(self.screen,(0,0,255),bottomleft,bottomright,self.LINESIZE)
        return True
    

    def createWall(self):
        """
            Creates all the inital walls for every cell.

            Loops through all the vertices in maze
                loops through all the neighbours
                    checks the direction using the coors then draw the approate wall by fetching the cells top left x and y axis w/ abit of maths 
    
            Returns:
                Boolean:True if the wall has been drawm

       """
        #Loop through all vertices
        for cell in maze.vertices.values():
            #Loop through all the neigbours
            for neighbour,wall in cell.neighbours.items():
                #Helper variables  
                cellX =cell.coor[0]
                cellY=cell.coor[1]
                if cellX+1 == neighbour.coor[0]:
                    topright = ((cellX*self.CELLWIDTH)+self.CELLWIDTH,cellY*self.CELLHEIGHT)
                    bottomright= ((cellX*self.CELLWIDTH)+self.CELLWIDTH,(cellY*self.CELLHEIGHT)+self.CELLHEIGHT)
                    line =[topright,bottomright]#Stores pos in array to be passed
                    pygame.draw.line(self.screen,(0,0,0),line[0],line[1],self.LINESIZE)#Creates right wall
                    cell.neighbours[neighbour] = line#Stores the wall that needs removing when edge is broken
                if cellX-1 == neighbour.coor[0]:
                    topleft = (cellX*self.CELLWIDTH,cellY*self.CELLHEIGHT)
                    bottomleft = (cellX*self.CELLWIDTH,(cellY*self.CELLHEIGHT)+self.CELLHEIGHT)
                    line =[topleft,bottomleft]#Stores pos in array to be passed
                    pygame.draw.line(self.screen,(0,0,0),line[0],line[1],self.LINESIZE)#Creates left wall
                    cell.neighbours[neighbour] = line#Stores the wall that needs removing when edge is broken
                if cellY+1 == neighbour.coor[1]:
                    bottomleft = (cellX*self.CELLWIDTH,(cellY*self.CELLHEIGHT)+self.CELLHEIGHT)
                    bottomright= ((cellX*self.CELLWIDTH)+self.CELLWIDTH,(cellY*self.CELLHEIGHT)+self.CELLHEIGHT)
                    line =[bottomleft,bottomright]#Stores pos in array to be passed
                    pygame.draw.line(self.screen,(0,0,0),line[0],line[1],self.LINESIZE)#Creates bottom wall
                    cell.neighbours[neighbour] = line#Stores the wall that needs removing when edge is broken
                if cellY-1 == neighbour.coor[1]:
                    topleft = (cellX*self.CELLWIDTH,cellY*self.CELLHEIGHT)
                    topright = ((cellX*self.CELLWIDTH)+self.CELLWIDTH,cellY*self.CELLHEIGHT)
                    line =[topleft,topright]#Stores pos in array to be passed
                    pygame.draw.line(self.screen,(0,0,0),line[0],line[1],self.LINESIZE)#Creates top wall
                    cell.neighbours[neighbour] = line#Stores the wall that needs removing when edge is broken
        return True
                    
    def removeLine(self,line):
        """
            Removes the wall by drawing over it again in white
            
            Parameters:
                line (Array): Array contain tuple values of the starting and end postion coor for the wall 

            Returns:
                Boolean:True if the wall has been removed

       """
        pygame.draw.line(self.screen,(255,255,255),line[0],line[1],self.LINESIZE)
        return True

    def updateCol(self,vertex):
        """
            Updates the colour of the cell
            
            Parameters:
                vertex (Cell): Cell object

            Returns:
                Boolean: True if colour has bee updated

       """
        topLeftX = vertex.coor[0]*ui.CELLWIDTH
        topRightY = vertex.coor[1]*ui.CELLHEIGHT
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(topLeftX+1, topRightY+1, ui.CELLWIDTH-1, ui.CELLHEIGHT-1))
        pygame.display.flip()
        return True
    
    def colourPath(self,nodesToCol):
        """
            Colours the path of the 
            
            Parameters:
                nodesToCol (Array): Array of coor to colour

            Returns:
                Boolean: True if path has been drawn

       """        
        for x in nodesToCol:
            topLeftX = x[0]*self.CELLWIDTH
            topRightY = x[1]*self.CELLHEIGHT
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(topLeftX+1, topRightY+1, ui.CELLWIDTH-1, ui.CELLHEIGHT-1))
            pygame.display.flip()
        pygame.display.update()
        return True

    def removeAllColBlocks(self,visitiedNode):
        """
            Removes all the coloured blocks and resets the maze back to normal
            
            Parameters:
                visitiedNode (dict): All cell that have been coloured

            Returns:
                Boolean: True if path has been drawn

       """ 
        for x in visitiedNode.keys():
            topLeftX = x.coor[0]*self.CELLWIDTH
            topRightY = x.coor[1]*self.CELLHEIGHT
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(topLeftX+1, topRightY+1, ui.CELLWIDTH-1, ui.CELLHEIGHT-1))
        pygame.display.flip()
        return True

class Helper():
    """
    Helper Class
    """
    def createCells(x,y):
        """
            Creates all the cells
            
            Parameters:
                x(int) number of rows
                y(int) number of column

            Returns:
                Boolean: True if path has been drawn

       """ 
        for a in range(x):
            for b in range(y):
                cell = Cell(a,b)
                maze.add_cell(cell)
        return True
    def createAllEdges():
        """
            Connects all the cells together
            
            Returns:
                Boolean: True if path has been drawn

       """ 
        for cell in maze.vertices.values():
            left  = (cell.coor[0]-1,cell.coor[1])
            right = (cell.coor[0]+1,cell.coor[1])
            top   = (cell.coor[0],cell.coor[1]-1)
            down  = (cell.coor[0],cell.coor[1]+1)
            if maze.vertices.get(left) != None:
                maze.add_edge(cell,maze.vertices.get(left))
            if maze.vertices.get(right) != None:
                maze.add_edge(cell,maze.vertices.get(right))
            if maze.vertices.get(top) != None:
                maze.add_edge(cell,maze.vertices.get(top))
            if maze.vertices.get(down) != None:
                maze.add_edge(cell,maze.vertices.get(down))
        return True
if __name__ =="__main__":
    
        
            
    #print("{} left: {} right: {} top: {} down: {}".format(cell.coor,left,right,top,down))
    maze =Maze()
    x = int(input("Enter the number of columns: "))
    y = int(input("Enter the number of rows: "))
    Helper.createCells(x,y)#Creates all the cells
    Helper.createAllEdges()#Connects all the cells together
    
    ui = UI()#Loads the UI
    #Set Up Screen
    pygame.init()
    ui.screen.fill(ui.WHITE)
    ui.drawOuterWall()#Draws the outer wall
    ui.createWall()#Creates all the inital walls the outer wall
    maze.dfsMazeGen()
    maze.bfsSolver()
    print(maze)
    
    #Main While loop
    while True:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:#Exits when x clicked
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
