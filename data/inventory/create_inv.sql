
ATTACH database 'inventory.sqlite' as 'inventory';

DROP TABLE inventory.SalesPerson;
DROP TABLE inventory.Beer;

CREATE TABLE inventory.SalesPerson(
   ID         INTEGER PRIMARY KEY  AUTOINCREMENT,
   Name       TEXT NOT NULL,
   Area       Text   
);

CREATE TABLE inventory.Beer(
    ID         INTEGER PRIMARY KEY  AUTOINCREMENT,
    Sales_ID   INT,
    Name       TEXT NOT NULL,
    Type       TEXT NOT NULL,
    Location   TEXT,
    Amount     INT  NOT NULL
);

INSERT INTO inventory.SalesPerson (Name, Area) VALUES ('Juelles', 'San Jose');
INSERT INTO inventory.SalesPerson (Name, Area) VALUES ('David', 'San Jose');
INSERT INTO inventory.SalesPerson (Name, Area) VALUES ('Jeff', 'Santa Clara');
INSERT INTO inventory.SalesPerson (Name, Area) VALUES ('Kregg', 'Santa Clara');

INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (1, 'SAS', 'Sixtle', 'Aloft', 1);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (2, 'IPO', 'Case', 'Aloft', 3);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (3, 'HS', 'Case', 'Aloft', 1);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (1, 'SAS', 'Case', 'Aloft', 1);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (2, 'HS', 'Half', 'Hartfard',2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (2, 'IPO', 'Sixtle', 'Hartfard',2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (2, 'SAS', 'Sixtle', 'Hartfard',2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (3, 'HS', 'Sixtle', 'Hartfard',5);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (3, 'HS', 'Sixtle', 'Hartfard',2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (3, 'SAS', 'Case', 'Zennottos', 3);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (1, 'SAS', 'Sixtle', 'Taplands', 2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (1, 'SAS', 'Case', 'Taplands', 2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (1, 'SAS', 'Sixtle', 'Taplands', 2);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (4, 'SAS', 'Sixtle', 'Aloft', 1);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (4, 'IPO', 'Case', 'Aloft', 3);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (4, 'HS', 'Case', 'Aloft', 1);
INSERT INTO inventory.Beer (Sales_ID, Name, Type, Location, Amount) VALUES (4, 'SAS', 'Case', 'Aloft', 1);
