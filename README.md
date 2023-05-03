# Wilson's Maze Generator

Generate a random maze using Wilson's algorythm. 


**This was implemented purely as Python a learning experience.**


## Description:

Naive implementation of wilsons maze generation algorithm.

We pick start and finish cells at random and begin scouting randomly: pick random direction, move to that cell and repeat until we reach the finish cell or any already visited cell.

During the scouting we record in which direction we exit each cell. If we walk through the same cell again and exit in a different direction - we override stored direction for that cell.

After finish is reached we go back to the start cell and use the recorded directions to build a path from start to finish.

All the paths stored are as lists of coordinates and directions, so 'carving' boils down to iterating through each list, obtaining exit direction and grid cell coordinates from each list item and removing one of the cell 'walls' towards which direction is pointing.
<br/><br/><br/>

Scouting (takes a while):
<br/><br/>
![scouting](https://user-images.githubusercontent.com/130370305/236021930-48fe284e-814b-4ba4-b914-249904847227.gif)

<br/><br/>

Carving:
<br/><br/>
![carving](https://user-images.githubusercontent.com/130370305/236021738-1405fc98-4917-45cb-b26a-295c221df7c4.gif)

<br/><br/><br/>

Result:
<br/><br/>
![00045_carving](https://user-images.githubusercontent.com/130370305/236026226-af8142e2-6103-437a-b729-acbb16f21bca.png)



