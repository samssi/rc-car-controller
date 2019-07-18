# rc-car-controller

Project idea is to create RC Car with an advanced onboard computer. Onboard computer receives user input
via client with UDP. Onboard computer will send streaming video to the client to provide feedback on
where the car is going.

This project provides all components as monorepo.

## Overall architecture

![architecture](/architecture.jpg)

### Client/Server messaging

Client server exchange with UDP should cutoff all DC motors if no message is received within given
configurable time frame (eg. 1 seconds) to prevent uncontrollable acceleration or steering when
UDP connection is lost.

Client/Server must follow this specification:

* Client should maintain latest control message state and send it through within onboard server side
cutoff time frame
* Server side stop timer will reset after each event
* Server side will cutoff DC motors if no message received within the time frame and will resume
when connection is restored with the latest received client message

## client

Client can be made to support multiple input methods. Keyboard, joystick and even autonomous operations.
Current client is developed with OpenCV for the video and pygame for input and displaying of the video
stream.

Autonomous driving can be implemented to the client side or to the onboard
computer. 

## onboard-camera

Onboard camera is the component responsible for streaming the camera output. It uses cameras own
picamera library and is developed with Python. Current camera setup is Raspberry Pi Camera Module v2:
https://www.raspberrypi.org/documentation/hardware/camera/

## onboard-udp

onboard-udp is based on Python socket and is a very simple implementation of UDP server. Package loss
is not an issue when sending control commands and protocol must be very responsive so UDP seems like
a right choice for command input. Onboard UDP receives JSON data packets and transforms those into
GPIO/PWM signals which are sent to L293 MCU (see: http://www.ti.com/lit/ds/symlink/l293.pdf) This microcontroller will handle
driving the DC motors.

## onboard-rest

At some point other functions such as powering on the car remotely will become available. REST API will
offer functions for this applications. REST API will control the GPIO and eg. power on powering relay onboard.

## onboard-autonomous-driver

At some point autonomous driving may be implemented to the onboard computer.

![wip](/wip.jpg)

[![Demo](https://img.youtube.com/vi/HN2twrgcHbo/0.jpg)](https://www.youtube.com/watch?v=HN2twrgcHbo)
