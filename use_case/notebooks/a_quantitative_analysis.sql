-- 1.1.1 The total number of chemical compounds.
SELECT
    COUNT(DISTINCT ac.id) AS number_of_archive_compounds,
    COUNT(DISTINCT wca.archive_compound_id) AS number_of_utilized_archive_compounds,
    100.0 * COUNT(DISTINCT wca.archive_compound_id) / COUNT(DISTINCT ac.id) AS percentage_of_utilized_archive_compounds,
    COUNT(DISTINCT wc.id) AS number_of_workbench_compounds
FROM archive_compound AS ac
    LEFT JOIN workbench_compound_archive AS wca ON ac.id = wca.archive_compound_id
    LEFT JOIN workbench_compound AS wc ON wca.workbench_compound_id = wc.id;

-- 1.1.2 The exclusive number of archive chemical compounds per data source.
SELECT
    COUNT(DISTINCT ac_1.id) AS number_of_archive_compounds,
    COUNT(DISTINCT wca_1.archive_compound_id) AS number_of_utilized_archive_compounds
FROM archive_compound AS ac_1
    JOIN archive_compound_source AS acs_1 ON ac_1.id = acs_1.archive_compound_id
    JOIN archive_source AS arso_1 ON acs_1.archive_source_id = arso_1.id
    LEFT JOIN workbench_compound_archive AS wca_1 ON ac_1.id = wca_1.archive_compound_id
WHERE arso_1.version = 'v_building_block_bb_30' AND ac_1.id NOT IN (
    SELECT
        acs_2.archive_compound_id
    FROM archive_compound AS ac_2
        JOIN archive_compound_source AS acs_2 ON ac_2.id = acs_2.archive_compound_id
        JOIN archive_source AS arso_2 ON acs_2.archive_source_id = arso_2.id
    WHERE arso_2.version IN ('v_building_block_bb_50', 'v_building_block_bb_40')
);

-- 1.1.3 The exclusive number of workbench chemical compounds per data source.
SELECT
    COUNT(DISTINCT wc_1.id) AS number_of_workbench_compounds
FROM workbench_compound AS wc_1
    JOIN workbench_compound_archive AS wca_1 ON wc_1.id = wca_1.workbench_compound_id
    JOIN archive_compound AS ac_1 ON wca_1.archive_compound_id = ac_1.id
    JOIN archive_compound_source AS acs_1 ON ac_1.id = acs_1.archive_compound_id
    JOIN archive_source AS arso_1 ON acs_1.archive_source_id = arso_1.id
WHERE arso_1.version = 'v_building_block_bb_30' AND wc_1.id NOT IN (
    SELECT
        wc_2.id
    FROM workbench_compound AS wc_2
        JOIN workbench_compound_archive AS wca_2 ON wc_2.id = wca_2.workbench_compound_id
        JOIN archive_compound AS ac_2 ON wca_2.archive_compound_id = ac_2.id
        JOIN archive_compound_source AS acs_2 ON ac_2.id = acs_2.archive_compound_id
        JOIN archive_source AS arso_2 ON acs_2.archive_source_id = arso_2.id
    WHERE arso_2.version IN ('v_building_block_bb_50', 'v_building_block_bb_40')
);



-- 1.2.1 The total number of chemical reactions.
SELECT
    COUNT(DISTINCT ar.id) AS number_of_archive_reactions,
    COUNT(DISTINCT wra.archive_reaction_id) AS number_of_utilized_archive_reactions,
    100.0 * COUNT(DISTINCT wra.archive_reaction_id) / COUNT(DISTINCT ar.id) AS percentage_of_utilized_archive_reactions,
    COUNT(DISTINCT wr.id) AS number_of_workbench_reactions,
    1.0 * COUNT(DISTINCT wr.id) / COUNT(DISTINCT ar.id) AS reaction_expansion_factor
FROM archive_reaction AS ar
    LEFT JOIN workbench_reaction_archive AS wra ON ar.id = wra.archive_reaction_id
    LEFT JOIN workbench_reaction AS wr ON wra.workbench_reaction_id = wr.id;

-- 1.2.2 The exclusive number of archive chemical reactions per data source.
SELECT
    COUNT(DISTINCT ar_1.id) AS number_of_archive_reactions,
    COUNT(DISTINCT wra_1.archive_reaction_id) AS number_of_utilized_archive_reactions
FROM archive_reaction AS ar_1
    JOIN archive_reaction_source AS ars_1 ON ar_1.id = ars_1.archive_reaction_id
    JOIN archive_source AS arso_1 ON ars_1.archive_source_id = arso_1.id
    LEFT JOIN workbench_reaction_archive AS wra_1 ON ar_1.id = wra_1.archive_reaction_id
WHERE arso_1.name = 'miscellaneous' AND ar_1.id NOT IN (
    SELECT
        ars_2.archive_reaction_id
    FROM archive_reaction AS ar_2
        JOIN archive_reaction_source AS ars_2 ON ar_2.id = ars_2.archive_reaction_id
        JOIN archive_source AS arso_2 ON ars_2.archive_source_id = arso_2.id
    WHERE arso_2.name IN ('uspto', 'ord', 'crd')
);

