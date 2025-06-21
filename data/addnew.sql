-- add new people (update w new table name)
insert into people (playerid, namefirst, namelast, bbrefid, suffix)
select bbrefid, translate(namefirst, 'ÁáÉéÍíÓóÚúÑñü', 'AaEeIiOoUuNnu') as namefirst,
translate(namelast, 'ÁáÉéÍíÓóÚúÑñü', 'AaEeIiOoUuNnu') as namelast,
bbrefid, suffix
from "2023-24-clean"
where bbrefid not in (select bbrefid from people) order by bbrefid

-- check it worked (update new id)
select * from people where id >= 21011

select * from teams where franchid = 'CHW'

-- add new year rows to teams
insert into teams (yearid, lgid, teamid, franchid, name)
select 2024, lgid, teamid, franchid, name from teams where yearid = 2023

-- add new rows to appearances (update w new table and year)
insert into appearances (yearid, playerid, teamid, lgid)
select clean."Year" as yearid, clean.bbrefid as playerid,
teams.teamid, teams.lgid
from "2023-24-clean" as clean
left join teams on teams.franchid = clean.team and teams.yearid = clean."Year"
where "Year" = 2024

-- check it worked (update w new year)
select * from appearances where yearid = 2024