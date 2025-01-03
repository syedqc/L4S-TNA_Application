import subprocess

if __name__ == "__main__":
    subprocess.run([
        "pytest",
        "--bdd",
        "--capture=no",
        "--alluredir=allure-results",
        "Feature/AdminLogin_Screen.feature",
        "Feature/PlatformAdminCreation_Screen.feature",
        "Feature/AdminPwdChange_Screen.feature"
    ])
