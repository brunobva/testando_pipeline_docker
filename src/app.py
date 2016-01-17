from flask import Flask
from redis import Redis
from multiprocessing import Process
import signal, os

host_redis=os.environ.get('HOST_REDIS', 'redis')
port_redis=os.environ.get('PORT_REDIS', '6379')
env_app=os.environ.get('ENV_APP', 'Desenvolvimento')
port_app=os.environ.get('PYTHON_PORT', '5000')

app = Flask(__name__)
redis = Redis(host=host_redis, port=port_redis)

@app.route('/')
def hello():
    redis.incr('hits')
    if env_app == "prod":
        return 'Hello World -- PRODUCAO ! %s times.' % redis.get('hits')
    else:
        return 'Hello World -- DESENVOLVIMENTO ! %s times.' % redis.get('hits')
if __name__ == "__main__":
    def handler(signum, frame):
        print 'Signal handler called with signal', signum
        server.terminate()
        server.join()

    signal.signal(signal.SIGTERM, handler)

    def run_server():
        app.run(host="0.0.0.0", port=int(port_app),  debug=True)

    server = Process(target=run_server)
    server.start()
