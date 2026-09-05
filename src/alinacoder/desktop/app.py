from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import DesktopControlPlane,DesktopStateStore,WorkbenchModel,self_test
def _default_state_path()->Path:return Path.home()/'.alinacoder'/'desktop-state.json'
def run_gui()->int:
    import tkinter as tk
    from tkinter import ttk
    root=tk.Tk();root.title('AlinaCoder v0.2')
    try:root.tk.call('tk','scaling',root.winfo_fpixels('1i')/72.0)
    except Exception:pass
    ctl=DesktopControlPlane();store=DesktopStateStore(_default_state_path());state=store.load();root.columnconfigure(0,weight=1);root.rowconfigure(1,weight=1)
    header=ttk.Frame(root);header.grid(row=0,column=0,sticky='ew');status=tk.StringVar(value=ctl.state);ttk.Label(header,text='AlinaCoder',name='title').pack(side='left',padx=8);ttk.Label(header,textvariable=status,name='status').pack(side='right',padx=8)
    body=ttk.Panedwindow(root,orient='horizontal');body.grid(row=1,column=0,sticky='nsew');chat=ttk.Frame(body);inspector=ttk.Notebook(body);body.add(chat,weight=3);body.add(inspector,weight=2);chat.columnconfigure(0,weight=1);chat.rowconfigure(0,weight=1)
    transcript=tk.Text(chat,wrap='word',name='transcript');transcript.grid(row=0,column=0,sticky='nsew',padx=8,pady=8);composer=ttk.Entry(chat,name='composer');composer.grid(row=1,column=0,sticky='ew',padx=8,pady=(0,8));composer.insert(0,state.get('draft',''))
    controls=ttk.Frame(chat);controls.grid(row=2,column=0,sticky='ew',padx=8,pady=(0,8))
    def set_state(fn):fn();status.set(ctl.state);store.save({'draft':composer.get(),'control_state':ctl.state})
    for label,fn in [('Pause',ctl.pause),('Resume',ctl.resume),('STOP',ctl.stop),('Takeover',ctl.takeover)]:ttk.Button(controls,text=label,command=lambda fn=fn:set_state(fn),name=label.lower()).pack(side='left',padx=2)
    for name in ['Plan','Context','Diff','Tests','Git','Receipts','Run Inspector','Timeline','Diagnostics']:
        frame=ttk.Frame(inspector);inspector.add(frame,text=name);ttk.Label(frame,text=f'{name} — canonical state view').pack(anchor='w',padx=8,pady=8)
    def on_close():store.save({'draft':composer.get(),'control_state':ctl.state});root.destroy()
    root.protocol('WM_DELETE_WINDOW',on_close);composer.focus_set();root.geometry('1200x760');root.mainloop();return 0
def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(prog='AlinaCoder');p.add_argument('--self-test',action='store_true');p.add_argument('--semantic-ui',action='store_true');a=p.parse_args(argv)
    if a.self_test:
        result=self_test();print(json.dumps(result,sort_keys=True));return 0 if result['ok'] else 2
    if a.semantic_ui:print(json.dumps(WorkbenchModel().semantic_ui_snapshot(),sort_keys=True));return 0
    return run_gui()
if __name__=='__main__':raise SystemExit(main())
