-- triggers

-- create trigger function for last modified (only needs to run once)
CREATE OR REPLACE FUNCTION update_last_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- apply this to each table
CREATE TRIGGER trigger_name_before_update
BEFORE UPDATE ON your_table_name
FOR EACH ROW
EXECUTE FUNCTION update_last_modified();

-- renaming columns
alter table fac_mapping rename column "From Fundamental Accounting Concept" to "concept";
alter table fac_mapping	rename column "Type of Relation (Arcrole)" to "relation_type";
alter table fac_mapping rename column "To IFRS XBRL Taxonomy Concept" to "taxonomy_concept";

-- companies
CREATE TABLE companies(
    id SERIAL PRIMARY KEY,
    cik VARCHAR(255) NOT NULL,
    ticker VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created TIMESTAMP DEFAULT now(),
    last_modified TIMESTAMP DEFAULT now(),
    CONSTRAINT unique_cik_ticker UNIQUE (cik, ticker)
);



-- Revenue
create table revenue(
	id SERIAL primary key,
	cik VARCHAR(255),
	start_date DATE not null,
	end_date DATE not null,
	amount INTEGER not null,
	year integer,
	period VARCHAR(20),
	form VARCHAR(20),
	acctn VARCHAR(255),
	filed DATE
)

