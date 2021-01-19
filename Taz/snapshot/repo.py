import mysql.connector
import configuration


class terminateDBOperations:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.hostname = configuration.hostname
        self.username = configuration.username
        self.db = configuration.db
        self.password = configuration.password

    def makeConnSQL(self):
        self.conn = mysql.connector.Connect(host=self.hostname, user=self.username, passwd=self.password, db=self.db)
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

    def closeConn(self):
        self.conn.close()

    def putResourceInfoToDatabase(self, table_name, snapshotid, creation_date, volumeid, v_size, terminated_flag, terminate, fetch_date, s_description, comment):
        try:
            self.makeConnSQL()
        except Exception as e:
            print("ERROR: An exception while making connection to SQL in OpsReportRDSMetrics e = " + str(e))
            raise

        sql = "INSERT IGNORE INTO " + table_name + " (snapshotid, creation_date, volumeid, v_size, terminated_flag, terminate, fetch_date, s_description, comment) VALUES (%s, %s ,  %s, %s, %s, %s, %s, %s, %s)"
        val = (snapshotid, creation_date, volumeid, v_size, terminated_flag, terminate, fetch_date, s_description, comment)

        try:
            self.cursor.execute(sql, val)
            self.conn.commit()
        except Exception as e:
            print("ERROR in putOpsStatsInDb ::  " + str(e) + " args=" + str(e.args) + " repr=" + str(repr(e)))

        self.closeConn()
        return True

    def updateResourceTerminationState(self, table_name, terminated_flag, SnapshotId):
        try:
            self.makeConnSQL()
        except Exception as e:
            print("ERROR: An exception while making connection to SQL in OpsReportRDSMetrics e = " + str(e))
            raise
        sql = "UPDATE " + table_name + " SET terminated_flag =  %s  WHERE SnapshotId =  %s"
        val = (terminated_flag, SnapshotId)
        try:
            self.cursor.execute(sql, val)
            self.conn.commit()
        except Exception as e:
            print("ERROR in putOpsStatsInDb ::  " + str(e))

        self.closeConn()
        return True

    def selectNonTerminatedResources(self, table_name, terminated_flag, terminate):
        try:
            self.makeConnSQL()
        except Exception as e:
            print("ERROR: An exception while making connection to SQL in OpsReportRDSMetrics e = " + str(e))
            raise

        sql = "SELECT SnapshotId FROM " + table_name + " WHERE terminated_flag =" + str(terminated_flag) + " AND terminate='" + str(terminate)+"'"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print("ERROR in putOpsStatsInDb ::  " + str(e))

        rows = self.cursor.fetchall()
        self.closeConn()
        return rows

    def deleteTaggedResources(self, table_name, resource_id):
        try:
            self.makeConnSQL()
        except Exception as e:
            print("ERROR: An exception while making connection to SQL in OpsReportRDSMetrics e = " + str(e))
            raise

        sql = "DELETE FROM " + table_name + " WHERE id = '" + str(resource_id) + "'"

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print(self.cursor.rowcount, "record(s) deleted")
        except Exception as e:
            print("ERROR in putOpsStatsInDb ::  " + str(e))
        self.closeConn()
        return True