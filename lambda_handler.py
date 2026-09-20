from mangum import Mangum

from gateway.app import app


handler = Mangum(app)
