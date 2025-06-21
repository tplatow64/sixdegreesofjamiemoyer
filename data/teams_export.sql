select distinct t."teamid", t2."franchname"
from new_baseball.teams t
inner join new_baseball.teams_franchises t2
on t."franchid" = t2."franchid"
order by t."teamid"