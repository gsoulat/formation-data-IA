-- Tables de codes issues du dictionnaire de données TLC (édition 2025).
CREATE OR REPLACE TABLE NYC_TAXI.STAGING.PAYMENT_TYPE_CODES AS
SELECT column1::integer AS payment_type_key, column2::varchar AS payment_type_label
FROM VALUES
    (0, 'Flex Fare trip'), (1, 'Credit card'), (2, 'Cash'), (3, 'No charge'),
    (4, 'Dispute'), (5, 'Unknown'), (6, 'Voided trip');

CREATE OR REPLACE TABLE NYC_TAXI.STAGING.RATE_CODE_CODES AS
SELECT column1::integer AS rate_code_key, column2::varchar AS rate_code_label
FROM VALUES
    (1, 'Standard rate'), (2, 'JFK'), (3, 'Newark'), (4, 'Nassau or Westchester'),
    (5, 'Negotiated fare'), (6, 'Group ride'), (99, 'Null or unknown');

CREATE OR REPLACE TABLE NYC_TAXI.STAGING.VENDOR_CODES AS
SELECT column1::integer AS vendor_key, column2::varchar AS vendor_name
FROM VALUES
    (1, 'Creative Mobile Technologies, LLC'), (2, 'Curb Mobility, LLC'),
    (6, 'Myle Technologies Inc'), (7, 'Helix');
