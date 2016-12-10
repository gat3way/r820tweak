#!/usr/bin/env python

import wx
import socket
import sys
import os


def get_lna_gain(sock):
    message = "g 5\n"
    sock.sendall(message)
    data = sock.recv(32)
    message = "s 6 "+str(1<<6)+" "+str(1<<6)+"\n"
    sock.sendall(message)
    data2 = sock.recv(32)
    return int(data[2:])&15

def get_mix_gain(sock):
    message = "g 7\n"
    sock.sendall(message)
    data = sock.recv(32)
    return int(data[2:])&15

def get_vga_gain(sock):
    message = "g 12\n"
    sock.sendall(message)
    data = sock.recv(32)
    return int(data[2:])&15

def get_hpf(sock):
    message = "g 27\n"
    sock.sendall(message)
    data = sock.recv(32)
    return 15-(int(data[2:])&15)

def set_hpf(sock,width):
    message = "s 27 "+str(15-width)+" 15\n"
    sock.sendall(message)
    data = sock.recv(32)

def get_lpnf(sock):
    message = "g 27\n"
    sock.sendall(message)
    data = sock.recv(32)
    return 15-(int(data[2:])&(15>>4))

def set_lpnf(sock,width):
    message = "s 27 "+str((15-width)<<4)+" "+str(15<<4)+"\n"
    sock.sendall(message)
    data = sock.recv(32)


def get_lpf(sock):
    message = "g 11\n"
    sock.sendall(message)
    data = sock.recv(32)
    return (int(data[2:])&15)

def set_lpf(sock,width):
    message = "s 11 "+str(width)+" 15\n"
    sock.sendall(message)
    data = sock.recv(32)

def get_filt(sock):
    message = "g 10\n"
    sock.sendall(message)
    data = sock.recv(32)
    return 15-(int(data[2:])&15)

def set_filt(sock,width):
    message = "s 10 "+str(15-width)+" 15\n"
    sock.sendall(message)
    data = sock.recv(32)

def set_lna_gain(sock,gain):
    message = "s 5 "+str(gain)+" 15\n"
    sock.sendall(message)
    data = sock.recv(32)


def set_mix_gain(sock, gain):
    message = "s 7 "+str(gain)+" 15\n"
    sock.sendall(message)
    data = sock.recv(32)


def set_vga_gain(sock, gain):
    message = "s 12 "+str(gain)+" 15\n"
    sock.sendall(message)
    data = sock.recv(32)





