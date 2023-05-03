# Wilson's Maze Generator
<br/>

![mini_maze](https://user-images.githubusercontent.com/130370305/236062401-d68d7c2c-4d3b-469b-8184-c0456fdb7197.gif)
  
<br/>
Generate a random maze using Wilson's algorythm. 

<br/><br/>

**This was implemented purely as Python a learning experience.**


## Description:

Naive implementation of wilsons maze generation algorithm.

We pick start and finish cells at random and begin scouting: pick random direction, move to that cell and repeat until we reach the finish cell or any already visited cell.

While scouting we record in which direction we exit each cell. If we walk through the same cell again and exit in a different direction - we override stored direction for that cell.

After finish (or unvisited cell) is reached we go back to the start cell and use the recorded directions to build a path from start to finish. All other scouted cells which are not on the path will be scouted again on next iteration.

All the paths are stored as lists of coordinates and directions, so 'carving' boils down to iterating through each list, obtaining exit direction and coordinates of a grid cell and removing the cell 'wall' towards which the direction is pointing.
<br/><br/><br/>

<details>
  <summary>Animated Scouting</summary>
  
  <br/>
  
![scouting](https://user-images.githubusercontent.com/130370305/236021930-48fe284e-814b-4ba4-b914-249904847227.gif)

</details>

<br/><br/>

<details>
  <summary>Animated Carving</summary>
  
  <br/>
  
![carving](https://user-images.githubusercontent.com/130370305/236021738-1405fc98-4917-45cb-b26a-295c221df7c4.gif)

</details>

<br/><br/>

<details>
  <summary>Results</summary>
  
  <br/>
  
6x6 maze:
<br/><br/>
![00045_carving](https://user-images.githubusercontent.com/130370305/236026226-af8142e2-6103-437a-b729-acbb16f21bca.png)


120x120 maze:
<br/><br/>
![maze](https://user-images.githubusercontent.com/130370305/236067860-7ef52ed1-b6b2-4e8d-abb5-3706c31c963b.png)
 
 </details>



