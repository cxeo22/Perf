"""Clicker tests with a simulated mouse sink; never generates OS input."""
import ctypes,time
from automation import DEFAULT,Engine,INPUT,Native,config_valid
class Sink:
    def __init__(self):self.events=[];self.escape=False
    def emit(self,kind,values):self.events.append((kind,values[:],time.perf_counter()))
    def down(self,vk):return self.escape and vk==27
    def cursor(self):return [10,20]
def wait(engine):
    engine.thread.join(2);assert engine.mode=='idle',engine.status
assert ctypes.sizeof(INPUT)==(40 if ctypes.sizeof(ctypes.c_void_p)==8 else 28)
for invalid in ({'interval_ms':0},{'click_key':'Escape'},{'double':1}):
    try:config_valid(invalid)
    except ValueError:pass
    else:raise AssertionError(invalid)
assert set(config_valid({**DEFAULT,'record_key':'F7','repeats':10,'speed':2}))==set(DEFAULT)
sink=Sink();engine=Engine(sink)
assert not hasattr(engine,'events') and not hasattr(engine,'_record')
for mode in ('recording','playing'):
    try:engine.start(mode,DEFAULT)
    except ValueError:pass
    else:raise AssertionError('Removed mode was allowed')
try:Native().emit('key',[65,30,0])
except ValueError:pass
else:raise AssertionError('Keyboard input was allowed')
engine.start('clicking',{**DEFAULT,'click_count':3,'interval_ms':20,'fixed':True,'x':-10,'y':20})
wait(engine)
assert [(k,v) for k,v,t in sink.events]==[('move',[-10,20]),('button',[0,1]),('button',[0,0])]*3
assert sink.events[-1][2]-sink.events[0][2]>=.03
sink.events=[]
engine.start('clicking',{**DEFAULT,'click_count':1,'double':True,'button':'right'})
wait(engine)
assert [(k,v) for k,v,t in sink.events]==[('button',[1,1]),('button',[1,0])]*2
sink.events=[]
engine.start('clicking',{**DEFAULT,'interval_ms':10000})
time.sleep(.04);engine.stop();wait(engine)
assert len(sink.events)==2
sink.events=[];engine.start('clicking',{**DEFAULT,'interval_ms':10000})
sink.escape=True;wait(engine)
assert all(k in ('move','button') for k,v,t in sink.events)
# Failed mouse-up must still be retried during cleanup.
class FailingSink(Sink):
    def __init__(self):super().__init__();self.failed=False
    def emit(self,kind,values):
        if values==[0,0] and not self.failed:self.failed=True;raise OSError('Test mouse-up failure')
        super().emit(kind,values)
failing=FailingSink();engine=Engine(failing);engine.start('clicking',{**DEFAULT,'click_count':1});wait(engine)
assert failing.events[-1][:2]==('button',[0,0])
print('PASS: click timing, fixed/double clicks, stop/Esc, mouse-button cleanup, configuration validation and removed modes rejected. No OS input generated.')