class MyPanel(wx.Panel):

    def scan_device(self):
        self.lna_gain = get_lna_gain(self.sock)
        self.mix_gain = get_mix_gain(self.sock)
        self.vga_gain = get_vga_gain(self.sock)
        self.lpf = get_lpf(self.sock)
        self.lpnf = get_lpnf(self.sock)
        self.hpf = get_hpf(self.sock)
        self.filt = get_filt(self.sock)


        self.slider_gain_lna.SetValue(self.lna_gain)
        self.slider_gain_mix.SetValue(self.mix_gain) 
        self.slider_gain_vga.SetValue(self.vga_gain)
        self.slider_lpf.SetValue(self.lpf)
        self.slider_lpnf.SetValue(self.lpnf)
        self.slider_hpf.SetValue(self.hpf)
        self.slider_filt.SetValue(self.filt)


    def connect(self, dev):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_address = '/var/tmp/rtlsdr' + str(dev)
        try:
            self.sock.connect(server_address)
        except socket.error:
            print >>sys.stderr
            #sys.exit(1)
            # TODO: proper warning


    def scan_devices(self):
        self.device_list = []
        self.device_nodes = []
        for a in range(16):
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server_address = '/var/tmp/rtlsdr' + str(a)
            try:
                sock.connect(server_address)
            except socket.error:
                pass
            else:
                self.device_list.append("R820T2 device: #" + str(a))
                self.device_nodes.append(a)



    def __init__(self, parent, id):
        self.scan_devices()

        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("white")

        wx.StaticText(self, -1, 'LNA Gain', (10,45))
        self.slider_gain_lna = wx.Slider(self, -1, 0, 0, 15, (10, 50), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="LNA Gain")
        wx.StaticText(self, -1, 'Mixer Gain', (10,80))
        self.slider_gain_mix = wx.Slider(self, -1, 0, 0, 15, (10, 85), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="Mixer Gain")
        wx.StaticText(self, -1, 'VGA Gain', (10,115))
        self.slider_gain_vga = wx.Slider(self, -1, 0, 0, 15, (10, 120), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="VGA Gain")

        wx.StaticText(self, -1, 'LPF Cutoff', (10,170))
        self.slider_lpf = wx.Slider(self, -1, 0, 0, 15, (10, 175), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="LPF Cutoff")
        wx.StaticText(self, -1, 'LPNF Cutoff', (10,205))
        self.slider_lpnf = wx.Slider(self, -1, 0, 0, 15, (10, 210), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="LNPF Cutoff")
        wx.StaticText(self, -1, 'HPF Cutoff', (10,240))
        self.slider_hpf = wx.Slider(self, -1, 0, 0, 15, (10, 245), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="HPF Cutoff")
        wx.StaticText(self, -1, 'Filter BW', (10,275))
        self.slider_filt = wx.Slider(self, -1, 0, 0, 15, (10, 280), (272, 40), wx.SL_HORIZONTAL | wx.SL_AUTOTICKS, name="Filter BW")


        self.cb = wx.ComboBox(self,
                              id=0,
                              value=self.device_list[0],
                              pos=(10,10),
                              size=(180,25),
                              choices=self.device_list,
                              style=wx.CB_READONLY|wx.CB_DROPDOWN)

        self.button = wx.Button(self, id=wx.ID_ANY, pos=(210,10), size=(70,25), label="Rescan")
        self.button.Bind(wx.EVT_BUTTON, self.onButton)
        self.cb.Bind(wx.EVT_COMBOBOX, self.onCBChange)


        if len(self.device_list):
            self.connect(self.device_nodes[0])
            self.scan_device()

        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)


    def onCBChange(self, event):
        item = self.cb.GetValue()
        num = self.device_list.index(item)
        self.connect(num)
        self.scan_device()


    def onButton(self, event):
        self.scan_devices()
        if len(self.device_list):
            self.connect(self.device_nodes[0])
            self.scan_device()
            self.cb = wx.ComboBox(self,
                              id=0,
                              value=self.device_list[0],
                              pos=(10,10),
                              size=(180,25),
                              choices=self.device_list,
                              style=wx.CB_READONLY|wx.CB_DROPDOWN)



    def sliderUpdate(self, event):
        try:
            if self.lna_gain != self.slider_gain_lna.GetValue():
                self.lna_gain = self.slider_gain_lna.GetValue()
                set_lna_gain(self.sock,self.lna_gain)

            if self.mix_gain != self.slider_gain_mix.GetValue():
                self.mix_gain = self.slider_gain_mix.GetValue()
                set_mix_gain(self.sock,self.mix_gain)

            if self.vga_gain != self.slider_gain_vga.GetValue():
                self.vga_gain = self.slider_gain_vga.GetValue()
                set_vga_gain(self.sock,self.vga_gain)

            if self.lpf != self.slider_lpf.GetValue():
                self.lpf = self.slider_lpf.GetValue()
                set_lpf(self.sock,self.lpf)

            if self.lpnf != self.slider_lpnf.GetValue():
                self.lpnf = self.slider_lpnf.GetValue()
                set_lpnf(self.sock,self.lpnf)

            if self.hpf != self.slider_hpf.GetValue():
                self.hpf = self.slider_hpf.GetValue()
                set_hpf(self.sock,self.hpf)

            if self.filt != self.slider_filt.GetValue():
                self.filt = self.slider_filt.GetValue()
                set_filt(self.sock,self.filt)
        except Exception:
            self.connect(0)


def usage():
    print sys.argv[1],"[program_to_run]"
    print "\n\n"
    print "When used without argument, the r820tweak control panel will launch"
    print "When [program_to_run] is provided, it starts the SDR program with the modified RTLSDR driver"


def main():
    if len(sys.argv)>1:
        if sys.argv[1]!="-h" or sys.argv[1]!="-?":
            os.system("LD_PRELOAD=/usr/local/share/r820tweak/librtlsdr.so " + sys.argv[1])
            return
        else:
            usage()
            return

    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, "r820tweak", size = (290, 340))
    MyPanel(frame,-1)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()