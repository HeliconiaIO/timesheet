import datetime

from .hr_timesheet_sheet_test_cases import HrTimesheetTestCases


class TestHrTimesheetSheetCreate(HrTimesheetTestCases):
    """
    Tests for timesheet create method with timezone handling.
    Employee timezone is Europe/Brussels (UTC+1 in winter, UTC+2 in summer).
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set employee timezone to Europe/Brussels for timezone boundary tests
        cls.user_id.tz = "Europe/Brussels"

    def test_create_timezone_boundary_next_day(self):
        """Test attendance at UTC date boundary that's next day in Brussels"""
        # Attendance at Jan 14, 23:30 UTC = Jan 15, 00:30 Brussels (UTC+1)
        # So it's Jan 15 in employee's timezone
        attendance = self._create_attendance(
            employee=self.employee,
            checkIn=datetime.datetime(2019, 1, 14, 23, 30, 0),
            checkOut=datetime.datetime(2019, 1, 15, 2, 0, 0),
        )
        # Timesheet for Jan 15-20
        timesheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": datetime.date(2019, 1, 15),
                "date_end": datetime.date(2019, 1, 20),
            }
        )
        # Should be included (check_in is Jan 15 in Brussels)
        self.assertIn(
            attendance.id,
            timesheet.attendances_ids.ids,
            "Attendance should be included (Jan 14 23:30 UTC = Jan 15 in Brussels)",
        )
