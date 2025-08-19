from flask import Flask, request, jsonify, send_from_directory
import threading, time, logging, os
import RPi.GPIO as GPIO


r_fr = 37
r_speed = 32

l_fr = 36
l_speed = 33


# Vorbereiten
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(r_speed,GPIO.OUT)
pi_pwm = GPIO.PWM(r_speed,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle

GPIO.setup(r_fr,GPIO.OUT)
GPIO.setup(r_speed,GPIO.OUT)


GPIO.setup(l_speed,GPIO.OUT)
pi_pwml = GPIO.PWM(l_speed,1000)		#create PWM instance with frequency
pi_pwml.start(0)				#start PWM of required Duty Cycle

GPIO.setup(l_fr,GPIO.OUT)
GPIO.setup(l_speed,GPIO.OUT)

app = Flask(__name__)

@app.get("/")
def index():
    # liefert /home/pi/Desktop/Egon/index.html
    return send_from_directory(app.root_path, "index.html")
@app.get("/script.js")
def script_js():
    # liefert /home/pi/Desktop/Egon/index.html
    return send_from_directory(app.root_path, "script.js")
# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger("robot")

# Gemeinsamer Zustand
state = {"left": 0, "right": 0}
state_lock = threading.Lock()

TICK_SEC = 1.0
_ticker_started = False
_ticker_lock = threading.Lock()

def start_ticker_once():
    """Startet den Sekundentakt genau einmal (threadsicher)."""
    global _ticker_started
    with _ticker_lock:
        if _ticker_started:
            return
        def _run():
            log.info("Ticker gestartet (Intervall %.1fs)", TICK_SEC)
            while True:
                with state_lock:
                    l = int(state["left"])
                    r = int(state["right"])
                # >>> HIER deine PWM ansteuern statt nur loggen <<<
                log.info("tick left=%4d  right=%4d", l, r)
                time.sleep(TICK_SEC)
        threading.Thread(target=_run, daemon=True).start()
        _ticker_started = True

# A) Bei 'flask run' mit Reloader nur im Kindprozess starten
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("RUN_MAIN") == "true":
    #start_ticker_once()
    pass
# B) Fallback: falls A nicht greift, spätestens beim ersten Request
@app.before_first_request
def _ensure_ticker():
    #start_ticker_once()
    pass

@app.post("/api/control")
def control():
    data = request.get_json(force=True) or {}
    print(data)
    
    l = max(-100, min(100, int(data.get("left", 0)))) * 0.2
    r = max(-100, min(100, int(data.get("right", 0)))) * 0.2

    if r < 0:
       GPIO.output(r_fr,GPIO.LOW)
    else:
        GPIO.output(r_fr,GPIO.HIGH)
    pi_pwm.ChangeDutyCycle(abs(r))

    if l < 0:
       GPIO.output(l_fr,GPIO.HIGH) # TODO:
    else:
        GPIO.output(l_fr,GPIO.LOW)
    pi_pwml.ChangeDutyCycle(abs(l))
    #with state_lock:
    #    state["left"] = l
    #    state["right"] = r
    #log.info("set  left=%4d  right=%4d", l, r)
    return jsonify(ok=True, left=l, right=r)
    
@app.get("/ping")
def ping():
    return "pong", 200
