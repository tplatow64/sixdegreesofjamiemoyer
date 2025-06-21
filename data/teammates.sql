select distinct concat(a."teamid", '_', a."yearid") as "team_year", a."playerid", t."teamid" as "teamid", t."name" AS "teamname", t2."franchname" as "franchisename", t2."franchid" as "franchiseid", a."yearid"
from new_baseball.appearances a 
inner join new_baseball.teams t 
on a."teamid" = t."teamid" 
and a."yearid" = t."yearid" 
inner join new_baseball.teams_franchises t2
on t."franchid" = t2."franchid"
order by t2."franchname"