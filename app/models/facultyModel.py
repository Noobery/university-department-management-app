from app import mysql
from datetime import timedelta

class facultyModel:
    @classmethod
    def create_faculty(cls, facultyID, firstname, lastname, email, role):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                "INSERT INTO faculty (facultyID, firstname, lastname, email, role) VALUES (%s, %s, %s, %s, %s)",
                (facultyID, firstname, lastname, email, role),
            )
            mysql.connection.commit()
            return "Faculty created successfully"
        except Exception as e:
            return f"Failed to create Faculty: {str(e)}"

    @classmethod
    def get_faculty(cls):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("SELECT facultyID, firstname, lastname, email, role FROM faculty WHERE facultyID != 'None'")
            faculties = cur.fetchall()
            return faculties
        except Exception as e:
            return f"Failed to retrieve faculty data: {str(e)}"
        
    # @classmethod
    # def get_single_faculty(cls, facultyID):
    #     try:
    #         cur = mysql.connection.cursor(dictionary=True)
    #         cur.execute("SELECT facultyID, firstname, lastname, email FROM faculty WHERE facultyID = %s", (facultyID,))
    #         faculty = cur.fetchone()
    #         return faculty
    #     except Exception as e:
    #         return f"Failed to retrieve faculty data: {str(e)}"
    #     finally:
    #         cur.close()

    @classmethod
    def delete_faculty(cls, facultyID):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM faculty where facultyID = %s", (facultyID,))
            mysql.connection.commit()
            return "Faculty deleted successfully"
        except Exception as e:
            return f"Failed to delete faculty: {str(e)}"

    @classmethod
    def update_faculty(cls, facultyID, firstname, lastname, email, role):
        try:
            cur = mysql.new_cursor(dictionary=True)
            # Use placeholders in the query to prevent SQL injection
            cur.execute("UPDATE faculty SET firstname = %s, lastname = %s, email = %s, role = %s WHERE facultyID = %s",
                        (firstname, lastname, email, role, facultyID))
            mysql.connection.commit()
            return "Faculty Information Updated Successfully"
        except Exception as e:
            return f"Failed to update faculty: {str(e)}"
    
    
    def get_assigned_subjects(self, faculty_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            query = (
                "SELECT "
                "   af.subjectID AS 'Subject Code', "
                "   subject.description AS 'Description', "
                "   subject.credits AS 'Credits', "
                "   af.sectionID AS 'Section ID', "
                "   s.scheduleID AS 'Schedule ID', "
                "   CASE "
                "       WHEN CONCAT(IFNULL(s.day, 'None'), ' ', "
                "                   IFNULL(TIME_FORMAT(s.time_start, '%h:%i %p'), 'None'), ' - ', "
                "                   IFNULL(TIME_FORMAT(s.time_end, '%h:%i %p'), 'None')) = 'None None - None' "
                "       THEN 'None' "
                "       ELSE CONCAT(IFNULL(s.day, 'None'), ' ', "
                "                   IFNULL(TIME_FORMAT(s.time_start, '%h:%i %p'), 'None'), ' - ', "
                "                   IFNULL(TIME_FORMAT(s.time_end, '%h:%i %p'), 'None')) "
                "   END AS 'Schedule' "
                "FROM assignFaculty af "
                "JOIN subject ON subject.subjectCode = af.subjectID "
                "LEFT JOIN schedule s ON af.subjectID = s.subjectID AND af.sectionID = s.sectionID "
                "WHERE af.facultyID = %s"
            )
            cur.execute(query, (faculty_id,))
            assigned_subjects = cur.fetchall()
            cur.close()
            return assigned_subjects
        except Exception as e:
            return f"Failed to retrieve assigned subject to faculty data: {str(e)}"

    @classmethod
    def create_schedule(cls, subjectID, sectionID, day, time_start, time_end):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                "INSERT INTO schedule (subjectID, sectionID, day, time_start, time_end) VALUES (%s, %s, %s, %s, %s)",
                (subjectID, sectionID, day, time_start, time_end),
            )
            mysql.connection.commit()
            return "Schedule created successfully"
        except Exception as e:
            return f"Failed to create schedule: {str(e)}"
        
    @classmethod
    def get_schedule_by_day(self, faculty_id, day):
        try:
            cur = mysql.new_cursor(dictionary=True)

            # Print the SQL query and parameters for debugging
            query = f"""
                SELECT
                    schedule.scheduleID,
                    schedule.subjectID,
                    schedule.sectionID,
                    schedule.day,
                    TIME_FORMAT(schedule.time_start, '%H:%i:%s') as time_start,
                    TIME_FORMAT(schedule.time_end, '%H:%i:%s') as time_end
                FROM
                    schedule
                JOIN
                    assignFaculty ON schedule.subjectID = assignFaculty.subjectID AND schedule.sectionID = assignFaculty.sectionID
                JOIN
                    faculty ON assignFaculty.facultyID = faculty.facultyID
                WHERE
                    schedule.day = '{day}'
                    AND faculty.facultyID = '{faculty_id}';
            """

            # print("SQL Query:", query)

            cur.execute(query)
            schedules = cur.fetchall()
            cur.close()
            return schedules
        except Exception as e:
            return f"Failed to retrieve {day} schedule data: {str(e)}"


    @classmethod
    def delete_schedule(cls, scheduleID):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM schedule WHERE scheduleID = %s", (scheduleID,))
            mysql.connection.commit()
            return "Schedule deleted successfully"
        except Exception as e:
            return f"Failed to delete Schedule: {str(e)}"
