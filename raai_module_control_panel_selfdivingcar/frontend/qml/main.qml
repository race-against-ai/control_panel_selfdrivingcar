import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./items"
import "./views"

Window {
    id: window

    color: "black"
    width: 1280
    height: 720

    minimumHeight: 480
    minimumWidth: 852

    visible: true
    title: qsTr("Race Against AI - Control Panel Selfdriving Car")

    signal sliderMaxThrottleChanged(real value)
    signal sliderMaxBrakeChanged(real value)
    signal sliderMaxClutchChanged(real value)
    signal sliderMaxSteeringChanged(real value)
    signal sliderAllMaxSpeedChanged(real value)
    signal sliderCurveSpeedChanged(real value)
    signal sliderStraightLineSpeedChanged(real value)

    signal sliderSteeringOffsetChanged(real value)

    signal buttonButtonStatusChanged()
    signal buttonResetHeadTracking()
    signal buttonPedalStatusChanged()
    signal buttonPlatformStatusChanged()
    signal buttonHeadTrackingChanged()
    signal buttonStartStatusChanged()
    signal buttonStreamStatusChanged()
    signal buttonMotorStatusChanged()
    signal buttonDebugStatusChanged()
    signal buttonProcessStatusChanged()


    signal timerStart()
    signal timerPause()
    signal timerStop()
    signal timerReset()
    signal timerResetFull()
    signal timerIgnore()

    property string background_color_start_light: "#e1e8f5"
    property string background_color_stop_light: "#a5acb8"

    property string light_grey: "#bfbfbf"

    property string caption_text_color: "#274c87"

    property string slider_gradient_start: "black"
    property string slider_gradient_stop: "#326ecf"
    property string slider_value_text_color: "#8eb1ed"
    property string slider_box_start: "#251887"
    property string slider_box_stop: "#251d63"

    property string dark_blue_text_color: "#274c87"
    property string light_blue_text_color: "#9bbefa"

    // reading window.visibility doesn't return the state (as in "Windowed")
    // this property is needed
    property bool isFullScreen: false

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: mainView

        Database {
            id: nameView
            onNavigateBack: stackView.pop()
        }

        MainView {
            id: mainView

            onNavigateNext: stackView.push(nameView)
        }
    }

    VariousButton {
        id: hamburgerButton
        text: "☰"
        anchors.top: parent.top
        anchors.left: parent.left
        height: parent.height * 0.05
        width: parent.width * 0.05

        onClicked: menu.open()

        Menu {
            id: menu
            x: hamburgerButton.x
            y: hamburgerButton.height

            MenuItem {
                text: "Main View"
                onTriggered: nameView.navigateBack()
            }

            MenuItem {
                text: "Database"
                onTriggered: mainView.navigateNext()
            }
        }
    }
}
