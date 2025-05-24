-- 2.1.1 Number of workbench chemical reactions per number of reactant compounds.
SELECT
    number_of_reactant_compounds,
    COUNT(*) AS number_of_workbench_reactions
FROM (
    SELECT
        COUNT(workbench_compound_id) AS number_of_reactant_compounds
    FROM workbench_reaction_reactant_compound
    GROUP BY workbench_reaction_id
)
GROUP BY number_of_reactant_compounds
ORDER BY number_of_reactant_compounds;

-- 2.1.2 Number of workbench chemical reactions per number of reactant and building block compounds.
SELECT
    number_of_reactant_compounds,
    number_of_building_block_compounds,
    COUNT(*) AS number_of_workbench_reactions
FROM (
    SELECT
        wrrc.workbench_reaction_id,
        COUNT(*) AS number_of_reactant_compounds,
        SUM(CAST(wc.is_building_block AS INT)) AS number_of_building_block_compounds
    FROM workbench_reaction_reactant_compound AS wrrc
        JOIN workbench_compound AS wc ON wrrc.workbench_compound_id = wc.id
    GROUP BY wrrc.workbench_reaction_id
)
GROUP BY number_of_reactant_compounds, number_of_building_block_compounds
ORDER BY number_of_reactant_compounds, number_of_building_block_compounds;

-- 2.1.3. Number of workbench chemical reactions in which the product is a building block compound.
SELECT
    COUNT(*) AS number_of_workbench_reactions
FROM workbench_reaction_product_compound AS wrpc
    JOIN workbench_compound AS wc ON wrpc.workbench_compound_id = wc.id
WHERE wc.is_building_block is TRUE;

-- 2.1.4. Number of workbench chemical reactions in which the product appears as a reactant compound in other reactions.
SELECT
    COUNT(DISTINCT wrpc.workbench_compound_id) AS number_of_workbench_reactions
FROM workbench_reaction_product_compound AS wrpc
WHERE wrpc.workbench_compound_id IN (
    SELECT
        DISTINCT workbench_compound_id
    FROM workbench_reaction_reactant_compound
);



-- 2.2.1 Number of workbench chemical reaction transformation patterns.
SELECT
    COUNT(DISTINCT wrtp.workbench_reaction_pattern_id) AS number_of_workbench_reaction_transformation_patterns
FROM workbench_reaction_transformation_pattern AS wrtp;


-- 2.2.2 Number of workbench chemical reactions per transformation pattern.
SELECT
    wrp.smarts AS workbench_reaction_pattern_smarts,
    COUNT(DISTINCT wrtp.workbench_reaction_id) AS number_of_workbench_reactions
FROM workbench_reaction_transformation_pattern as wrtp
    LEFT JOIN workbench_reaction_pattern AS wrp ON wrtp.workbench_reaction_pattern_id = wrp.id
GROUP BY wrp.smarts
ORDER BY number_of_workbench_reactions DESC;
