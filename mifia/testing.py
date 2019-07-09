import mifia.salem as s
import mifia.namelists as nl
import mifia.salem.rolelists as rl
import mifia.salem.roles as r

g = s.Salem(namelist=nl.RoyalGames(), rolelist=rl.SimpleRoleList())

# Use 10 players
g.player_join(s.SalemPlayer(g))
g.player_join(s.SalemPlayer(g))
g.player_join(s.SalemPlayer(g))
g.player_join(s.SalemPlayer(g))
g.player_join(s.SalemPlayer(g))

g.start_game()

mafioso: s.SalemPlayer = g.players.with_role(r.Mafioso)[0]
mafioso_role: r.Mafioso = mafioso.role
mafioso_role.target = g.players.list

...
