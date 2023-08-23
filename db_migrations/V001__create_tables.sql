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

