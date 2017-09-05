''' 

Based Heavily on IndyJoeA's Group Actor plugin

'''

from modules import cbpi
from modules.core.props import Property
from modules.core.hardware import ActorBase
from modules.core.hardware import SensorPassive

master_actor_ids = []


@cbpi.actor
class SlaveActorControl(ActorBase):

    actordesc = "Select an actor to be controlled by this group."
    a_actor= Property.Actor("Slave Actor", description= "Actor to be driven if any others on")
    actor01 = Property.Actor("Actor 1", description=actordesc)
    actor02 = Property.Actor("Actor 2", description=actordesc)
    actor03 = Property.Actor("Actor 3", description=actordesc)
    actor04 = Property.Actor("Actor 4", description=actordesc)
    actor05 = Property.Actor("Actor 5", description=actordesc)
    actor06 = Property.Actor("Actor 6", description=actordesc)
    actor07 = Property.Actor("Actor 7", description=actordesc)
    actor08 = Property.Actor("Actor 8", description=actordesc)

    def init(self):
        self.actors = []
        self.manual_on = False
        if isinstance(self.a_actor, unicode) and self.a_actor:
            self.slave_actor = (int(self.a_actor))
        else:
            self.slave_actor = None
        if isinstance(self.actor01, unicode) and self.actor01:
            self.actors.append(int(self.actor01))
        if isinstance(self.actor02, unicode) and self.actor02:
            self.actors.append(int(self.actor02))            
        if isinstance(self.actor03, unicode) and self.actor03:
            self.actors.append(int(self.actor03))
        if isinstance(self.actor04, unicode) and self.actor04:
            self.actors.append(int(self.actor04))
        if isinstance(self.actor05, unicode) and self.actor05:
            self.actors.append(int(self.actor05))            
        if isinstance(self.actor06, unicode) and self.actor06:
            self.actors.append(int(self.actor06))
        if isinstance(self.actor07, unicode) and self.actor07:
            self.actors.append(int(self.actor07))
        if isinstance(self.actor08, unicode) and self.actor08:
            self.actors.append(int(self.actor08))
      
        if not int(self.id) in master_actor_ids:
            master_actor_ids.append(int(self.id))  
    
  
    def execute_func(self):
        active = False
        if self.manual_on == True:
            active = True
        for actor in self.actors:
            if cbpi.cache.get("actors").get(actor).state == True:
                active = True
        if (self.slave_actor is not None) and (cbpi.cache.get("actors").get(self.slave_actor).state != active):
            if active == True:
                self.api.switch_actor_on(self.slave_actor)
            else:
                self.api.switch_actor_off(self.slave_actor)
  
  
    def set_power(self, power):
        if self.slave_actor is not None:
            self.api.actor_power(self.slave_actor, power=power)

    def on(self, power=None):
        print "Slave on"
        self.manual_on = True
        if self.slave_actor is not None:
            self.api.switch_actor_on(self.slave_actor)

    def off(self):
        print "Slave off"
        self.manual_on = False
        
@cbpi.backgroundtask(key="actor_execute", interval=.2)
def actor_execute(api):
    global master_actor_ids
    for id in master_actor_ids:
        actor = cbpi.cache.get("actors").get(id)
        #test for deleted Func actor
        if actor is None:
            master_actor_ids.remove(id)
        else:
            try:    # try to call execute. Remove if execute fails. Added back when settings updated
                actor.instance.execute_func()
            except Exception as e:
                print e
                cbpi.notify("Actor Error", "Failed to execute actor %s. Please update the configuraiton" % actor.name, type="danger", timeout=0)
                cbpi.app.logger.error("Execute of Actor %s failed, removed from execute list" % id)  
                function_actor_ids.remove(id)   
      
