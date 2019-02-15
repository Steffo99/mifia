from mifia.base.roles import Role


class Villager(Role):
    name: str = "Villager"
    default_priority: int = 0
