import os, time
import vlc
from time import sleep
from onvif import ONVIFCamera
import zeep

class Player:
    '''
        args: set options
    '''
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

    # Set the URL or local file path to be played, and the resource will be reloaded every time it is called
    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # Play Success returns 0, failure returns -1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # pause 
    def pause(self):
        self.media.pause()

    # resume
    def resume(self):
        self.media.set_pause(0)

    # stop 
    def stop(self):
        self.media.stop()

    # release 
    def release(self):
        return self.media.release()

    # get status, is playing ?
    def is_playing(self):
        return self.media.is_playing()

    # get time elapsed, milisecond
    def get_time(self):
        return self.media.get_time()

    # Drag to play at the specified millisecond value. Return 0 on success, -1 on failure (note that only the current multimedia format or streaming protocol support will take effect)
    def set_time(self, ms):
        return self.media.get_time()

    # Total length of audio and video, return milliseconds
    def get_length(self):
        return self.media.get_length()

    # Get the current volume (0~100)
    def get_volume(self):
        return self.media.audio_get_volume()

    # Set the volume (0~100)
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # Return to current state: playing; paused; others
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # Current playback progress. Returns a floating point number between 0.0 and 1.0
    def get_position(self):
        return self.media.get_position()

    # Drag the current progress and pass in a floating point number between 0.0~1.0 (note that only the current multimedia format or streaming media support will take effect)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # Get the current file playback rate
    def get_rate(self):
        return self.media.get_rate()

    # Set the playback rate (for example: 1.2, which means that the playback speed is 1.2 times faster)
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # Set the aspect ratio (eg "16:9", "4:3")
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # Must be set to 0, otherwise the screen width and height cannot be modified
        self.media.video_set_aspect_ratio(ratio)

    # Register callback
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # Remove Callback
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)

    def my_call_back(event):
        print("call:", player.get_time())
class onvif():
    XMAX = 0.1
    XMIN = -0.1
    YMAX = 0.1
    YMIN = -0.1
    def zeep_pythonvalue(self, xmlvalue):
        return xmlvalue


    def perform_move(ptz, request, timeout):
        # Start continuous move
        ptz.ContinuousMove(request)
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        ptz.Stop({'ProfileToken': request.ProfileToken})


    def move_up(ptz, request, timeout=0.5):
        print('move up...')
        request.Velocity.PanTilt.x = 0
        request.Velocity.PanTilt.y = YMAX
        onvif.perform_move(ptz, request, timeout)


    def move_down(ptz, request, timeout=0.5):
        print('move down...')
        request.Velocity.PanTilt.x = 0
        request.Velocity.PanTilt.y = YMIN
        onvif.perform_move(ptz, request, timeout)


    def move_right(ptz, request, timeout=0.5):
        print('move right...')
        request.Velocity.PanTilt.x = XMAX
        request.Velocity.PanTilt.y = 0
        onvif.perform_move(ptz, request, timeout)


    def move_left(ptz, request, timeout=0.5):
        print('move left...')
        request.Velocity.PanTilt.x = XMIN
        request.Velocity.PanTilt.y = 0
        onvif.perform_move(ptz, request, timeout)


    def continuous_move():
        #address onvif with IP, Port, Username, Password
        mycam = ONVIFCamera('192.168.1.99', 80, 'admin', 'admin111')
        # Create media service object
        media = mycam.create_media_service()
        # Create ptz service object
        ptz = mycam.create_ptz_service()

        # Get target profile
        zeep.xsd.simple.AnySimpleType.pythonvalue = onvif.zeep_pythonvalue
        media_profile = media.GetProfiles()[0]

        # Get PTZ configuration options for getting continuous move range
        request = ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = media_profile.PTZConfiguration.token
        ptz_configuration_options = ptz.GetConfigurationOptions(request)

        request = ptz.create_type('ContinuousMove')
        request.ProfileToken = media_profile.token
        ptz.Stop({'ProfileToken': media_profile.token})

        if request.Velocity is None:
            request.Velocity = ptz.GetStatus({'ProfileToken': media_profile.token}).Position
            request.Velocity = ptz.GetStatus({'ProfileToken': media_profile.token}).Position
            request.Velocity.PanTilt.space = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
            request.Velocity.Zoom.space = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

        # Get range of pan and tilt
        # NOTE: X and Y are velocity vector
        global XMAX, XMIN, YMAX, YMIN
        XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
        XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
        YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
        YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

        while True :
            control = input('Untuk Kontrol, pakai w a s d ')

            if control == 'd':
                    # move right
                    onvif.move_right(ptz, request)
            if control == 'a':
                    # move left
                    onvif.move_left(ptz, request)
            if control == 'w':
                    # Move up
                    onvif.move_up(ptz, request)
            if control == 's':
                    # move down
                    onvif.move_down(ptz, request)

if "__main__" == __name__:
    player = Player()
    #player.add_callback(vlc.EventType.MediaPlayerTimeChanged, Player.my_call_back)

    #stream the camera
    player.play("rtsp://admin:admin111@192.168.1.99/Streaming/Channels/1")

    # play local file
    # player.play("D:/abc.mp3")

    # Prevent the current process from exiting
    while True:
        pass
        onvif.continuous_move()