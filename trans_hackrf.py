import sys
import signal
import os
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
from gnuradio import analog, audio, blocks, filter, gr, soapy
from gnuradio.fft import window
import wave
import subprocess
import sip
import soundfile as sf


class WBFM_STARSV(gr.top_block, Qt.QWidget):

    def __init__(self, wav_file):
        gr.top_block.__init__(self, "Transmission Window", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(4e6)
        self.freq = freq = int(105e6)

        ##################################################
        # Blocks
        ##################################################
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, freq)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(16, 0.0), 47.0))
        self.rational_resampler_xxx_2 = filter.rational_resampler_ccc(
                interpolation=100,
                decimation=1,
                taps=[],
                fractional_bw=0)
           
                
        self.blocks_wavfile_source_0 = blocks.wavfile_source(wav_file, False)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_source_0 = audio.source(48000, '', False)
        self.analog_wfm_tx_0 = analog.wfm_tx(
            audio_rate=samp_rate,
            quad_rate=samp_rate,
            tau=75e-6,
            max_dev=5e3,
            fh=-1.0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_add_xx_0, 0))
        
        
        self.connect((self.rational_resampler_xxx_2, 0), (self.soapy_hackrf_sink_0, 0))

    def message_listener(self):
        for line in self.process.stdout:
            message = line.strip().decode()
            if message == "TRANSMISSION_COMPLETE":
                self.close()  # Close GUI window when transmission is completed
                return

    def closeEvent(self, event):
        self.process.terminate()  # Terminate subprocess on closing the GUI
        self.settings = Qt.QSettings("GNU Radio", "WBFM_STARSV")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        print("GUI Closed")
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_sink_x_0_1_0.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_sink_x_0_1_0.set_frequency_range(self.freq, self.samp_rate)

def get_audio_length(wav_file):
    # Open the audio file and get its duration
    with wave.open(wav_file, 'rb') as wf:
        return wf.getnframes() / wf.getframerate()

def main(top_block_cls=WBFM_STARSV, options=None):
    qapp = Qt.QApplication(sys.argv)

    # Parse command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 WBFM_STARSV.py <path_to_wav_file>")
        sys.exit(1)

    wav_file = sys.argv[1]

    audio_length = get_audio_length(wav_file)

    tb = top_block_cls(wav_file)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    # Fetching the PID of the current process
    pid = os.getpid()
    print("Process ID:", pid)

    # Set the timer to the duration of the audio file
    timer = Qt.QTimer()
    timer.start(int(audio_length * 1000))  # Convert seconds to milliseconds
    timer.timeout.connect(lambda: os.kill(pid, signal.SIGTERM))  # Terminate the process when the timer expires

    # Trigger rx_fox.py in pc2
    rx_fox_command = f'ssh -X -i ~/.ssh/sshtry cranky@192.168.0.100 "python3 /home/cranky/Downloads/rx_fox.py {audio_length}" > /dev/null 2>&1 &'
    subprocess.Popen(rx_fox_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)




    qapp.exec_()

if __name__ == '__main__':
    main()

