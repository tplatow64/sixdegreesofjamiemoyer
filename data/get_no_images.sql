select people.playerid, people.bbrefid,
trim(concat(people.namefirst, ' ', people.namelast, ' ', people.suffix)) as name,
concat('https://www.baseball-reference.com/players/', lower(left(people.namelast, 1)), '/', people.bbrefid, '.shtml') as player_url
from people left join image_urls iu on iu.playerid = people.bbrefid
where iu.playerid is null and people.bbrefid != ''