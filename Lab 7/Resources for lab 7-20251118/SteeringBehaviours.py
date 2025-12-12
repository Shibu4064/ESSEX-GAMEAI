from __future__ import annotations
import pygame,math,random
from vector import Vector2D

pygame.init()
screen_size = [900,600]
black=[0,0,0]
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption("Steering Behaviours Demo")
pygame.mouse.set_visible(0)
done = False
mouse_down = False
clock = pygame.time.Clock()

class SteeringAgent:

    def __init__(self, init_x: float, init_y: float, draw_colour, max_speed: float, max_acc: float, mass: float):
        self.agent_position=Vector2D(init_x,init_y)    
        self.agent_velocity=Vector2D(0,0)
        self.position = Vector2D(init_x, init_y)
        self.agent_mass=mass
        self.max_speed=max_speed
        self.max_acc=max_acc
        self.draw_colour=draw_colour

    def apply_steering_force(self, desired_velocity: Vector2D, deltaT: float):
        steering_force=desired_velocity-self.agent_velocity
        steering_acceleration=steering_force / self.agent_mass
        if abs(steering_acceleration)>self.max_acc:
          steering_acceleration=steering_acceleration.normalise()*self.max_acc
        self.agent_position += self.agent_velocity * deltaT
        self.agent_velocity += steering_acceleration * deltaT
    
    def calculate_seek_velocity(self, target_position: Vector2D) -> Vector2D:
        # calculate the desired_velocity so as to "seek" to target position
        desired_velocity=target_position-self.agent_position
        if desired_velocity.mag()>0:
            desired_velocity=desired_velocity.normalise()*self.max_speed # TODO fix this
        return desired_velocity

    def calculate_flee_velocity(self, target_position: Vector2D) -> Vector2D:
        # calculate the desired_velocity so as to "flee" from the target position
        desired_velocity=self.agent_position-target_position 
        if desired_velocity.mag()>0:#
            desired_velocity=desired_velocity.normalise()*self.max_speed# TODO fix this
        return desired_velocity
       
    def calculate_pursuit_advanced_target(self, other_agent: SteeringAgent, maxT: float) -> Vector2D:
        # calculate the position of the point in front of other_agent, according to the "pursuit" behaviour
        distance=self.agent_position-other_agent.agent_position
        time_to_reach=distance.mag()/self.max_speed
        if time_to_reach>maxT:
            time_to_reach=maxT
        advanced_target=other_agent.agent_position+other_agent.agent_velocity*time_to_reach # TODO fix this
        return advanced_target


    def adjust_velocity_for_arrival(self, desired_velocity: Vector2D, target_position: Vector2D, arrivalSlowingDist: float, arrivalStoppingDist: float) -> Vector2D:
        # calculate a new velocity vector, based upon desired_velocity, but which is modified according to the "arrival" behaviour
        # On entry, desired_velocity will have magnitude self.max_speed
        # Calculate distance to the target.
        to_target=target_position-self.agent_position
        distance_to_target=to_target.mag()
        if distance_to_target<arrivalStoppingDist:
            desired_velocity=Vector2D(0,0)
        elif distance_to_target<arrivalSlowingDist:
            desired_velocity=desired_velocity*(distance_to_target/arrivalSlowingDist)
        #modified_velocity = desired_velocity*1 # TODO fix this
        return desired_velocity
       
    def get_agent_orientation(self) ->float:
        if self.agent_velocity.mag()>0:
            ang=math.atan2(self.agent_velocity.x,self.agent_velocity.y) # measure angle of agent's velocity vector, in radians clockwise from north
        else:
            ang=0
        return ang
        
    def keep_within_screen_bounds(self):
        self.agent_position.x=(self.agent_position.x+screen_size[0])%screen_size[0] # force wrap-around in x direction
        self.agent_position.y=(self.agent_position.y+screen_size[1])%screen_size[1] # force wrap-around in x direction
            
    def draw_agent(self):
        size = (16, 16)
        temp_surface = pygame.Surface(size,pygame.SRCALPHA)
        colour=self.draw_colour+[255] # the 255 here is the alpha value, i.e. we want this polygon to be opaque
        pygame.draw.polygon(temp_surface, colour, ((14,0),(8,16),(2,0))) # draw a solid triangle shape pointing straight up
        ang=self.get_agent_orientation()
        rotated_surface=pygame.transform.rotate(temp_surface, math.degrees(ang)) # rotate anticlockwise by amount ang
        screen.blit(rotated_surface, (self.agent_position.x, self.agent_position.y))

