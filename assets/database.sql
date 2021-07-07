CREATE TABLE "restaurants" (
	"name"	TEXT NOT NULL,
	"address"	TEXT,
	"city"	TEXT,
	"state"	TEXT,
	"features"	TEXT,
	"stars"	REAL DEFAULT 0,
	"identified"	INTEGER DEFAULT 0,
	"delivery"	INTEGER DEFAULT 0,
	"takeout"	INTEGER DEFAULT 0,
	"landline"	TEXT,
	"reviewNum"	INTEGER DEFAULT 0,
	"bReviewNum"	INTEGER DEFAULT 0,
	CONSTRAINT "name-addr-city-uniqueness" UNIQUE("name","address","city")
);