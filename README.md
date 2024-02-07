#Solar System Simulator
<h1>Description</h1>
This project contains code that simulates the solar system by solving the N-body problem with elastic collisions. It takes in real data from NASA as initial conditions (scaling radii up by 10) and lets the user explore the solar system as well as play with whatever features they want such as changing the simulation speed, changing collisions, adding objects, editing objects, etc.... 

<h3>Controls and Options</h3>
To control yourself you can use WASD to move left right forwards and backwards and then lshift and space to move down and up respectively. Pressing the "R" key will speed up your movement by a factor of 10. You can press I to instantly insert a small body in front of you. More importantly you can access the menu with M. In the menu you can change the speed the simulation runs at (although it will lag if you set it too fast). You can also change how fast you move in the simulation. 

If you switch to the entities menu you can add or edit objects in the simulation.

Editing: To edit an object simply click on its box and edit its parameters and then click edit and then when you leave the menu your changes will be applied.

Adding: If you want to add an entity use the up and down arrows (labeled "U" and "D" on the menu) to scroll down until you see the "+" button, pressing the button will let you set an objects position, velocity, radius, mass, name, and texture. You can add any texture you want as a jpg into the textures folder and then you can write its name in (NOTE: It is case insensitive so make sure if you add a texture the difference in filename is not due to casing). When you give position and velocity you can just write them in the format $(x,y,z)$ (parentheses and commas required). 

Teleporting: You can also select an object and click teleport so that when you exit the menu you will be teleported to the location of the object. 

<h3>Simulation Explanation</h3>
The simulation does an $O(N^2)$ gravity calculation and then integrates using a leapfrog technique, the largest times scaling allowed is 5000*realTime any larger than this and the simulation will just while loop through your timestep in these chunks. The purpose of this is to preserve accuracy. The leapfrog integration we use is drift-kick-drift. The scheme for going from some position $\vec{r}_n$ and velocity $\vec{v}_n$ to updated $\vec{r}_{n+1}$ and $\vec{v}_{n+1}$ after a timestep $h$ with acceleration determined by $f(\vec{r})$ is layed out below: 

$$\vec{r}_{n+1/2}=\vec{r}_n+\vec{v}\frac{h}{2}$$

$$\vec{v}_{n+1}=\vec{v}_n+hf(\vec{r}_n)$$

$$
\vec{r}\_{n+1}=\vec{r}\_{n+1&lowbar;2}+\frac{h}{2}\vec{v}\_{n+1}
$$

The advantage of this scheme is that it is symmetric which means if we let our evolution operator be represented by $\Gamma(h)$ that $\Gamma(-h)=\Gamma^{-1}(h)$. If we let $\mathrm{T}$ represent the time reversal operator that our scheme is normal which means $\mathrm{T}\Gamma(h)=\Gamma(-h)\mathrm{T}$. These are both conditions that we know hold for the exact solution of our ODE so when we force our numerical scheme to respect them we are able to respect the structure of our equations in some sense. To be more precise these conditions to ensure that our time evolution is handled respectfully allow us to stay on (or near) the symplectic manifold which our exact solution exists on thus preserving our energy better and giving us stability in long-time integrations (If you want to learn more about this view of Classical Mechanics Jose and Saletan's textbook is a great resource).

We also have collisions included in the simulation. For this we just assume that the collision between our two bodies happens elastically and then just use the formulas for an elastic collision between two bodies (you can find these on wikipedia if you want). Actually modelling the collisions between two celestial bodies is an incredibly computationally taxing and interesting problem that research still gets done on which is why it is not included here.

<h3>Works in Progress</h3>

1. Working on adding a whole host of bodies such as asteroids, Saturn's rings and a few satellites and telescopes that humanity has launched.
 
2. Creating a barebones UI that allows users to specify arbitrary initial conditions that will evolve them numerically, basically allowing users to do large N-body gravity simulations
  
3. Making the program an executable of some sort.

<h3>Notes and Resources</h3>
Planet textures are from NASA as is the background image of space and the data of the planets, the exception for this is Saturn's rings whose texture was obtained from Bjorn Jonssons's page (http://bjj.mmedia.is/data/s_rings/index.html). The 3D graphics engine was made using a combination of PyGLM, modernGL, and PyGame. Numpy and Numba are both used in performing and speeding up calculations. Feel free to use this for whatever, especially anything physics educational (I have no idea how to add one of those license things and it seems boring to learn right now...). 


Author: Gabriel Kumar
