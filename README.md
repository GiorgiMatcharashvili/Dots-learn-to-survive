# Dots-learn-to-survive
My goal was to create AI mapping model and train it, so it could map the terrain, find deadly points and best safe point near it.
deadly point can be anything starting from a simple wall end of the mine in the field.

NOTE: this is simple AI project from scratch without tenerflow or keras.

# Description
In my model, there is Base class, where I put numbers of population of the dots and size of the terrain. in real life dots can be anything, it can be a drone,
which scans the terrain or something else. 
At the start dots are generated in the center of the terrain, number of dots which will be generated is depend of
the population we put in Base class. They are ruled to leave each other as far as possible, so they can search terrain for deadly points.

After deadly points are found, in next generation, they will find safe points near them and more deadly points. In every generation, there will be more deadly
points found and more safe points around them. In that way, the any terrain will be mapped.

# Getting started
If you want to run the project, clone it and run the launch.py. you can make changes in Base class to customize it and see the results in data.json file,
after it finishes working.

# How does AI works

At first generation, dots are rulled to get away from each other, they don't know any deadly or safe points so they will find deadly points eventually.
At second generation, they know where deadly points are so they will try to get away from each other and don't touch the deadly points at the same time.
after the second generation, algorithm will generates safe points. GP_INDEX in Base classs is responsible for that.
when the third generation starts, dots will try to occupy safe points right away, and after all the safe points will be occupied they will go and try to
find other safe points. After that algorithm will sort and filter all the old and new good points and stabilize them.
At the end, when all the dots will occupy safe points, program will stops working and we will get the mapped terrain.

# Credits
@inc. all by myself
