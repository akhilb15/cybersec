from pwn import *

'''
example maze output:

<<< Maze 1
 ##################
 #o              ##
 # ### ### ##### ##
 #   #   #     # ##
 # # # ######### ##
 # # #       # # ##
 # # # # ##### ####
 # # # #         ##
 # ### ### # # ####
 # # #   # # #   ##
 # # # # ####### ##
 #   # #       # ##
 # # # ##### ######
 # # #     # # # ##
 ### ######### # ##
 #              E##
 ##################
 ##################
             End >>>


L R U D
'''

conn = remote('chal.sigpwny.com', 3502)

conn.recvline()
conn.recvline()

# there are 1000 mazes
for i in range(1000):
    # read the maze
    print(conn.recvline())
    maze = []
    # while the line is does not contain end
    while (line := conn.recvline()).decode().find('End') == -1:
        maze.append([c for c in line.decode() if c != b'\n'])
        
    
    start = (-1, -1)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'o':
                start = (i, j)
                break
        
            
    # print the maze
    for row in maze:
        for col in row:
            print(col, end=' ')
        print()
    
    
    # solve the maze using dfs
    path = []
    visited = set()
    def dfs(i, j):
        if (i, j) in visited:
            return False
        if i < 0 or i >= len(maze) or j < 0 or j >= len(maze[i]):
            return False
        visited.add((i, j))
        if maze[i][j] == '#':
            return False
        if maze[i][j] == 'E':
            return True
        if dfs(i + 1, j):
            path.append('D')
            return True
        if dfs(i - 1, j):
            path.append('U')
            return True
        if dfs(i, j + 1):
            path.append('R')
            return True
        if dfs(i, j - 1):
            path.append('L')
            return True 
        return False
    
    dfs(start[0], start[1])
    path = ''.join(path[::-1])
    
    print(path)
    # send the path
    conn.sendline(path.encode())
    
conn.interactive()
    

    