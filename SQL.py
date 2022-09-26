import sqlite3

class SQL:
    def __init__(self):
        self.conn = sqlite3.connect('Photos.db')

    # record table creation
    def TableCreation(self):
        self.conn.execute('''CREATE TABLE Record
                (ID         INTEGER     PRIMARY KEY     AUTOINCREMENT,
                Name        TEXT        NOT NULL,
                LocID       INTEGER     NOT NULL,
                Faces       TEXT        ,
                Location    TEXT        ,
                DOC         TEXT        ,
                DOM         TEXT        ,
                Size        TEXT        ,
                CapFrom     TEXT        ,
                FOREIGN KEY (LocID)      REFERENCES Location(ID));''')
        print("Record Record table created successfully")

        self.conn.execute('''CREATE TABLE Master
                (ID         INTEGER     PRIMARY KEY     AUTOINCREMENT,
                Name        TEXT        NOT NULL,
                Path        TEXT        NOT NULL);''')
        print("Record Master table created successfully")
        self.conn.execute('''CREATE TABLE Location
                (ID         INTEGER     PRIMARY KEY     AUTOINCREMENT,
                MasterID    INTEGER     NOT NULL,
                Path        TEXT        NOT NULL,
                FOREIGN KEY (MasterID)  REFERENCES Master(ID));''')
        print("Record Location table created successfully")

        self.conn.execute('''CREATE TABLE Places
                (ID             INTEGER     PRIMARY KEY     AUTOINCREMENT,
                ImgID           INTEGER     NOT NULL,
                town            TEXT        ,
                county          TEXT        ,
                state_district  TEXT        ,
                state           TEXT        ,
                postcode        TEXT        ,
                country         TEXT        ,
                amenity         TEXT        ,
                road            TEXT        ,
                FOREIGN KEY (ImgID)      REFERENCES Record(ID));''')
        print("Record Places table created successfully")

        self.Commit()

    # adding to Record table
    def SqlAddRecord(self, name, LocID, faces, location, doc, dom, size, capfrom):
        self.conn.execute("INSERT INTO Record (Name,LocID,Faces,Location,DOC,DOM,Size,CapFrom) VALUES (\"{0}\", {1}, \"{2}\", \"{3}\", \"{4}\", \"{5}\", \"{6}\", \"{7}\")".format(
            name, LocID, faces, location, doc, dom, size, capfrom))

    def SqlAddMaster(self, name, path):
        self.conn.execute("INSERT INTO Master (Name,Path) VALUES (\"{0}\", \"{1}\")".format(
            name, path))

    def SqlAddLocation(self, MasterID, path):
        self.conn.execute("INSERT INTO Location (Path,MasterID) VALUES (\"{0}\",{1})".format(
            path, MasterID))

    def SqlAddPlaces(self, ID, loc):
        ImgID = ID
        town = loc['town'] if 'town' in loc else ""
        county = loc['county'] if 'county' in loc else ""
        state_district = loc['state_district'] if 'state_district' in loc else ""
        state = loc['state'] if 'state' in loc else ""
        postcode = loc['postcode'] if 'postcode' in loc else ""
        country = loc['country'] if 'country' in loc else ""
        amenity = loc['amenity'] if 'amenity' in loc else ""
        road = loc['road'] if 'road' in loc else ""
        self.conn.execute("INSERT INTO Places (ImgID, town, county, state_district, state, postcode, country,amenity,road) VALUES ({0},\"{1}\",\"{2}\",\"{3}\",\"{4}\",\"{5}\",\"{6}\",\"{7}\",\"{8}\")".format(
            ImgID, town, county, state_district, state, postcode, country, amenity, road))
    # Misc

    def SqlQuaryExec(self, quary):
        c = self.conn.cursor()
        c.execute(quary)
        return(c.fetchall())

    def Commit(self):
        self.conn.commit()

    # def DropTable(self, table):
    #     stm = "DROP TABLE {0};".format(table)
    #     self.SqlQuaryExec(stm)
    #     self.Commit()

    # Quary all
    def QuaryMaster(self):
        SUB = self.SqlQuaryExec("""select ID,Name,Path
                                from Master;""")
        return SUB

    def QuaryLocation(self):
        SUB = self.SqlQuaryExec("""select ID, Path, MasterID
                                from Location;""")
        return SUB

    def QuaryLocationUser(self, user,onlypaths=1):
        subM = self.QuaryMaster()
        masterID = -1
        for i in range(len(subM)):
            if subM[i][1] == user:
                masterID = i+1
                break
        if masterID == -1:
            return []
        if onlypaths==1:
            SUB = self.SqlQuaryExec("""select DISTINCT Path
                                    from Location
                                    where MasterID={0};""".format(masterID))
        else:
            SUB = self.SqlQuaryExec("""select DISTINCT ID, MasterID, Path
                                    from Location
                                    where MasterID={0};""".format(masterID))
        print(SUB)
        return SUB

    def QuaryRecord(self):
        SUB = self.SqlQuaryExec("""select ID,Name,LocID,Faces,Location,DOC,DOM,Size,CapFrom
                                from Record;""")
        return SUB

    def QuaryPlaces(self):
        SUB = self.SqlQuaryExec("""select ImgID, town, county, state_district, state, postcode, country,amenity,road
                                from Places;""")
        return SUB

    def FindLocation(self, loc):
        SUB = self.SqlQuaryExec("""select ID, Path, MasterID
                                from Location
                                where Path = \"{0}\";""".format(loc))
        return SUB


if __name__ == "__main__":
    sql = SQL()
    # print(sql.FindLocation("E:/all/photo-and-videos/phone/Camera/IMG_20190720_184203")[0][0])
    sql.TableCreation()
