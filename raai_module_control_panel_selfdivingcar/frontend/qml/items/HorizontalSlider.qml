import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: horizontalSlider

    signal sliderMaxChanged(val: real)
    signal sliderSteeringOffsetChanged(val: real)

    property real actualValue: 0
    property real value: 0
    property real maxValue: 0
    property real steeringOffset: 0


    Rectangle {
        id: background_rectangle
        radius: 10
        color: "grey"
        opacity: 0.5
        height: parent.height
        width: parent.width
    }



    Rectangle {
        radius: 10
        transformOrigin: Item.Left
        rotation: actualValue > 0 ? 180 : 0
        height: parent.height
        width: (parent.width / 2) * Math.abs(actualValue / 100)
        x: parent.width / 2
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop {
                position: 0.0
                color: window.slider_gradient_start
            }
            GradientStop {
                position: 1.0
                color: window.slider_gradient_stop
            }
        }
    }

    Rectangle {
        radius: 10
        color: "grey"
        opacity: 0.4
        transformOrigin: Item.Left
        rotation: actualValue > 0 ? 180 : 0
        height: parent.height
        width: (parent.width / 2) * Math.abs(actualValue / 100) * (strength_slider.value / 100)
        x: parent.width / 2

    }

    Text {
        text: (horizontalSlider.actualValue).toFixed(0)
        font.pointSize: parent.height / 2
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        color: window.slider_value_text_color
    }

    Text {
        id: steering_strength_text
        text: "Steering Strength"
        color: window.dark_blue_text_color
        font.bold: true
        font.pointSize: parent.height / 5
        anchors.top: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Text {
        id: steering_offset_text
        text: "Steering Offset"
        color: window.dark_blue_text_color
        font.bold: true
        font.pointSize: parent.height / 5
        anchors.top: strength_slider.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Slider {
        id: strength_slider
        x: parent.width / 2 - width / 2
        anchors.top: steering_strength_text.bottom
        height: parent.height / 2
        width: parent.width
        from: 0
        to: 100
        value: horizontalSlider.maxValue

        onMoved: horizontalSlider.sliderMaxChanged(value)

        handle: Rectangle {
            x: strength_slider.width * (strength_slider.value / 100) - width / 2
            anchors.verticalCenter: parent.verticalCenter
            height: parent.height
            width: parent.height / 3
            radius: 5
            color: window.slider_value_text_color
        }
    }

    Slider {
        id: offset_slider
        x: parent.width / 2 - width / 2
        anchors.top: steering_offset_text.bottom
        height: parent.height / 2
        width: parent.width
        from: -100
        to: 100
        value: horizontalSlider.steeringOffset

        onMoved: horizontalSlider.sliderSteeringOffsetChanged(value)

        handle: Rectangle {
            x: offset_slider.width / 2 + (offset_slider.width * (offset_slider.value / 200)) - width / 2
            anchors.verticalCenter: parent.verticalCenter
            height: parent.height
            width: parent.height / 3
            radius: 5
            color: window.slider_value_text_color
        }
    }

    Text {
        anchors.horizontalCenter: strength_slider.horizontalCenter
        anchors.verticalCenter: strength_slider.verticalCenter
        text: strength_slider.value.toFixed(1)
        font.pointSize: strength_slider.height / 2
        color: window.dark_blue_text_color
    }

    Text {
        anchors.horizontalCenter: offset_slider.horizontalCenter
        anchors.verticalCenter: offset_slider.verticalCenter
        text: offset_slider.value.toFixed(1)
        font.pointSize: offset_slider.height / 2
        color: window.dark_blue_text_color
    }
}
