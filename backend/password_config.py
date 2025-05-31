# Password configuration file
# Administrators can modify these settings as needed

# Minimum password length
MIN_LENGTH = 10

# Maximum password length
MAX_LENGTH = 50

# Whether to require at least one uppercase letter
REQUIRE_UPPERCASE = False

# Whether to require at least one lowercase letter
REQUIRE_LOWERCASE = True

# Whether to require at least one number
REQUIRE_NUMBERS = True

# Whether to require at least one special character
REQUIRE_SPECIAL_CHARS = True

# Allowed special characters
SPECIAL_CHARS = "!@#$%^&*()_-+=<>?/[]{}|"

# Password history - number of previous passwords to check against
# User cannot reuse any of their last N passwords
PASSWORD_HISTORY_LENGTH = 3

# Maximum number of failed login attempts before account is locked
MAX_LOGIN_ATTEMPTS = 3

# Maximum number of failed login attempts per IP before it's blocked
MAX_IP_LOGIN_ATTEMPTS = 10

# Minutes to lock an IP after too many failed attempts
IP_LOCKOUT_MINUTES = 60

# List of common passwords that are not allowed (dictionary passwords)
DISALLOWED_PASSWORDS = [
    "password",
    "123456",
    "1234567890",
    "qwerty",
    "abc123",
    "111111",
    "123123",
    "admin",
    "welcome",
    "password123",
    "admin123",
    "letmein",
    "monkey",
    "1234567",
    "sunshine",
    "iloveyou",
    "trustno1",
    "princess",
    "123456789",
    "987654321",
    "mypassword",
    "football",
    "000000",
    "qwerty123",
    "dragon",
    "baseball",
    "superman",
    "password1",
    "internet",
    "service",
    "provider",
    "Abc@123456",
    "Password@123",
    "Welcome123!",
    "Qwerty@1234",
    "Admin123456!",
    "P@ssw0rd1234",
    "Abc123456789!",
    "Summer2023!",
    "Winter2023@",
    "Spring2023#",
    "Autumn2023$",
    "Iloveyou123!",
    "Football123@",
    "Baseball123#",
    "America123$",
    "Liverpool123%",
    "Manchester1!",
    "Chelsea123^&",
    "Arsenal123*(",
    "Barcelona12+",
    "January2023!",
    "February23@",
    "March2023#$",
    "April2023%^",
    "December23&",
    "Monday2023!",
    "Friday2023@",
    "Abcdef1234!",
    "Zxcvbn1234@",
    "Asdfgh1234#",
    "P@$$w0rd123",
    "$ecur1tyAbc",
    "Adm1n1str@t",
    "M@nager123!",
    "L0g1n@ccess",
    "C0mp@ny123$",
    "W3lc0me123!",
    "$uper123Man",
    "Tr0ub@dour1",
    "Th1nkp@d123",
    "Qwerty123!@",
    "Company2023!",
    "Passw0rd!23",
    "Security1!2",
    "Abcd1234!@",
    "Test1234!@#",
    "Default123$",
    "Network123!",
    "Internet123@"
]