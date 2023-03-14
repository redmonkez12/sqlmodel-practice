# List the countries that have a larger area than 3 million square kilometers or at least 25 million inhabitants.

## Solution    

    SELECT w.name, w.population, w.area
    FROM world w
    WHERE w.population >= 25000000 OR w.area >= 3000000;SELECT w.name, w.population, w.area
    FROM world w
    WHERE w.population >= 25000000 OR w.area >= 3000000;