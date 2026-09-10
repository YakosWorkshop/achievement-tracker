import sqlachemy

class Achievement:
    def __init__(self, name, unlocked):
        self.name = name
        self.unlocked = unlocked
    

achievements = [
    Achievement("Halo CE", True),
    Achievement("Mortal Combat", False)
]

for achievement in achievements:
    print(achievement.name)
    

# SQL