-- 1.2.3 The exclusive number of workbench chemical reactions per data source.
SELECT
    COUNT(DISTINCT wr_1.id) AS number_of_workbench_reactions
FROM workbench_reaction AS wr_1
    JOIN workbench_reaction_archive AS wra_1 ON wr_1.id = wra_1.workbench_reaction_id
    JOIN archive_reaction AS ar_1 ON wra_1.archive_reaction_id = ar_1.id
    JOIN archive_reaction_source AS ars_1 ON ar_1.id = ars_1.archive_reaction_id
    JOIN archive_source AS arso_1 ON ars_1.archive_source_id = arso_1.id
WHERE arso_1.name = 'miscellaneous' AND wr_1.id NOT IN (
    SELECT
        wr_2.id
    FROM workbench_reaction AS wr_2
        JOIN workbench_reaction_archive AS wra_2 ON wr_2.id = wra_2.workbench_reaction_id
        JOIN archive_reaction AS ar_2 ON wra_2.archive_reaction_id = ar_2.id
        JOIN archive_reaction_source AS ars_2 ON ar_2.id = ars_2.archive_reaction_id
        JOIN archive_source AS arso_2 ON ars_2.archive_source_id = arso_2.id
    WHERE arso_2.name IN ('uspto', 'ord', 'crd')
);



-- 1.3.1 The total number of chemical reaction patterns.
SELECT
    COUNT(DISTINCT arp.id) AS number_of_archive_reaction_patterns,
    COUNT(DISTINCT wrpa.archive_reaction_pattern_id) AS number_of_utilized_archive_reaction_patterns,
    100.0 * COUNT(DISTINCT wrpa.archive_reaction_pattern_id) / COUNT(DISTINCT arp.id) AS percentage_of_utilized_archive_reaction_patterns,
    COUNT(DISTINCT wrp.id) AS number_of_workbench_reaction_patterns
FROM archive_reaction_pattern AS arp
    LEFT JOIN workbench_reaction_pattern_archive AS wrpa ON arp.id = wrpa.archive_reaction_pattern_id
    LEFT JOIN workbench_reaction_pattern AS wrp ON wrpa.workbench_reaction_pattern_id = wrp.id;

-- 1.3.2 The exclusive number of archive chemical reaction patterns per data source.
SELECT
    COUNT(DISTINCT arp_1.id) AS number_of_archive_reaction_patterns,
    COUNT(DISTINCT wrpa_1.archive_reaction_pattern_id) AS number_of_utilized_archive_reaction_patterns
FROM archive_reaction_pattern AS arp_1
    JOIN archive_reaction_pattern_source AS arps_1 ON arp_1.id = arps_1.archive_reaction_pattern_id
    JOIN archive_source AS arso_1 ON arps_1.archive_source_id = arso_1.id
    LEFT JOIN workbench_reaction_pattern_archive AS wrpa_1 ON arp_1.id = wrpa_1.archive_reaction_pattern_id
WHERE arso_1.version = 'v_auto_template_by_20240627_chen_l_and_li_y' AND arp_1.id NOT IN (
    SELECT
        arps_2.archive_reaction_pattern_id
    FROM archive_reaction_pattern AS arp_2
        JOIN archive_reaction_pattern_source AS arps_2 ON arp_2.id = arps_2.archive_reaction_pattern_id
        JOIN archive_source AS arso_2 ON arps_2.archive_source_id = arso_2.id
    WHERE arso_2.version IN ('v_retro_transform_db_by_20180421_avramova_s_et_al', 'v_dingos_by_20190701_button_a_et_al')
);

-- 1.3.3 The exclusive number of workbench chemical reaction patterns per data source.
SELECT
    COUNT(DISTINCT wrp_1.id) AS number_of_workbench_reaction_patterns
FROM workbench_reaction_pattern AS wrp_1
    JOIN workbench_reaction_pattern_archive AS wrpa_1 ON wrp_1.id = wrpa_1.workbench_reaction_pattern_id
    JOIN archive_reaction_pattern AS arp_1 ON wrpa_1.archive_reaction_pattern_id = arp_1.id
    JOIN archive_reaction_pattern_source AS arps_1 ON arp_1.id = arps_1.archive_reaction_pattern_id
    JOIN archive_source AS arso_1 ON arps_1.archive_source_id = arso_1.id
WHERE arso_1.version = 'v_auto_template_by_20240627_chen_l_and_li_y' AND wrp_1.id NOT IN (
    SELECT
        wrp_2.id
    FROM workbench_reaction_pattern AS wrp_2
        JOIN workbench_reaction_pattern_archive AS wrpa_2 ON wrp_2.id = wrpa_2.workbench_reaction_pattern_id
        JOIN archive_reaction_pattern AS arp_2 ON wrpa_2.archive_reaction_pattern_id = arp_2.id
        JOIN archive_reaction_pattern_source AS arps_2 ON arp_2.id = arps_2.archive_reaction_pattern_id
        JOIN archive_source AS arso_2 ON arps_2.archive_source_id = arso_2.id
    WHERE arso_2.version IN ('v_retro_transform_db_by_20180421_avramova_s_et_al', 'v_dingos_by_20190701_button_a_et_al')
);
