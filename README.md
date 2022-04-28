
# Box_Vole_Simulation

## Recent Changes Notes

    interactable.isIndependent is set to True if how an interactable functions is independent of a vole's behavior.

- Door is Independent
- Lever is Dependent
- RFID is Dependent


Basically if when we gather information for an interactable, if it directly depends on what a vole chooses to do, then isIndependent gets set to False. By this definition, a door's isIndependent is True because a door will be directly dependent on a lever(s), but not directly dependent on a vole. (A vole cannot open a door without first pressing a lever)


If an interactable has any dependents, then there must be a method dependents_loop defined in that interactable's class. 
Here, we set the interactables isIndependent attribute to True, and also define how the interactable handles/interacts with its dependents. 

For a door, we define that if any of its dependents (levers) reaches threshold, then we can open() or close() the door (whichever was indicated in the threshold_condition['goal_value']). 


On the simulation side of things, if we try to call vole_interactable_interaction on an interactable that isIndependent==True, then we return and do not procede with a simulation becuase we defined that the interactable acts independent of a vole's behavior, so we don't want to simulate a behavior that doesn't make sense in a real experiment. 