class WanderingAgent(SteeringAgent):# inherits most behaviour from SteeringAgent
    def __init__(self, init_x, init_y, draw_colour, max_speed, max_acc, mass, wander_rate,wander_offset,wander_radius):
        self.position = Vector2D(init_x, init_y)
        self.wander_rate=wander_rate
        self.wander_radius=wander_radius
        self.wander_offset=wander_offset
        self.wander_orientation=0
        SteeringAgent.__init__(self,init_x, init_y, draw_colour, max_speed, max_acc, mass)

    def calculate_wander_seek_target(self, random_float: float) -> Vector2D:
        # This function needs to apply the main logic of the "wander" behaviour
        # It should calculate the position that will then be used as the seek_target.
        # This function should return a position (of the seek target)
        # It should also modify self.wander_orientation
        # On entry: random_float is a random float in range from -1 to +1
        #seek_target = Vector2D(0,0) # TODO fix this
        #return seek_target
        self.wander_orientation += random_float * self.wander_rate
        target_orientation = self.wander_orientation + self.get_agent_orientation()
        forward_dir = self.agent_velocity.normalise()
        large_circle_centre = self.position + forward_dir * self.wander_offset
        target_orientation_vec = Vector2D(math.sin(target_orientation),math.cos(target_orientation))
        seek_target = large_circle_centre + target_orientation_vec * self.wander_radius
        return seek_target

    def calc_wander_target_velocity(self) -> Vector2D:
        seek_target=self.calculate_wander_seek_target(random.uniform(-1, 1))
        # Seek towards the target small circle:
        return self.calculate_seek_velocity(seek_target)



def draw_mouse_pointer(screen,mouse_pos, colour):
    pygame.draw.rect(screen, colour, pygame.Rect(mouse_pos.x, mouse_pos.y, 12, 12))


yellow = [255,255,0]
magenta = [255,0,255]
blue = [0,0,255]
red = [255,0,0]
white=[255,255,255]

deltaT=1/50
agent_seek = SteeringAgent(200,200,magenta,200,300,.1)
agent_flee = SteeringAgent(300,200,blue,200,300,.1)
agent_pursuit = SteeringAgent(300,200,yellow,200*2,300*2,.1)
#agent_wander = WanderingAgent(300,200,white,100,300,.1, 20*deltaT,20,3)
agent_wander = WanderingAgent(300, 200, white, 100, 300, 0.1, 20 * deltaT, 20, 3)
mouse_pos=Vector2D(100,100)

while done==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    screen.fill(black) # background screen colour
    
    mouse_down = pygame.mouse.get_pressed()[0]#note: returns 0/1, which == False/True
    if not mouse_down:
        pos = pygame.mouse.get_pos()
        mouse_pos=Vector2D(pos[0],pos[1])
    draw_mouse_pointer(screen,mouse_pos,red)
    target_position=mouse_pos
    
    
    desired_velocity=agent_seek.calculate_seek_velocity(target_position)
    desired_velocity=agent_seek.adjust_velocity_for_arrival(desired_velocity, target_position, arrivalSlowingDist=40, arrivalStoppingDist=10)
    agent_seek.apply_steering_force(desired_velocity, deltaT)
    
    desired_velocity=agent_flee.calculate_flee_velocity(target_position)
    agent_flee.apply_steering_force(desired_velocity, deltaT)
    
    advanced_target=agent_pursuit.calculate_pursuit_advanced_target(agent_seek, maxT=6)
    desired_velocity=agent_pursuit.calculate_seek_velocity(advanced_target)
    agent_pursuit.apply_steering_force(desired_velocity, deltaT)
    
    desired_velocity=agent_wander.calc_wander_target_velocity()
    agent_wander.apply_steering_force(desired_velocity, deltaT)

    for agent in [agent_seek, agent_flee, agent_pursuit, agent_wander]:
        agent.keep_within_screen_bounds()
        agent.draw_agent()
        
    pygame.display.flip() # pushes all drawings to the screen
    clock.tick(1/deltaT) # pauses deltaT time

pygame.quit()
