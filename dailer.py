import pjsua

# Callback class for handling events
class MyCallCallback(pjsua.CallCallback):
    def on_state(self, prm):
        print("Call state:", prm.e)
        if prm.e == pjsua.CallState.DISCONNECTED:
            pjsua.stop()
            pjsua.destroy()

# Initialize pjsua
pjsua.Lib.instance().init()
pjsua.Lib.instance().set_null_snd_dev()

# Replace 'recipient_phone_number' with the phone number you want to call
call_uri = 'sip:' + 'recipient_phone_number' + '@sip.example.com'

# Make the call
call = pjsua.Lib.instance().make_call(call_uri, MyCallCallback())

# Start pjsua main loop
pjsua.Lib.instance().start()
