select p."playerid", p."bbrefid",
trim(concat(p."namefirst", ' ', p."namelast", ' ', p."suffix")) as name, 
p."namegiven", p."birthyear", p."namefirst", p."namelast", p.suffix,
appearances_data."debut", appearances_data."finalgame", iu."image_url"
from people p 
left join image_urls iu
on p."playerid" = iu.playerid
left join(
select playerid, min(yearid) as debut, max(yearid) as finalgame from appearances a 
group by playerid
) as appearances_data
on p.playerid=appearances_data.playerid
where p.bbrefid != ''