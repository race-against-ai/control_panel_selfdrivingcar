import QtQuick 2.0
import QtQuick.Controls 2.15

Item {
    id: verticalSlider

    signal sliderMaxChanged(val: real)

    property real value: 0
    property real actualValue: 0
    property real maxValue: 0
    property real rotation: 0

    property string text: ""


    Rectangle {
        radius: 10
        color: "grey"
        opacity: 0.5
        height: parent.height
        anchors.left: parent.left
        anchors.right: parent.right

    }

    Rectangle {
        radius: 10
        anchors.bottom: parent.bottom
        height: parent.height * (Math.abs(verticalSlider.value) / 100)
        anchors.left: parent.left
        anchors.right: parent.right

        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: window.slider_gradient_stop
            }
            GradientStop {
                position: 1.0
                color: window.slider_gradient_start
            }
        }
    }

    Rectangle {
        radius: 10
        anchors.bottom: parent.bottom
        height: parent.height * (Math.abs(verticalSlider.value) / 100)
        anchors.left: parent.left
        anchors.right: parent.right
        color: "#b4c3db"
        opacity: 0.4
    }

    Text {
        id: headline
        text: parent.text
        rotation: parent.rotation
        color: window.light_blue_text_color
        x: parent.width / 2 - width / 2
        y: parent.height - width
        font.pixelSize: parent.width * 0.3

    }

    Text {
        text: strength_slider.value.toFixed(0)
        color: window.light_blue_text_color
        rotation: parent.rotation
        x: parent.width / 2 - width / 2
        y: 30
        font.pointSize: parent.width * 0.5

    }


    Slider {
        id: strength_slider
        y: parent.height / 2 - height / 2
        x: parent.width - width / 2 - (parent.text === "throttle" ? parent.width : 0)
        rotation: 90
        height: 20
        width: parent.height
        from: 100
        to: 0
        value: verticalSlider.maxValue

        onMoved: {
                verticalSlider.value = value
                verticalSlider.sliderMaxChanged(value)

                 }

        handle: Rectangle {
            x: strength_slider.width - (strength_slider.width * (strength_slider.value / 100))
            anchors.verticalCenter: parent.verticalCenter
            height: parent.height
            width: parent.height / 3
            radius: 5
            color: window.dark_blue_text_color
        }


    }



}
