
@echo off
call C:\Users\syedt\PycharmProjects\L4S-TNA_Application\.venv\Scripts\activate.bat

behave Feature\AdminLogin_Screen.feature
behave Feature\PlatformAdminCreation_Screen.feature
behave Feature\AdminPwdChange_Screen.feature