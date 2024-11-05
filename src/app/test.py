from datetime import timedelta
from datetime import datetime
d = timedelta(days=1)
v = datetime.now() - datetime.now()
print(v > d)