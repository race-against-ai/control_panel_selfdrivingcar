import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./../items"

Item {
    signal navigateNext()
    signal sliderMaxThrottleChanged(int value)
    signal sliderMaxBrakeChanged(int value)
    signal sliderMaxClutchChanged(int value)
    signal sliderMaxSteeringChanged(int value)
    //signal sliderStraightLineSpeedChanged(int value)
    //signal sliderCurveSpeedChanged(int value)

    anchors.fill: parent


    Rectangle {
        id: background
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop {
                position: 0.0
                color: background_color_start_light
            }
            GradientStop {
                position: 1.0
                color: background_color_stop_light
            }
        }
        Component.onCompleted: {
            console.log("Background created");
        }
    }

    Image {
        id: vw_logo
        source: "./../pictures/ui_Background_VW_logo.svg"
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit
        height: parent.height
        width: parent.width
        scale: 0.9
    }
    
    Item {
        id: wheels

        Wheels {
            x: car_image.x
            y: car_image.y * 1.1
            steering_value: -control_panel_model.steering
        }

        Wheels {
            x: car_image.x + car_image.width - car_image.width * 0.15
            y: car_image.y *1.1
            steering_value: -control_panel_model.steering
        }

    }

    IconImage {
        id: car_image
        source: "./../pictures/ui_car_car.svg"
        height: parent.height / 2
        width: height / 2
        x: parent.width / 2 - width / 2
        y: parent.height * 0.4
        color: dark_blue_text_color


    }


    Image {
        id: ngitl_logo
        source: "./../pictures/ui_Background_NGITL_logo_logo.svg"
        anchors.fill: parent
    }


    Text {
        text: "Selfdriving Car"
        y: 10
        x: parent.width / 2 - width / 2
        color: caption_text_color
        font.pointSize: parent.height / 15
        font.bold: true
    }

    VerticalSlider {
            id: curvespeed_bar
            text: "curvespeed"
            rotation: -90
            x: parent.width * 0.25
            y: parent.height / 2 - height / 2
            width: parent.width * 0.04
            height: parent.height * 0.7

            value: control_panel_model.curvespeed
            actualValue: control_panel_model.curvespeed
            maxValue: control_panel_model.curvespeed

            onSliderMaxChanged: function(val) {
                control_panel_model.curvespeed = val
                sliderCurveSpeedChanged(val)
                //console.log("Curvspeed Slider value changed: " + value)
                //console.log(val)
            }

            
        }

   VerticalSlider {
            id: straightlinespeed_bar
            text: "straightlinespeed"
            rotation: 90
            x: parent.width * 0.75 - width
            y: parent.height / 2 - height / 2
            width: parent.width * 0.04
            height: parent.height * 0.7

            value: control_panel_model.straightlinespeed
            actualValue: control_panel_model.actual_straightlinespeed
            maxValue: control_panel_model.straightlinespeed



            onSliderMaxChanged: function(val) {
                control_panel_model.straightlinespeed = val
                sliderStraightLineSpeedChanged(val)
                //console.log("Straightlinespeed Slider value changed: " + value)
                //console.log(val)
            }

        }





    ControlBox {
        id: left_setting_box
        height: parent.height * 0.7
        width: parent.width * 0.1
        y: parent.height / 2 - height / 2
        x: parent.width * 0.125
    }

    TimerBox {
        id: right_setting_box
        height: parent.height * 0.7
        width: parent.width * 0.1
        y: parent.height / 2 - height / 2
        x: parent.width * 0.875 - width

    }

    HorizontalSlider {
        id: steering_bar
        width: parent.width * 0.4
        height: parent.width * 0.04
        x: parent.width / 2 - width / 2
        y: parent.height * 0.15

        value: control_panel_model.steering
        actualValue: control_panel_model.actual_steering
        maxValue: control_panel_model.max_steering
        steeringOffset: control_panel_model.steering_offset

        onSliderMaxChanged: function(val) {
            window.sliderMaxSteeringChanged(val)
        }

        onSliderSteeringOffsetChanged: function(val) {
            window.sliderSteeringOffsetChanged(val)
        }
    }

    Rectangle {
        id: timerBackground
        x: window.width / 2 - width / 2
        y: window.height * 0.9
        radius: 10
        color: window.light_grey
        width: timer.width * 1.2
        height: timer.height * 1.05
        border.color: "white"
        border.width: 5

        Text {
            id: timer
            text: String(t_model.minutes).padStart(2, '0') + ":" + String(t_model.seconds).padStart(2, '0') + "." + String(t_model.millis).padStart(3, '0')
            anchors.verticalCenter: timerBackground.verticalCenter
            anchors.horizontalCenter: timerBackground.horizontalCenter
            color: window.dark_blue_text_color
            font.pointSize: window.height / 30
            font.bold: true
        }
    }

}
