--update new_baseball."2023-24" set "player" = replace("player", '*', '');
--
--update new_baseball."2023-24" set "player" = replace("player", '#', '');


select * from new_baseball."2023-24" t where player = 'Aroldis Chapman'

--SELECT "Year", "player", "team", "Player-additional", COUNT(*)
--FROM new_baseball."2023-24" t 
--GROUP BY "Year", "player", "team", "Player-additional"
--HAVING COUNT(*) > 1;

--WITH duplicates AS (
--    SELECT
--        ctid,
--        ROW_NUMBER() OVER (
--            PARTITION BY "Year", "player", "team", "Player-additional"
--        ) AS row_num
--    FROM new_baseball."2023-24"
--)
--DELETE FROM new_baseball."2023-24"
--WHERE ctid IN (
--    SELECT ctid FROM duplicates WHERE row_num > 1
--);